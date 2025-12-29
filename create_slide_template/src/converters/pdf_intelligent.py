import fitz  # PyMuPDF
import os
from typing import List, Dict, Tuple
from src.schema.slide_schema import PresentationDeck, SlideContent, SlideType, SlideElement

class IntelligentPdfParser:
    def parse(self, pdf_path: str, output_image_dir: str = "output/images") -> PresentationDeck:
        if not os.path.exists(pdf_path):
             raise FileNotFoundError(f"PDF not found: {pdf_path}")
        
        doc = fitz.open(pdf_path)
        slides = []
        
        if not os.path.exists(output_image_dir):
            os.makedirs(output_image_dir)

        print(f"Intelligent Parsing of {pdf_path} ({len(doc)} pages)...")
        
        for page_num, page in enumerate(doc):
            # 1. Analyze Layout (Text Blocks)
            # blocks = page.get_text("dict")["blocks"]
            text_blocks = page.get_text("blocks") # (x0, y0, x1, y1, "text", block_no, block_type)
            
            # Filter valid text blocks
            # block_type=0 is text, 1 is image
            
            # Identify Title (Topmost, largest font? - tough with "blocks", better with "dict")
            # Let's switch to "dict" for font size details
            page_dict = page.get_text("dict")
            
            elements = []
            title_candidate = None
            max_font_size = 0
            
            page_width = page.rect.width
            page_height = page.rect.height
            
            # --- Text Processing ---
            for block in page_dict["blocks"]:
                if block["type"] == 0: # Text
                    # Check lines/spans for font size
                    block_text = ""
                    block_font_size = 0
                    
                    for line in block["lines"]:
                        for span in line["spans"]:
                            if span["text"].strip():
                                block_text += span["text"]
                                # Initial font size of the block
                                if span["size"] > block_font_size:
                                    block_font_size = span["size"]
                    
                    if not block_text.strip():
                        continue
                        
                    # Normalize bbox
                    bbox = block["bbox"]
                    norm_rect = [
                        bbox[0] / page_width,
                        bbox[1] / page_height,
                        (bbox[2] - bbox[0]) / page_width,
                        (bbox[3] - bbox[1]) / page_height
                    ]
                    
                    # Heuristic for Title: Top 20% of page, large font
                    is_title = False
                    if norm_rect[1] < 0.2 and block_font_size > max_font_size:
                        max_font_size = block_font_size
                        title_candidate = block_text
                        is_title = True
                    
                    if not is_title:
                        elements.append(SlideElement(
                            type="text",
                            content=block_text,
                            rect=norm_rect,
                            font_size=block_font_size
                        ))

            # --- Image Extraction ---
            image_list = page.get_images(full=True)
            for img_idx, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                image_filename = f"im_p{page_num}_{img_idx}.{image_ext}"
                image_path = os.path.join(output_image_dir, image_filename)
                
                with open(image_path, "wb") as f:
                    f.write(image_bytes)
                
                # Try to find image location
                # get_images doesn't give location directly. 
                # We need to search for the image in the page's "image type" blocks or use get_image_rects
                image_rects = page.get_image_rects(xref)
                for rect in image_rects:
                    norm_rect = [
                        rect.x0 / page_width,
                        rect.y0 / page_height,
                        rect.width / page_width,
                        rect.height / page_height
                    ]
                    elements.append(SlideElement(
                        type="image",
                        content=image_path,
                        rect=norm_rect
                    ))

            # Construct Slide
            slide_type = SlideType.CONTENT
            if page_num == 0:
                slide_type = SlideType.COVER
                
            slides.append(SlideContent(
                type=slide_type,
                title=title_candidate if title_candidate else "No Title",
                elements=elements
            ))

        return PresentationDeck(title=os.path.basename(pdf_path), slides=slides)
