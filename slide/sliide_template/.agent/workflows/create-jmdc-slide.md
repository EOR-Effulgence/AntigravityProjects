---
description: JMDCテンプレートを使用してMarpスライドを新規作成する
---

# JMDCテンプレートでスライド作成

## テンプレート参照先
`slide_jmdc_template/` フォルダ内のファイルを参照してください：
- `theme.css` - Marpテーマ（CSS変数とスライドレイアウト定義）
- `examples/sample.md` - 使用例
- `README.md` - スライドクラスの説明

## 手順

### 1. 新規Markdownファイル作成
プロジェクトルートに新しい `.md` ファイルを作成します。

### 2. フロントマターを設定
```markdown
---
marp: true
lang: ja-JP
size: 16:9
---
```

### 3. スライドクラスを使用

**タイトルスライド:**
```markdown
<!-- _class: title-slide -->
# タイトル
## サブタイトル
発表者名
```

**アジェンダスライド:**
```markdown
<!-- _class: agenda-slide -->
<!-- _footer: © JMDC Inc. -->
# アジェンダ
- 項目1
- 項目2
```

**中見出しスライド:**
```markdown
<!-- _class: chapter-slide -->
<!-- _footer: © JMDC Inc. -->
## Part 1
# セクションタイトル
```

**コンテンツスライド:**
```markdown
<!-- _class: content-slide -->
<!-- _footer: © JMDC Inc. -->
# スライドタイトル
本文
```

**終了スライド:**
```markdown
<!-- _class: end-slide -->
# Thank you
```

### 4. ビルド
// turbo
```bash
npx @marp-team/marp-cli@latest [作成したファイル].md --theme slide_jmdc_template/theme.css -o output.html
```

### 5. 確認
// turbo
```bash
python3 -m http.server 8080
```
ブラウザで http://localhost:8080/output.html を開く

## 注意事項
- imagesフォルダはテンプレートフォルダ内に配置されているため、HTMLを開く際はローカルサーバー経由で確認してください
- フッターは `<!-- _footer: © JMDC Inc. -->` ディレクティブで設定
