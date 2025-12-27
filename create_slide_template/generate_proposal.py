#!/usr/bin/env python3
"""
Proposal AI Generator (Markdown Version)
Multi-agent system to create a slide proposal in Markdown format and convert to PPTX.
"""
import os
import sys
import argparse
import time
import re
from pathlib import Path
import google.generativeai as genai
import subprocess

# Setup paths (Running from root)
PROJECT_ROOT = Path(__file__).parent.absolute()
PROMPTS_DIR = PROJECT_ROOT / "prompts"

def load_prompt(name):
    with open(PROMPTS_DIR / f"{name}.txt", "r", encoding="utf-8") as f:
        return f.read()

def call_gemini(prompt, model_name="gemini-1.5-pro", response_mime_type="text/plain"):
    """
    Calls Gemini API and returns the response text.
    Markdown output requires text/plain (default).
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("エラー: GEMINI_API_KEY が見つかりません。環境変数を設定してください。")
        sys.exit(1)
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    
    generation_config = {
        "temperature": 0.7,
        "max_output_tokens": 8192,
    }
    
    if response_mime_type:
        generation_config["response_mime_type"] = response_mime_type

    try:
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        return response.text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return ""

def main():
    parser = argparse.ArgumentParser(description="Generate a proposal presentation with AI (Markdown flow).")
    parser.add_argument("--topic", required=True, help="Topic of the proposal")
    parser.add_argument("--audience", default="一般ビジネス層", help="Target audience")
    parser.add_argument("--slides", type=int, default=5, help="Approximate number of content slides")
    parser.add_argument("--output_md", default="proposal.md", help="Output Markdown file path")
    parser.add_argument("--output_pptx", default="output/proposal.pptx", help="Output PPTX file path")
    
    args = parser.parse_args()
    
    print(f"🚀 提案書生成を開始します (MDフロー): '{args.topic}'")
    
    # ---------------------------------------------------------
    # 1. Planner Agent (MD Outline)
    # ---------------------------------------------------------
    print("\n[1/2] 構成案を作成中...")
    planner_prompt_tmpl = load_prompt("proposal_planner")
    planner_prompt = planner_prompt_tmpl.replace("{topic}", args.topic) \
                                        .replace("{audience}", args.audience) \
                                        .replace("{num_slides}", str(args.slides))
    
    outline_md = call_gemini(planner_prompt)
    if not outline_md:
        print("構成案の生成に失敗しました。")
        sys.exit(1)

    # ---------------------------------------------------------
    # 2. Content Writer Agent (Iterative MD refinement)
    # ---------------------------------------------------------
    print("\n[2/2] 詳細コンテンツとグラフを生成中...")
    
    # スライドごとに分割して処理
    slide_blocks = re.split(r'^---+\s*$', outline_md, flags=re.MULTILINE)
    final_blocks = []
    
    writer_tmpl = load_prompt("slide_content_writer")
    prev_content_summary = ""
    
    for i, slide_block in enumerate(slide_blocks):
        if not slide_block.strip():
            continue
            
        print(f"  > スライド {i+1} を執筆中...")
        
        # 執筆
        writer_prompt = writer_tmpl.replace("{topic}", args.topic) \
                                   .replace("{audience}", args.audience) \
                                   .replace("{slide_md}", slide_block) \
                                   .replace("{prev_content}", prev_content_summary)
        
        refined_slide_md = call_gemini(writer_prompt)
        if not refined_slide_md:
            refined_slide_md = slide_block # 失敗時はそのまま使う
            
        final_blocks.append(refined_slide_md.strip())
        
        # 文脈更新（簡易的に先頭100文字などを記録）
        prev_content_summary += f"\n[Slide {i+1}] {refined_slide_md[:200]}..."
        
        time.sleep(1)

    # ---------------------------------------------------------
    # Finalize
    # ---------------------------------------------------------
    full_md = "\n\n---\n\n".join(final_blocks)
    
    # Save MD
    with open(args.output_md, "w", encoding="utf-8") as f:
        f.write(full_md)
        
    print(f"\nMarkdown提案書を保存しました: {args.output_md}")
    
    # Generate PPTX using run_gen.py
    print("PPTXへの変換を開始します...")
    cmd = [sys.executable, str(PROJECT_ROOT / "run_gen.py"), args.output_md, args.output_pptx]
    subprocess.run(cmd, check=True)
    
    print(f"完了しました: {args.output_pptx}")

if __name__ == "__main__":
    main()
