import re
import sys
import os
from pathlib import Path
from typing import List, Dict, Any

# Adjust path to include src if running from root
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from src.schema.slide_schema import PresentationDeck, SlideContent, SlideType, ChartData, ChartType, SlideElement

class MarkdownParser:
    def parse(self, md_text: str) -> PresentationDeck:
        """MarkdownテキストをパースしてPresentationDeckを返す"""
        
        # スライド区切り (---) で分割
        slide_blocks = re.split(r'^---+\s*$', md_text, flags=re.MULTILINE)
        
        slides: List[SlideContent] = []
        deck_title = "Untitled Presentation"
        
        for i, block in enumerate(slide_blocks):
            if not block.strip():
                continue
                
            slide = self._parse_slide_block(block)
            slides.append(slide)
            
            # Use the title of the first slide (usually Cover) as the deck title
            if i == 0 and slide.title:
                deck_title = slide.title
        
        return PresentationDeck(title=deck_title, slides=slides)

    def _parse_slide_block(self, block: str) -> SlideContent:
        lines = block.strip().split('\n')
        
        # Default values
        slide_type = SlideType.CONTENT
        title = None
        subtitle = None
        body_lines = []
        chart_data = None
        
        in_code_block = False
        code_block_content = []
        code_block_lang = ""
        
        elements = []
        current_element_params = None

        layout_map = {
            "表紙": SlideType.COVER,
            "目次": SlideType.TOC,
            "中見出し": SlideType.SECTION,
            "コンテンツ": SlideType.CONTENT,
            "裏表紙": SlideType.BACK_COVER
        }

        for line in lines:
            line = line.strip()
            
            # 1. レイアウト解析 (<!-- layout: XXX -->)
            layout_match = re.match(r'<!--\s*layout:\s*(.+?)\s*-->', line)
            if layout_match:
                layout_name = layout_match.group(1).strip()
                slide_type = layout_map.get(layout_name, SlideType.CONTENT)
                continue
            
            # Skip other comments
            if line.startswith('<!--'):
                continue

            # Code Block Handling (Charts)
            if line.startswith('```'):
                if in_code_block:
                    # End of block
                    in_code_block = False
                    if code_block_lang.startswith('chart:'):
                       chart_data = self._parse_chart_block(code_block_lang, code_block_content)
                    # Reset
                    code_block_content = []
                    code_block_lang = ""
                else:
                    # Start of block
                    in_code_block = True
                    code_block_lang = line.replace('```', '').strip()
                continue
            
            if in_code_block:
                code_block_content.append(line)
                continue

            # Title Parsing (# )
            if not title and line.startswith('# '):
                title = line.replace('# ', '').strip()
                continue
            
            # Subtitle Parsing (## )
            if not subtitle and line.startswith('## '):
                subtitle = line.replace('## ', '').strip()
                continue
            
            # Custom Element Parsing
            # Syntax: <!-- element: type=text, rect=[0.1, 0.2, 0.3, 0.4], size=12, color=[0,0,0] -->
            element_match = re.match(r'<!--\s*element:\s*(.+?)\s*-->', line)
            if element_match:
                param_str = element_match.group(1).strip()
                # Parse params (naive split by comma, careful with lists)
                # Let's simple regex for rect
                params = {}
                
                type_match = re.search(r'type=(\w+)', param_str)
                if type_match: params['type'] = type_match.group(1)
                
                rect_match = re.search(r'rect=\[([\d\.\s,]+)\]', param_str)
                if rect_match:
                   rect_vals = [float(x) for x in rect_match.group(1).split(',')]
                   params['rect'] = rect_vals
                   
                size_match = re.search(r'size=([\d\.]+)', param_str)
                if size_match: params['size'] = float(size_match.group(1))
                
                color_match = re.search(r'color=\[([\d\.\s,]+)\]', param_str)
                if color_match:
                   color_vals = [int(x) for x in color_match.group(1).split(',')]
                   params['color'] = color_vals
                   
                # Mark upcoming lines as content for this element until empty line
                current_element_params = params
                continue
            
            # If we are inside an element context (capturing multiline content?)
            # Simplifying assumption: Element content is the next non-empty line(s)
            # Actually, let's treat the *next* line as content if type=text/image
            
            if current_element_params:
                content_val = line
                if current_element_params.get("type") == "image":
                     # Strip markdown image syntax if present
                     img_m = re.match(r'!\[.*?\]\((.*?)\)', line)
                     if img_m:
                         content_val = img_m.group(1)

                elements.append(SlideElement(
                    type=current_element_params.get("type", "text"),
                    content=content_val,
                    rect=current_element_params.get("rect"),
                    font_size=current_element_params.get("size"),
                    color=current_element_params.get("color")
                ))
                current_element_params = None # Reset
                continue

            # Regular Body Text
            if line:
                body_lines.append(line)

        # Assemble SlideContent
        return SlideContent(
            type=slide_type,
            title=title,
            subtitle=subtitle,
            body="\n".join(body_lines) if body_lines else None,
            chart=chart_data,
            elements=elements
        )

    def _parse_chart_block(self, lang_tag: str, content_lines: List[str]) -> ChartData:
        """
        Parses a chart block. 
        Format:
        Title
        Category, Series1, Series2
        Cat1, Val1, Val2
        """
        chart_type_str = lang_tag.split(':')[1].lower()
        
        # Map to Enum
        type_map = {
            "bar": ChartType.BAR_CLUSTERED,
            "column": ChartType.COLUMN_CLUSTERED,
            "line": ChartType.LINE,
            "pie": ChartType.PIE
        }
        chart_type = type_map.get(chart_type_str, ChartType.COLUMN_CLUSTERED)
        
        # Parse CSV-like content
        # Line 0: Title
        # Line 1: Header (Category Name, Series Names...)
        # Line 2+: Data
        
        if not content_lines:
            return None
            
        title = content_lines[0].strip()
        if len(content_lines) < 3:
            return ChartData(type=chart_type, title=title, categories=[], series={})

        header = [x.strip() for x in content_lines[1].split(',')]
        # series_names = header[1:] 
        
        categories = []
        series_data = {name: [] for name in header[1:]}
        
        for row_str in content_lines[2:]:
            row = [x.strip() for x in row_str.split(',')]
            if len(row) < len(header):
                continue
            
            categories.append(row[0])
            for i, val in enumerate(row[1:]):
                series_name = header[i+1]
                try:
                    series_data[series_name].append(float(val))
                except ValueError:
                     series_data[series_name].append(0.0)

        return ChartData(
            title=title,
            type=chart_type,
            categories=categories,
            series=series_data
        )
