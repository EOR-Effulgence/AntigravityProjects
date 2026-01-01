# deck × Google AI画像生成の統合可能性

**結論：deckはコードブロック→画像変換機能により、外部画像生成コマンドと統合可能。ただし、Gemini/Imagen APIとの直接連携は自前で構築する必要がある。** 最も現実的なワークフローは、deckの`codeBlockToImageCommand`機能にGemini API呼び出しスクリプトを組み込むか、deck変換後にSlides API経由でAI画像を挿入するパイプラインの構築となる。

---

## deckの画像挿入機能は柔軟性が高い

deck（k1LoW/deck）は、Go製のMarkdown→Google Slides変換ツールで、GitHub Stars **1,100+**の活発なプロジェクト。画像処理において以下の機能を提供する。

### 標準的な画像参照

通常のMarkdown記法で画像を埋め込める：

```markdown
![ローカル画像](./assets/diagram.png)
![外部URL](https://example.com/image.jpg)
```

**対応フォーマット**はPNG、JPEG、GIFの3種類（Google Slides API制約）。ローカルファイルは一時的にGoogle Driveにアップロードされ、公開URLを取得してSlides APIに渡される。

### 動的画像生成との統合：codeBlockToImageCommand

deckの最も強力な機能は、**コードブロックを画像に変換**する仕組み。これにより、AI画像生成との統合が可能になる。

```yaml
---
presentationID: xxxxx
codeBlockToImageCommand: "./generate-ai-image.sh"
---
```

Markdownでプロンプトを記述し、外部コマンドで画像を生成できる：

````markdown
```ai-image
ビジネス向けの四半期売上成長グラフ
```
````

外部コマンドは以下の環境変数を受け取る：
- **`CODEBLOCK_LANG`**: 言語識別子（上記例では `ai-image`）
- **`CODEBLOCK_CONTENT`**: コードブロックの内容（プロンプト）
- **`CODEBLOCK_OUTPUT`**: 出力先の一時ファイルパス

### Songmu/laminateによる拡張

**laminate**は、deckと組み合わせて使う画像生成ルーターで、言語ごとに異なるコマンドを実行できる：

```yaml
# ~/.config/laminate/config.yml
patterns:
  - lang: mermaid
    run: 'mmdc -i - -o "{{output}}" --quiet'
  - lang: ai-image
    run: './scripts/gemini-image.sh "{{input}}" "{{output}}"'
  - lang: "*"
    run: 'silicon --from-clipboard -o "{{output}}"'
```

---

## Google Slides APIとImagen/Gemini APIの連携

### 直接連携は不可能、パイプライン構築が必要

**重要な制約**：Google Slides APIは**公開アクセス可能なURL**からのみ画像を挿入できる。Base64データや非公開のDriveファイルIDは直接使用できない。

したがって、以下のパイプラインが必要：

```
Vertex AI Imagen API → Cloud Storage/Drive → 公開URL取得 → Slides API
```

### Vertex AI Imagen APIの概要

**利用可能なモデル**（2025年12月時点）：

| モデル | 用途 |
|--------|------|
| `imagen-4.0-generate-001` | 最新GA、汎用 |
| `imagen-4.0-ultra-generate-001` | 最高品質 |
| `imagen-3.0-generate-002` | 安定版、本番運用向け |

### Python統合コード例

```python
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
from google.cloud import storage
from googleapiclient.discovery import build
import datetime

# 1. Vertex AI Imagenで画像生成
vertexai.init(project="PROJECT_ID", location="us-central1")
model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")
images = model.generate_images(
    prompt="ビジネスプレゼン用の成長グラフ",
    aspect_ratio="16:9"
)

# 2. Cloud Storageにアップロード
storage_client = storage.Client()
bucket = storage_client.bucket("my-bucket")
blob = bucket.blob("generated-image.png")
blob.upload_from_string(images[0]._image_bytes, content_type="image/png")

# 3. 署名付きURL生成（15分有効）
url = blob.generate_signed_url(expiration=datetime.timedelta(minutes=15))

# 4. Google Slidesに挿入
slides_service = build('slides', 'v1', credentials=creds)
requests = [{
    "createImage": {
        "url": url,
        "elementProperties": {
            "pageObjectId": "SLIDE_ID",
            "size": {"width": {"magnitude": 4000000, "unit": "EMU"},
                     "height": {"magnitude": 3000000, "unit": "EMU"}}
        }
    }
}]
slides_service.presentations().batchUpdate(
    presentationId="PRESENTATION_ID",
    body={"requests": requests}
).execute()
```

---

## Gemini in Google Slidesの「Help me visualize」機能

### 機能概要

Google Slidesの「**挿入 → Help me visualize**」から利用可能：
- **Image**: テキストプロンプトから画像生成
- **Slide**: スライド全体をデザイン
- **Infographic**: データ可視化インフォグラフィック

画像生成には**Nano Banana Pro**（Imagen 3ベース）が使用される。

### API経由でのアクセスは不可能

**重要な制約**：「Help me visualize」機能は**UIからのみ利用可能**であり、Google Slides APIやApps Scriptから呼び出すことはできない。自動化にはGemini APIとSlides APIを個別に組み合わせる必要がある。

---

## 実現可能なワークフロー

### ワークフロー1：deck + カスタム画像生成コマンド（推奨）

最もシームレスな統合方法。deckの`codeBlockToImageCommand`にGemini/Imagen API呼び出しスクリプトを設定：

```bash
#!/bin/bash
# gemini-image.sh
PROMPT=$(cat)  # 標準入力からプロンプト取得
OUTPUT=$CODEBLOCK_OUTPUT

curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"contents\":[{\"parts\":[{\"text\":\"$PROMPT\"}]}]}" \
  | jq -r '.candidates[0].content.parts[0].inlineData.data' \
  | base64 -d > "$OUTPUT"
```

**Markdown側**：
````markdown
---
codeBlockToImageCommand: "./gemini-image.sh"
---

# 売上レポート

```ai
四半期売上の成長を示すプロフェッショナルな棒グラフ、青色基調
```
````

### ワークフロー2：deck変換後にSlides APIで画像挿入

1. Markdownにプレースホルダーを配置：`{{IMAGE:growth-chart}}`
2. deckで基本スライドを生成
3. Pythonスクリプトでプレースホルダーを検出
4. Gemini APIで画像生成 → Cloud Storageにアップロード
5. Slides APIの`replaceAllShapesWithImage`で置換

### ワークフロー3：NotebookLM + 手動テンプレート適用

NotebookLMのSlide Deck機能はNano Banana Proで高品質な画像付きスライドを生成するが、**PDFエクスポートのみ**対応。

**限界**：
- Google Slides形式で出力不可
- 会社テンプレートの適用不可
- 編集可能なスライドとして再利用困難

**活用方法**：生成されたスライドデザインを参考に、別途deckやSlides APIで再構築する「デザインリファレンス」としての利用が現実的。

---

## 代替ツールとの比較

| ツール | AI画像生成 | Google Slides出力 | テンプレート対応 | API連携 |
|--------|-----------|------------------|----------------|---------|
| **deck + Gemini** | ✅ 構築可能 | ✅ ネイティブ | ✅ 完全対応 | ✅ 自前構築 |
| **Plus AI** | ✅ Pro以上 | ✅ ネイティブ | ✅ Team以上 | ✅ 完備 |
| **NotebookLM** | ✅ 高品質 | ❌ PDFのみ | ❌ 非対応 | ❌ なし |
| **Gamma** | ✅ あり | ⚠️ PPTX経由 | ⚠️ 基本のみ | ⚠️ 限定的 |
| **SlidesAI** | ⚠️ Pro以上 | ✅ アドオン | ❌ 非対応 | ❌ なし |

---

## 推奨アプローチ

### 最適解：deck + laminate + Gemini APIカスタムコマンド

1. **laminate設定**で言語ルーティングを構築
2. `ai-image`言語のコードブロックをGemini APIに送信
3. 生成画像を一時ファイルに保存
4. deckが自動的にDriveアップロード → Slides挿入

```yaml
# laminate設定
patterns:
  - lang: ai-image
    run: './scripts/gemini-generate.py "{{input}}" -o "{{output}}"'
  - lang: mermaid
    run: 'mmdc -i - -o "{{output}}"'
```

**メリット**：
- Markdownベースのワークフロー維持
- 会社テンプレート完全対応（deck機能）
- 画像生成ロジックを自由にカスタマイズ可能
- CI/CDパイプラインに組み込み可能

**必要な開発**：
- Gemini/Imagen API呼び出しスクリプト（50-100行程度）
- Cloud Storage署名URL生成ロジック
- エラーハンドリングとリトライ機構

---

## 結論と次のステップ

deckとGoogle AI画像生成の統合は**十分に実現可能**だが、既製の統合は存在しないため**カスタム開発が必要**。

**即座に始められるアクション**：
1. Gemini APIキーの取得（Google AI Studio）
2. 画像生成シェルスクリプトのプロトタイプ作成
3. laminate設定でルーティング構築
4. テスト用Markdownで動作確認

**開発工数の目安**：基本的なパイプライン構築に**2-3日**、エラーハンドリングと本番品質への改善に**追加1週間**程度。
