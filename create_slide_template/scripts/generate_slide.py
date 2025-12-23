#!/usr/bin/env python3
"""
JMDCテンプレートを使用してPowerPointスライドを生成するスクリプト
"""

import json
import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor


def load_slide_data(json_path: str) -> dict:
    """JSONファイルからスライドデータを読み込む"""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_mapping(config_path: str) -> dict:
    """レイアウトマッピング設定を読み込む"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def create_presentation(template_path: str, slide_data: dict, output_path: str, mapping_path: str):
    """
    テンプレートを使用してプレゼンテーションを作成
    """
    prs = Presentation(template_path)
    mapping_config = load_mapping(mapping_path)
    layout_mapping = mapping_config["layouts"]
    
    # テンプレートのレイアウト名とインデックスのマッピング
    ppt_layout_indices = {}
    for idx, layout in enumerate(prs.slide_masters[0].slide_layouts):
        ppt_layout_indices[layout.name] = idx
    
    print(f"テンプレート内のレイアウト: {list(ppt_layout_indices.keys())}")
    
    # 既存のサンプルスライドを削除
    if slide_data.get("clear_existing", False):
        while len(prs.slides) > 0:
            rId = prs.slides._sldIdLst[0].rId
            prs.part.drop_rel(rId)
            del prs.slides._sldIdLst[0]
    
    # 新しいスライドを追加
    for i, slide_info in enumerate(slide_data.get("slides", [])):
        layout_name = slide_info.get("layout", "コンテンツ")
        
        # マッピング定義にあるレイアウトか確認
        if layout_name not in layout_mapping:
            print(f"警告: マッピング定義にないレイアウト '{layout_name}' です。スキップします。")
            continue
            
        # テンプレートに存在するレイアウトか確認
        if layout_name not in ppt_layout_indices:
            print(f"警告: テンプレートにレイアウト '{layout_name}' が見つかりません。")
            continue
        
        # スライド追加
        layout_idx = ppt_layout_indices[layout_name]
        layout = prs.slide_masters[0].slide_layouts[layout_idx]
        slide = prs.slides.add_slide(layout)
        
        # マッピング定義に基づいてコンテンツを設定
        ph_map = layout_mapping[layout_name]
        
        for field, config in ph_map.items():
            if field == "description": continue
            
            target_idx = config["idx"]
            
            # 入力データにそのフィールドの値があるか確認
            # slide_info = {"layout": "...", "title": "...", "content": [...]}
            # field = "title" or "content" etc.
            
            # 特別対応: bodyとcontentは相互に融通を利かせる（入力JSONのゆらぎ吸収）
            content_value = slide_info.get(field)
            if content_value is None:
                if field == "content" and "body" in slide_info:
                    content_value = slide_info["body"]
                elif field == "body" and "content" in slide_info:
                    content_value = slide_info["content"]
            
            if content_value:
                # 該当するインデックスのプレースホルダーを探す
                try:
                    shape = slide.placeholders[target_idx]
                    
                    if isinstance(content_value, list):
                        # リスト形式のコンテンツ
                        tf = shape.text_frame
                        tf.clear()
                        for i, item in enumerate(content_value):
                            if i == 0:
                                tf.paragraphs[0].text = item
                            else:
                                p = tf.add_paragraph()
                                p.text = item
                                p.level = 0
                    else:
                        # テキスト形式
                        shape.text = str(content_value)
                        
                except KeyError:
                    print(f"警告: スライド[{i}] '{layout_name}' のプレースホルダー idx={target_idx} ({field}) が見つかりません。")
        
        print(f"スライド追加: {layout_name} - {slide_info.get('title', 'No Title')}")
    
    # 保存
    prs.save(output_path)
    print(f"\nプレゼンテーションを保存しました: {output_path}")


def main():
    if len(sys.argv) < 3:
        print("使用方法: python generate_slide.py <input.json> <output.pptx>")
        sys.exit(1)
    
    input_json = sys.argv[1]
    output_pptx = sys.argv[2]
    
    # パス設定
    script_dir = Path(__file__).parent.parent
    template_path = script_dir / "JMDC2022_16対9(標準)_v1.1.pptx"
    mapping_path = script_dir / "config" / "layout_mapping.json"
    
    slide_data = load_slide_data(input_json)
    create_presentation(str(template_path), slide_data, output_pptx, str(mapping_path))


if __name__ == "__main__":
    main()
