#!/usr/bin/env python3
"""
Markdown (proposal.md) を解析して PPTX を生成するスクリプト
"""
import sys
import re
import os
from pathlib import Path
import json

# アドホックにパスを通して既存モジュールを再利用
sys.path.append(str(Path(__file__).parent))
import generate_slide
import chart_utils

def parse_markdown(md_text: str) -> dict:
    """Markdownテキストをパースして中間JSON形式にする"""
    
    # スライド区切り (---) で分割
    slide_blocks = re.split(r'^---+\s*$', md_text, flags=re.MULTILINE)
    
    slides_data = []
    
    for block in slide_blocks:
        if not block.strip():
            continue
            
        slide = {
            "layout": "コンテンツ", # デフォルト
            "title": "",
            "body": "",
            "content": [],
            "charts": [],
            "images": []
        }
        
        lines = block.strip().split('\n')
        
        # 1. レイアウト解析 (<!-- layout: XXX -->)
        layout_match = re.search(r'<!--\s*layout:\s*(.+?)\s*-->', block)
        if layout_match:
            slide["layout"] = layout_match.group(1).strip()
            
        # 2. タイトル解析 (# Title)
        # 最初の H1 をタイトルとする
        title_found = False
        body_lines = []
        
        # 行ごとの解析
        in_code_block = False
        code_block_content = []
        code_block_lang = ""
        
        for line in lines:
            # マジックコメントはスキップ
            if re.match(r'<!--\s*layout:', line):
                continue
                
            # コードブロック処理
            if line.strip().startswith('```'):
                if in_code_block:
                    # ブロック終了
                    in_code_block = False
                    
                    # チャートブロックの処理
                    if code_block_lang.startswith('chart:'):
                        chart_type = code_block_lang.split(':')[1]
                        chart_text = "\n".join(code_block_content)
                        
                        # タイトル抽出 (最初の行をタイトルと見なす簡易ロジック)
                        chart_lines = chart_text.strip().split('\n')
                        chart_title = ""
                        csv_content = chart_text
                        
                        if chart_lines and ',' not in chart_lines[0]:
                             chart_title = chart_lines[0]
                             csv_content = "\n".join(chart_lines[1:])
                        
                        parsed_data = chart_utils.parse_chart_data_from_csv(csv_content)
                        if parsed_data:
                            slide["charts"].append({
                                "type": chart_type.upper(),
                                "title": chart_title,
                                "data": parsed_data,
                                "position": {"left": 7.0, "top": 2.0, "width": 6.0, "height": 4.0} # デフォルト位置
                            })
                    
                    code_block_content = []
                    code_block_lang = ""
                else:
                    # ブロック開始
                    in_code_block = True
                    code_block_lang = line.strip().replace('```', '')
                continue
            
            if in_code_block:
                code_block_content.append(line)
                continue

            # タイトル解析
            if not title_found and line.strip().startswith('# '):
                slide["title"] = line.strip().replace('# ', '')
                title_found = True
                continue
            
            # サブタイトル解析 (## ) -> 表紙や中見出し用
            if line.strip().startswith('## '):
                slide["subtitle"] = line.strip().replace('## ', '')
                continue

            # 画像 (Markdown記法)
            img_match = re.search(r'!\[(.*?)\]\((.*?)\)', line)
            if img_match:
                slide["images"].append({
                    "path": img_match.group(2),
                    "prompt": img_match.group(1), # alt textをプロンプト代わりに
                    "position": {"left": 7.0, "top": 2.0, "width": 6.0, "height": 4.0}
                })
                continue
                
            # 通常の本文
            if line.strip():
                body_lines.append(line)
        
        # 本文の整形
        slide["body"] = "\n".join(body_lines)
        # リスト項目の抽出（簡易）
        slide["content"] = [l.replace('* ', '').replace('- ', '').strip() for l in body_lines if l.strip().startswith(('*', '-'))]
        
        slides_data.append(slide)
        
    return {"slides": slides_data, "clear_existing": True}

def main():
    if len(sys.argv) < 3:
        print("Usage: python md_to_slide.py <input.md> <output.pptx>")
        sys.exit(1)
        
    input_md = sys.argv[1]
    output_pptx = sys.argv[2]
    
    with open(input_md, 'r', encoding='utf-8') as f:
        md_text = f.read()
        
    slide_data = parse_markdown(md_text)
    
    # 既存の generate_slide ロジックを流用
    # パス設定の解決
    script_dir = Path(__file__).parent.parent
    template_path = script_dir / "JMDC2022_16対9(標準)_v1.1.pptx"
    mapping_path = script_dir / "config" / "layout_mapping.json"
    
    # 出力ディレクトリ作成
    Path(output_pptx).parent.mkdir(parents=True, exist_ok=True)
    
    generate_slide.create_presentation(str(template_path), slide_data, output_pptx, str(mapping_path))

if __name__ == "__main__":
    main()
