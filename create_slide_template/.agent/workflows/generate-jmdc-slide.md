---
description: JMDCテンプレートを使用してPowerPointスライドを生成する
---

# JMDC PowerPointスライド生成ワークフロー

このワークフローは、JMDCのPowerPointテンプレートを使用して営業スライド・提案書・報告書を生成する手順を定義します。

## 前提条件
- Python 3.x がインストールされていること
- python-pptx がインストールされていること（`pip3 install python-pptx`）

## 手順

### 1. プロンプト集を確認
`prompts/slide_prompts.md` を参照して、作成したいスライドの種類に合ったプロンプトを選択します。

### 2. ユーザーから情報を収集
プロンプトの【入力情報】に必要な情報をユーザーから収集します。

### 3. JSONデータを生成
収集した情報をもとに、以下の形式でJSONファイルを作成します：

```json
{
  "clear_existing": true,
  "slides": [
    {"layout": "表紙", "title": "タイトル", "subtitle": "サブタイトル"},
    {"layout": "目次", "title": "目次", "body": "アジェンダ内容"},
    {"layout": "中見出し", "subtitle": "セクション名", "title": "詳細説明"},
    {"layout": "コンテンツ", "title": "ページタイトル", "content": ["項目1", "項目2"]},
    {"layout": "裏表紙"}
  ]
}
```

**利用可能なレイアウト**: 表紙、目次、中見出し、コンテンツ、裏表紙

### 4. JSONファイルを保存
// turbo
```bash
# 作業ディレクトリに移動してJSONファイルを保存
cd /Users/hiratani/Documents/AntigravityProjects/create_slide_template
```

JSONデータを `output/slide_data.json` に保存します。

### 5. PPTXを生成
// turbo
```bash
python3 scripts/generate_slide.py output/slide_data.json output/generated.pptx
```

### 6. 出力を確認
生成されたPPTXファイル `output/generated.pptx` をユーザーに提示します。

## テンプレート情報

テンプレートの詳細は `template_analysis.json` を参照してください。

## トラブルシューティング

- **レイアウトが見つからない**: レイアウト名は「表紙」「目次」「中見出し」「コンテンツ」「裏表紙」のいずれかを使用
- **文字化け**: JSONファイルはUTF-8で保存してください
- **プレースホルダーに内容が入らない**: JSONのキー名（title, subtitle, body, content, footer）を確認
