import os
import sys
import argparse

# Adjust path to include src
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.converters.pdf_intelligent import IntelligentPdfParser
from src.converters.deck_to_md import DeckToMarkdownConverter
from src.markdown_parser.md_parser import MarkdownParser
from src.builder.slide_builder import SlideBuilder

def main():
    parser = argparse.ArgumentParser(description="Convert PDF to JMDC PowerPoint Template via Intermediate Markdown.")
    parser.add_argument("input_pdf", help="Path to input PDF file")
    parser.add_argument("--output", help="Output PPTX path", default="output/converted_from_pdf.pptx")
    parser.add_argument("--template", help="Path to PowerPoint template", 
                        default="/Users/hiratani/Documents/AntigravityProjects/original_templates/JMDC2022_16対9(標準)_基本テンプレ_v1.2.pptx")
    parser.add_argument("--intermediate", help="Intermediate Markdown path", default=None)
    parser.add_argument("--only-extract", action="store_true", help="Stop after generating intermediate Markdown (for manual editing)")

    args = parser.parse_args()

    # Determine paths
    if not args.intermediate:
        base_name = os.path.splitext(os.path.basename(args.input_pdf))[0]
        output_dir = os.path.dirname(args.output)
        if not output_dir: output_dir = "."
        args.intermediate = os.path.join(output_dir, f"{base_name}_intermediate.md")

    # 1. Parse PDF intelligently
    print(f"Reading PDF: {args.input_pdf}")
    if not os.path.exists(args.input_pdf):
        print(f"Error: Input file not found: {args.input_pdf}")
        return

    # Use Intelligent Parser which returns PresentationDeck directly
    pdf_parser = IntelligentPdfParser()
    try:
        # Images go next to intermediate MD
        image_dir = os.path.join(os.path.dirname(args.intermediate), "extracted_images")
        deck = pdf_parser.parse(args.input_pdf, output_image_dir=image_dir)
        print(f"PDF Analysis successful. Identified {len(deck.slides)} slides.")
    except Exception as e:
        print(f"Error converting PDF: {e}")
        import traceback
        traceback.print_exc()
        return

    # 2. Serialize to Intermediate Markdown
    print(f"Saving intermediate Markdown to {args.intermediate}...")
    serializer = DeckToMarkdownConverter()
    md_content = serializer.convert(deck)
    
    # Ensure dir exists
    int_dir = os.path.dirname(args.intermediate)
    if int_dir and not os.path.exists(int_dir):
        os.makedirs(int_dir)
        
    with open(args.intermediate, "w", encoding="utf-8") as f:
        f.write(md_content)
    
    print("Intermediate Markdown saved. You can edit this file now.")
    
    if args.only_extract:
        print("Extraction complete. Exiting as requested.")
        return

    # 3. Read back Markdown
    # In a real workflow, this might be a separate step/script run by the user.
    # For now, we proceed automatically to demonstrate validity.
    print("Reading back Markdown content...")
    with open(args.intermediate, "r", encoding="utf-8") as f:
        final_md_text = f.read()
    
    md_parser = MarkdownParser()
    final_deck = md_parser.parse(final_md_text)

    # 4. Build PowerPoint
    print(f"Generating PowerPoint using template...")
    if not os.path.exists(args.template):
         print(f"Error: Template file not found: {args.template}")
         return
         
    builder = SlideBuilder(args.template)
    builder.build(final_deck, args.output)
    
    print(f"Success! Saved to {args.output}")

if __name__ == "__main__":
    main()
