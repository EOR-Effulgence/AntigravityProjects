import os
import sys

# Adjust path to include src if running from root
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from src.schema.slide_schema import PresentationDeck, SlideContent, SlideType, ChartData, ChartType
from src.builder.slide_builder import SlideBuilder

def main():
    # 1. Prepare Data
    slides = [
        SlideContent(
            type=SlideType.COVER,
            title="自動生成プレゼンテーション",
            subtitle="JMDC Template Reproduction Test"
        ),
        SlideContent(
            type=SlideType.TOC,
            title="本日のアジェンダ",
            body="1. プロジェクト概要\n2. 技術的アプローチ\n3. 今後の計画\n4. Q&A"
        ),
        SlideContent(
            type=SlideType.SECTION,
            title="プロジェクト概要",
            subtitle="Background & Objectives"
        ),
        SlideContent(
            type=SlideType.CONTENT,
            title="技術的アプローチ",
            subtitle="Python-pptxによる自動化",
            body="本システムは、テンプレートの構造を解析し、中間スキーマ（Pydanticモデル）を介してPPTXを再構築します。\n\n- Template Analysis\n- Abstract Schema\n- Modular Builder"
        ),
        SlideContent(
            type=SlideType.CONTENT,
            title="成果物グラフ（サンプル）",
            subtitle="半期ごとの売上推移",
            chart=ChartData(
                title="Revenue Growth",
                type=ChartType.COLUMN_CLUSTERED,
                categories=["2024 H1", "2024 H2", "2025 H1", "2025 H2"],
                series={
                    "Japan": [100.0, 120.0, 150.0, 180.0],
                    "Global": [80.0, 90.0, 110.0, 140.0]
                }
            )
        ),
        SlideContent(
            type=SlideType.BACK_COVER
        )
    ]
    
    deck = PresentationDeck(
        title="Reproduction Test",
        slides=slides
    )

    # 2. Configure Paths
    template_path = "/Users/hiratani/Documents/AntigravityProjects/original_templates/JMDC2022_16対9(標準)_基本テンプレ_v1.2.pptx"
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_path = os.path.join(output_dir, "test_reproduction.pptx")

    # 3. Build Presentation
    print(f"Building presentation using template: {os.path.basename(template_path)}")
    builder = SlideBuilder(template_path)
    builder.build(deck, output_path)
    print("Done.")

if __name__ == "__main__":
    main()
