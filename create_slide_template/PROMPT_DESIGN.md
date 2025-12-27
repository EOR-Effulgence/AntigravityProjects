# プロンプト設計と運用マニュアル (PROMPT_DESIGN.md)

このドキュメントは、提案書生成システムのAIプロンプト設計思想と、他の環境で再現するためのガイドラインをまとめたものです。

## 1. システム概要
本システムは、「プランナー」「ライター」「デザイナー」という3つの役割を持つAIエージェントが協調して動作するマルチエージェントアーキテクチャを採用しています。

### エージェントの役割
1.  **Proposal Planner (構成担当)**: トピックから全体の章立て（スライド構成とレイアウト）を決定します。
2.  **Content Writer (執筆担当)**: 各スライドの詳細なテキストコンテンツを執筆します。
3.  **Visual Designer (視覚担当)**: スライド内容に合わせた画像プロンプトやグラフデータを生成します。

## 2. プロンプト設計思想

### 基本原則
*   **日本語思考・日本語出力**: 日本のビジネス文脈に適合させるため、入力・出力ともに日本語を指定しています。
*   **構造化データ (JSON)**: プログラムで確実に処理するため、全ての出力をJSON形式に限定しています。
*   **役割の分離 (Role Separation)**: 1つのプロンプトで全てを行おうとせず、工程を分けることで質を高めています。

### プロンプトファイル一覧
| ファイル名 | 役割 | 入力パラメータ |
|:---:|:---:|:---|
| `prompts/proposal_planner.txt` | 全体のスライド構成案を作成 | `{topic}` (トピック), `{audience}` (読者), `{num_slides}` (枚数) |
| `prompts/slide_content_writer.txt` | スライドごとの原稿を作成 | `{topic}`, `{audience}`, `{slide_info}` (構成情報), `{prev_content}` (文脈) |
| `prompts/visual_designer.txt` | 画像・グラフの提案 | `{slide_text}` (原稿), `{slide_type}` (レイアウト) |

## 3. 運用・移植ガイド

他のPCや環境でこのフォーマットを利用する場合、以下の手順に従ってください。

### 必須環境
*   Python 3.9+
*   Google Gemini API Key (`GEMINI_API_KEY`)
*   PowerPointテンプレート (`JMDC2022_16対9(標準)_v1.1.pptx`)
*   フォント: **Noto Sans CJK JP** (システムにインストールされていること)

### 実行フロー
1.  **環境変数の設定**:
    ```bash
    export GEMINI_API_KEY="your_api_key"
    ```
2.  **生成スクリプトの実行**:
    ```bash
    python3 scripts/proposal_generator.py --topic "新規事業案" --audience "経営会議"
    ```
3.  **スライド変換**:
    ```bash
    python3 scripts/generate_slide.py proposal.json output/result.pptx
    ```

### プロンプトの調整（カスタマイズ）
文体やフォーマットを変更したい場合は、`prompts/` フォルダ内のテキストファイルを編集してください。Pythonコードを変更する必要はありません。

*   **もっとカジュアルにしたい場合**: `slide_content_writer.txt` の指示に「親しみやすいトーンで」と追加。
*   **グラフを増やしたい場合**: `visual_designer.txt` の指示で「数値を積極的にグラフ化するよう」強調。

## 4. コンテキストの維持
「同じコンテキストで扱う」ために、`scripts/proposal_generator.py` では `prev_content_summary` という変数を使い、前のスライドの内容を次のスライドの生成プロンプトに渡しています。これにより、プレゼンテーション全体の一貫性（ストーリーフロー）が保たれます。

他の言語モデル（GPT-4など）に移植する場合も、この「前のスライドの内容を入力に含める」というロジックを維持することが重要です。
