---
marp: true
theme: default
paginate: true
header: '令和X年度 保健事業報告'
footer: '© 〇〇市 健康福祉部'
style: |
  /* グローバルスタイル: 余白を十分に確保 */
  section {
    background: linear-gradient(135deg, #f5f7fa 0%, #dae2ee 100%);
    font-size: 26px;
    padding: 60px 80px; /* 余白を拡大 */
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
  }
  h1 {
    color: #1a365d;
    font-size: 1.6em;
    border-bottom: 3px solid #3182ce;
    padding-bottom: 10px;
    margin-top: 0;
    margin-bottom: 30px;
    width: 100%;
  }
  h2 {
    color: #2c5282;
    font-size: 1.25em;
    margin-top: 15px;
    margin-bottom: 10px;
  }
  /* グリッドレイアウト: 右側の見切れを防止 */
  .grid-2col {
    display: grid;
    grid-template-columns: 60% 40%;
    gap: 40px;
    align-items: center; /* 垂直中央揃えでバランスを調整 */
    width: 100%;
  }
  .content-left {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }
  .content-right {
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .content-right img {
    max-width: 95%; /* 枠からはみ出さないよう制限 */
    max-height: 400px;
    object-fit: contain;
    border-radius: 12px;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  }
  /* 表紙用特別スタイル */
  section.lead {
    justify-content: center;
    text-align: center;
    background: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)), url('images/healthcare_title_bg.png');
    background-size: cover;
  }
  section.lead h1 {
    border-bottom: none;
    font-size: 2.2em;
    margin-bottom: 10px;
  }
  /* テーブル調整: 中央配置と横幅の最適化 */
  table {
    font-size: 0.9em;
    margin: 20px auto; /* 中央寄せ */
    width: 90%;
    border-collapse: collapse;
  }
  th, td {
    padding: 12px;
  }
  /* 引用 (Before/After用) のセンタリング */
  blockquote {
    background: rgba(49, 130, 206, 0.05);
    border-left: 5px solid #3182ce;
    padding: 15px 25px;
    margin: 20px auto;
    width: 85%;
  }
---

<!-- _class: lead -->

# 特定健診・糖尿病性腎症重症化予防
# 事業実施報告書

### 〜要医療者・治療中断者への介入と成果〜

**〇〇市 健康福祉部 国保年金課**
202X年X月X日

---

# 1. 事業の背景と目的

<div class="grid-2col">

<div class="content-left">

本市における透析患者数は年々増加傾向にあり、医療費の適正化が急務となっています。

*   **現状の課題:**
    *   要医療者の受診未済率が高い
    *   糖尿病治療中断者の重症化リスク
*   **目的:**
    *   データ活用によるハイリスク者の抽出
    *   早期治療導入と継続支援の強化

</div>

<div class="content-right">

![](images/dialysis_challenge.png)

</div>

</div>

---

# 2. 対象者の抽出スキーム

<div class="grid-2col">

<div class="content-left">

KDBシステムを活用し、優先度の高い対象者を論理的に抽出しました。

*   **A群 (緊急):**
    HbA1c 8.0以上 + 未治療
*   **B群 (再開):**
    治療中断 6ヶ月以上

AI予測モデルによる更なる精度向上も計画中です。

</div>

<div class="content-right">

![w:400](images/risk_stratification_diagram.png)

</div>

</div>

---

# 3. 実施した介入施策

<div class="grid-2col">

<div class="content-left">

対象者の心理的ハードルを考慮した重層的なアプローチ。

*   **ナッジ理論の応用:**
    開封率を高め、行動変容を促すデザイン。
*   **医療連携の強化:**
    地域医師会と連携した受診しやすい環境整備。

</div>

<div class="content-right">

![](images/nudge_intervention.png)

</div>

</div>

---

# 4. 事業成果 (定量的評価)

介入の結果、顕著な受診行動の変容が確認されました。

| 対象区分 | 受診確認数 | 受診率 | 前年比 |
| :--- | :---: | :---: | :---: |
| 緊急勧奨 (A群) | 98名 | **65.3%** | +12.0pt |
| 治療再開 (B群) | 115名 | **35.9%** | +5.4pt |
| **全体** | **213名** | **45.3%** | **+8.2pt** |

> **Before/After:**
> 特に、保健師による個別勧奨を強化したA群において、高い成果が得られました。

---

# 5. 重症化予防効果の試算

<div class="grid-2col">

<div class="content-left">

本事業による医療費適正化の推計効果です。

*   **透析移行予防数:**
    推計 **2.5人** / 年
*   **医療費抑制効果:**
    **約 1,250 万円 / 年**
    (1人あたり約500万円として試算)

</div>

<div class="content-right">

![](images/cost_savings.png)

</div>

</div>

---

# 6. 今後の課題と展望

<div class="grid-2col">

<div class="content-left">

## 次年度の方針 (DX推進)
1. **SMS勧奨の導入:** 到達率向上
2. **AIコールの活用:** 業務効率化
3. **オンライン指導:** フォローアップ拡充

## 課題
*   若年層へのリーチ手法の確立
*   保健師の業務負荷分散

</div>

<div class="content-right">

![](images/healthcare_dx_future.png)

</div>

</div>

---

<!-- _class: lead -->

# ご清聴ありがとうございました

**健康福祉部 保健予防課**
(内線: XXXX)
