# JMDCテンプレート移行ガイド

## 1. 現状のステータス
JMDCの企業テンプレート (`JMDC2022_16対9(標準)_基本テンプレ_v1.2.pptx`) はGoogleスライドへ変換され、以下のIDで利用可能です。

-   **Presentation ID**: `1R_Y7SgxFhqSWnGs0zYaTOKlhpWQra3lebYu3jM5Rq1M`
-   **deck.yaml**: 既にこのIDを使用するように設定済みです。

## 2. 残された作業：レイアウト名のマッピング
`deck` が正しいデザインを適用するには、Googleスライド上で定義されている**正確なレイアウト名**を知る必要があります。

### 手順
1.  **deckの認証設定**:
    まだ認証を行っていない場合、以下のコマンドで認証ファイルを生成してください。
    ```bash
    # ブラウザが開きます
    deck auth
    ```

2.  **レイアウト一覧の取得**:
    以下のコマンドを実行し、利用可能なレイアウト名を表示します。
    ```bash
    deck ls-layouts --presentation-id 1R_Y7SgxFhqSWnGs0zYaTOKlhpWQra3lebYu3jM5Rq1M
    ```
    
    出力例：
    ```
    TITLE_SLIDE (タイトル)
    SECTION_HEADER (セクションヘッダー)
    MAIN_POINT (ポイント)
    ...
    ```

3.  **deck.yamlの更新**:
    `deck.yaml` をテキストエディタで開き、`layout: "タイトル"` の部分を、上記コマンドで確認した**実際のレイアウト名**（例: "TITLE_SLIDE" や "タイトル" など）に書き換えてください。

## 3. 完了確認
設定が正しければ、以下のコマンドでJMDCデザインが適用されたスライドが生成されます。

```bash
deck sample_presentation.md
```
