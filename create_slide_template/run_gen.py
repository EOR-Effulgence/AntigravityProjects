#!/usr/bin/env python3
import sys
import argparse
from pathlib import Path

# Add src to path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir / "src"))

from builder.slide_builder import SlideBuilder
# We need the markdown parser logic. 
# For now, I'll basically copy the parse_markdown logic from the old script to a new parser module.

from markdown_parser.md_parser import parse_markdown

def main():
    parser = argparse.ArgumentParser(description="Convert Markdown proposal to PPTX (Refactored)")
    parser.add_argument("input_md", help="Input Markdown file")
    parser.add_argument("output_pptx", help="Output PPTX file")
    parser.add_argument("--config", default="config/settings.yaml", help="Path to config file")

    args = parser.parse_args()

    # Read MD
    with open(args.input_md, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # Parse
    slide_data = parse_markdown(md_text)

    # Build
    builder = SlideBuilder(config_path=args.config, project_root=current_dir)
    builder.build(slide_data, args.output_pptx)

if __name__ == "__main__":
    main()
