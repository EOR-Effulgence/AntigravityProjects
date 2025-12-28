import os
import sys
import argparse

# Adjust path to include src to allow running from root
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.markdown_parser.md_parser import MarkdownParser
from src.builder.slide_builder import SlideBuilder

def main():
    parser = argparse.ArgumentParser(description="Generate PowerPoint proposal from Markdown.")
    parser.add_argument("input_file", help="Path to input Markdown file")
    parser.add_argument("--template", help="Path to PowerPoint template", 
                        default="/Users/hiratani/Documents/AntigravityProjects/original_templates/JMDC2022_16対9(標準)_基本テンプレ_v1.2.pptx")
    parser.add_argument("--output", help="Output file path", default="output/proposal.pptx")
    
    args = parser.parse_args()

    # 1. Parse Markdown
    print(f"Parsing {args.input_file}...")
    if not os.path.exists(args.input_file):
        print(f"Error: Input file not found: {args.input_file}")
        return

    with open(args.input_file, "r", encoding="utf-8") as f:
        md_text = f.read()
    
    md_parser = MarkdownParser()
    deck = md_parser.parse(md_text)
    print(f"Parsed {len(deck.slides)} slides. Deck Title: {deck.title}")

    # 2. Build Presentation
    print(f"Building presentation using template: {os.path.basename(args.template)}...")
    if not os.path.exists(args.template):
         print(f"Error: Template file not found: {args.template}")
         return

    # Ensure output directory exists
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    builder = SlideBuilder(args.template)
    builder.build(deck, args.output)
    
    print(f"Success! Presentation saved to {args.output}")

if __name__ == "__main__":
    main()
