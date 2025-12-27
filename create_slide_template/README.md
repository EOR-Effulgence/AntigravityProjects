# AI Presentation Generator

AIエージェントを活用して、MarkdownテキストからプロフェッショナルなPowerPointスライドを自動生成するシステムです。

## 🚀 特徴
*   **Markdown First**: 構成案は全てMarkdownで記述・編集可能。
*   **Native Charts**: Markdown内のテキストデータから、編集可能なPowerPointグラフを生成。
*   **Diagram Support**: フロー図やサイクル図もMarkdownから自動描画。
*   **Customizable**: テンプレート、フォント、カラーパレットを自由に設定可能。

## 📂 ドキュメント
詳細は `docs/` ディレクトリを参照してください。
*   [`PROPOSAL_FORMAT.md`](docs/PROPOSAL_FORMAT.md): スライド構成やグラフ・図解の記法リファレンス
*   [`PROMPT_DESIGN.md`](docs/PROMPT_DESIGN.md): AIプロンプトの設計思想と運用ガイド
*   [`walkthrough_log.md`](docs/walkthrough_log.md): 最新機能の動作検証記録
*   [`refactoring_log.md`](docs/refactoring_log.md): リファクタリング計画記録

## 🛠 使い方

### 1. 全自動生成 (Requires API Key)
Gemini APIを使用して、トピックから提案書を生成します。
```bash
export GEMINI_API_KEY="your_api_key"
python3 generate_proposal.py --topic "新規事業案"
```

### 2. Markdownから変換 (Manual Mode)
手元のMarkdownファイルをスライドに変換します。
```bash
python3 run_gen.py my_draft.md output/result.pptx
```

## ⚙️ 設定
`config/settings.yaml` でフォントやカラーパレットを変更できます。

```yaml
design:
  font:
    name: "Noto Sans CJK JP"
  colors:
    palette: 
      - "#0052cc" # Primary Color
      ...
```
