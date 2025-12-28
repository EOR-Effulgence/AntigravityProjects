from datetime import datetime
from pptx.dml.color import RGBColor
from enum import Enum

class JMDCFont:
    REGULAR = "Noto Sans CJK JP Regular" # Deduced from Rulebook
    BOLD = "Noto Sans CJK JP Bold"     # Assumed partner font
    # Fallback to standard if needed
    DEFAULT = "MSGothic" 

class JMDCColor:
    # Approximate JMDC Brand Colors (to be verified)
    PRIMARY = RGBColor(0, 51, 102) # Dark Blue example
    TEXT_MAIN = RGBColor(51, 51, 51) # Dark Grey
    ACCENT = RGBColor(255, 102, 0)   # Orange example

class TextStyle(Enum):
    TITLE_MAIN = "title_main"
    TITLE_SLIDE = "title_slide"
    SUBTITLE = "subtitle"
    BODY = "body"
    CAPTION = "caption"

class StyleConfig:
    @staticmethod
    def get_font_style(style_type: TextStyle):
        """
        Returns a dict of font properties for a given usage context.
        """
        base = {
            "name": JMDCFont.REGULAR,
            "color": JMDCColor.TEXT_MAIN,
            "bold": False,
            "italic": False,
            "size": 18 # pt default
        }
        
        if style_type == TextStyle.TITLE_MAIN:
            base["size"] = 32
            base["bold"] = True
            base["color"] = JMDCColor.PRIMARY
            
        elif style_type == TextStyle.TITLE_SLIDE:
            base["size"] = 24
            base["bold"] = True
            base["color"] = JMDCColor.PRIMARY
            
        elif style_type == TextStyle.SUBTITLE:
            base["size"] = 14
            base["name"] = JMDCFont.BOLD
            
        elif style_type == TextStyle.BODY:
            base["size"] = 14 # 14pt seems standard for high density slides

        return base
