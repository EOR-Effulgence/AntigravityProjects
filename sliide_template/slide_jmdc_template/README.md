# JMDC Marp Template

JMDCブランドのMarpプレゼンテーションテンプレートです。

## クイックスタート

```bash
# 依存関係のインストール
npm install

# HTMLとして出力
npm run build

# PDFとして出力
npm run build:pdf
```

## 手動ビルド

```bash
npx @marp-team/marp-cli@latest your-presentation.md -o output.html
```

## スライドタイプ

### タイトルスライド (`title-slide`)
```markdown
---
marp: true
---

<!-- _class: title-slide -->

# プレゼンテーションタイトル

## サブタイトル

発表者名 / 日付
```

### アジェンダスライド (`agenda-slide`)
```markdown
---

<!-- _class: agenda-slide -->
<!-- _footer: © JMDC Inc. -->

# アジェンダ

- 項目1
- 項目2
- 項目3
```

### 中見出しスライド (`chapter-slide`)
```markdown
---

<!-- _class: chapter-slide -->
<!-- _footer: © JMDC Inc. -->

## Part 1

# セクションタイトル
```

### コンテンツスライド (`content-slide`)
```markdown
---

<!-- _class: content-slide -->
<!-- _footer: © JMDC Inc. -->

# スライドタイトル

本文テキスト
```

### 終了スライド (`end-slide`)
```markdown
---

<!-- _class: end-slide -->

# Thank you
```

## ファイル構成

```
├── theme.css       # Marpテーマ
├── images/         # ロゴ・アイコン
├── examples/       # サンプル
└── .marprc.yml     # CLI設定
```

## カスタマイズ

`theme.css` のCSS変数を編集してカラーを変更できます：

```css
--color-accent: #0CAA41;   /* メインカラー */
--color-accent2: #53C57A;  /* サブカラー */
```

## ライセンス

JMDC Inc. 社内利用限定
