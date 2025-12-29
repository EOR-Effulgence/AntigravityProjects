import os
from pypdf import PdfReader
from typing import List

class PdfToMarkdownConverter:
    def convert(self, pdf_path: str) -> str:
        """
        Converts a PDF file to a Markdown string compatible with the slide parser.
        
        Strategy:
        - Each page becomes a slide.
        - First non-empty line is treated as Title.
        - Second non-empty line (if short) is treated as Subtitle.
        - Remaining text is Body.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        reader = PdfReader(pdf_path)
        md_output = []

        # Add initial layout comment for the first slide (usually Cover is better manually set, but logic here helps)
        # md_output.append("<!-- layout: 表紙 -->")
        # We'll default everything to Content layout for now, or let the parser default take over.

        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if not text.strip():
                continue
            
            lines = [l.strip() for l in text.split('\n') if l.strip()]
            
            if not lines:
                continue

            # Slide delimiter
            if i > 0:
                md_output.append("\n---\n")
            
            # Simple Heuristic
            # Line 1: Title
            title = lines[0]
            
            # Line 2: Subtitle? (If short and verified not to be a long sentence)
            subtitle = None
            body_start_idx = 1
            
            if len(lines) > 1:
                potential_subtitle = lines[1]
                if len(potential_subtitle) < 50: # Arbitrary threshold
                    subtitle = potential_subtitle
                    body_start_idx = 2
            
            # Layout determination (Naive)
            # If it's the first page, assume Cover
            layout = "コンテンツ"
            if i == 0:
                layout = "表紙"
                md_output.append(f"<!-- layout: {layout} -->")
            else:
                md_output.append(f"<!-- layout: {layout} -->")
            
            # Construct MD
            md_output.append(f"# {title}")
            if subtitle:
                md_output.append(f"## {subtitle}")
            
            md_output.append("") # Spacer
            
            # Body
            for line in lines[body_start_idx:]:
                # Check for list-like items (starts with -, *, number)
                # If not, just append as text
                if line.startswith(('-', '*', '•')):
                     md_output.append(f"- {line.lstrip('-*• ')}")
                else:
                     md_output.append(line)
        
        return "\n".join(md_output)
