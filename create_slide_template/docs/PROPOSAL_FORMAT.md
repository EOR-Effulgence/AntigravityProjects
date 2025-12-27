# Proposal Markdown Format Specification (`PROPOSAL_FORMAT.md`)

... (前略) ...

## 4. 図解 (Diagram) の記述

単純なフロー図やプロセス図を、PowerPointのシェイプ（図形）として自動生成できます。
`diagram:タイプ` を指定して、要素をリスト形式で記述します。

### 構文
````markdown
```diagram:process
Step 1: 現状分析
Step 2: 戦略策定
Step 3: 実行
```
````

### Diagramの種類 (`diagram:xxx`)
*   `process`: 左から右へ流れるプロセス図（矢印で連結）
*   `cycle`: 循環型のサイクル図（PDCAなど）
*   `list`: 強調したいポイントのリスト

### 例: PDCAサイクル
````markdown
```diagram:cycle
Plan: 計画
Do: 実行
Check: 評価
Act: 改善
```
````

... (後略) ...
