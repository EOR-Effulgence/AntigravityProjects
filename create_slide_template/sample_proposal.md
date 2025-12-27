<!-- layout: 表紙 -->
# MDベース提案システム
## MarkdownからPPTXを生成するテスト
2025年12月28日

---

<!-- layout: 目次 -->
# 本日のアジェンダ

1. Markdownの利点
2. グラフ記述のデモ
3. 自動配置の確認

---

<!-- layout: コンテンツ -->
# グラフ記述のデモ (Excelライク)

CSV形式のテキストから、PowerPointのネイティブグラフを生成します。

```chart:column
部門別売上実績
部門, 2023年, 2024年
営業1課, 500, 650
営業2課, 450, 480
マーケ, 300, 400
```

<!-- note: このグラフはmd_to_slide.pyによって自動生成されました。 -->

---

<!-- layout: コンテンツ -->
# 円グラフのテスト

シェアなどの表現に最適です。

```chart:pie
スマートフォンOSシェア
OS, シェア(%)
iOS, 65
Android, 34
Others, 1
```

*   日本市場におけるシェア
*   若年層でのiPhone人気が顕著

---

<!-- layout: コンテンツ -->
# フロー図の自動生成デモ (Process & Cycle)

Markdownで記述するだけで、PowerPointのシェイプ（図形）としてフローチャートを描画します。

## プロセス図 (Process)
```diagram:process
Status 1: 調査・分析
Status 2: 企画立案
Status 3: 開発・実装
Status 4: リリース
```

## サイクル図 (Cycle)
```diagram:cycle
Plan
Do
Check
Act
```

