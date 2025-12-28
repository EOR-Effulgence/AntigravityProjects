from enum import Enum
from typing import List, Optional, Union, Dict, Any
from pydantic import BaseModel, Field

class SlideType(str, Enum):
    COVER = "cover"
    TOC = "toc"
    SECTION = "section"
    CONTENT = "content"
    BACK_COVER = "back_cover"

class ChartType(str, Enum):
    BAR_CLUSTERED = "bar_clustered"
    COLUMN_CLUSTERED = "column_clustered"
    LINE = "line"
    PIE = "pie"

class ChartData(BaseModel):
    title: Optional[str] = None
    type: ChartType
    categories: List[str] # X-axis labels (e.g., ["Q1", "Q2", "Q3", "Q4"])
    series: Dict[str, List[float]] # Series Name -> Data Points (e.g., {"Revenue": [10, 20, 30, 40]})

class SlideContent(BaseModel):
    """
    Generic content model for a slide.
    Different slide types will use different subsets of these fields.
    """
    type: SlideType
    title: Optional[str] = None
    subtitle: Optional[str] = None
    body: Optional[str] = None # Markdown or plain text
    bullets: Optional[List[str]] = None
    image_path: Optional[str] = None
    chart: Optional[ChartData] = None
    footer: Optional[str] = None
    
    # Metadata for specific template mapping if needed
    layout_index: Optional[int] = None 

class PresentationDeck(BaseModel):
    title: str
    author: Optional[str] = None
    date: Optional[str] = None
    slides: List[SlideContent] = []
