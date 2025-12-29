from src.schema.slide_schema import PresentationDeck, SlideContent, SlideType

class DeckToMarkdownConverter:
    def convert(self, deck: PresentationDeck) -> str:
        md_lines = []
        
        # Deck Title Metadata? 
        # md_lines.append(f"<!-- deck: {deck.title} -->")
        
        for i, slide in enumerate(deck.slides):
            if i > 0:
                md_lines.append("\n---\n")
            
            # Layout Comment
            layout_name = self._map_type_to_layout_name(slide.type)
            md_lines.append(f"<!-- layout: {layout_name} -->")
            
            # Title
            if slide.title:
                md_lines.append(f"# {slide.title}")
            
            # Subtitle
            if slide.subtitle:
                md_lines.append(f"## {slide.subtitle}")
            
            md_lines.append("")
            
            # Body (if exists)
            if slide.body:
                md_lines.append(slide.body)
                md_lines.append("")

            # Advanced Elements (Absolute Positioning)
            # Syntax: <!-- element: type=text, rect=[x,y,w,h], size=12, color=[r,g,b] -->
            if slide.elements:
                for elem in slide.elements:
                    rect_str = f"[{elem.rect[0]:.4f}, {elem.rect[1]:.4f}, {elem.rect[2]:.4f}, {elem.rect[3]:.4f}]" if elem.rect else "[]"
                    
                    params = [f"type={elem.type}", f"rect={rect_str}"]
                    if elem.font_size:
                        params.append(f"size={elem.font_size:.1f}")
                    if elem.color:
                        params.append(f"color={elem.color}")
                    
                    param_str = ", ".join(params)
                    md_lines.append(f"<!-- element: {param_str} -->")
                    
                    if elem.type == "text":
                        md_lines.append(elem.content if elem.content else "")
                    elif elem.type == "image":
                        md_lines.append(f"![]({elem.content})")
                    
                    md_lines.append("")
        
        return "\n".join(md_lines)

    def _map_type_to_layout_name(self, slide_type: SlideType) -> str:
        # Inverse mapping of MD Parser
        mapping = {
            SlideType.COVER: "表紙",
            SlideType.TOC: "目次",
            SlideType.SECTION: "中見出し",
            SlideType.CONTENT: "コンテンツ",
            SlideType.BACK_COVER: "裏表紙"
        }
        return mapping.get(slide_type, "コンテンツ")
