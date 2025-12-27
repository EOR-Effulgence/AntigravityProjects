import json
import os
import sys
import yaml
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
# from pptx.enum.lang import MSO_LANGUAGE_ID # 必要なら

# Import utils
sys.path.append(str(Path(__file__).parent.parent))
from utils import chart_utils, image_utils, diagram_utils

class SlideBuilder:
    def __init__(self, config_path="config/settings.yaml", project_root=None):
        self.project_root = Path(project_root) if project_root else Path(os.getcwd())
        self.config = self._load_config(config_path)
        self.layout_mapping = self._load_mapping()
        self.font_name = self.config.get("design", {}).get("font", {}).get("name", "Noto Sans CJK JP")
        self.palette = self.config.get("design", {}).get("colors", {}).get("palette", [])
        
    def _load_config(self, path_str):
        full_path = self.project_root / path_str
        with open(full_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _load_mapping(self):
        mapping_rel = self.config["paths"]["layout_mapping"]
        full_path = self.project_root / mapping_rel
        with open(full_path, 'r', encoding='utf-8') as f:
            return json.load(f)["layouts"]

    def build(self, slide_data: dict, output_path: str):
        template_rel = self.config["paths"]["template_file"]
        template_path = self.project_root / template_rel
        
        prs = Presentation(str(template_path))
        
        # Mapping layout names to indices
        ppt_layout_indices = {}
        for idx, layout in enumerate(prs.slide_masters[0].slide_layouts):
            ppt_layout_indices[layout.name] = idx
            
        # Clear existing keys if requested
        if slide_data.get("clear_existing", False):
             self._clear_slides(prs)

        # Add slides
        for i, slide_info in enumerate(slide_data.get("slides", [])):
            self._add_single_slide(prs, slide_info, ppt_layout_indices)
            
        # Save
        # Make sure directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        prs.save(output_path)
        print(f"Presentation saved: {output_path}")

    def _clear_slides(self, prs):
         # xml_slides = prs.slides._sldIdLst
         # slides = list(xml_slides)
         # for slide in slides:
         #    prs.slides._sldIdLst.remove(slide)
         while len(prs.slides) > 0:
            rId = prs.slides._sldIdLst[0].rId
            prs.part.drop_rel(rId)
            del prs.slides._sldIdLst[0]

    def _add_single_slide(self, prs, slide_info, layout_indices):
        layout_name = slide_info.get("layout", "コンテンツ")
        
        if layout_name not in self.layout_mapping:
            print(f"Warning: Unknown layout mapping '{layout_name}'. Skipping.")
            return

        if layout_name not in layout_indices:
             print(f"Warning: Layout '{layout_name}' not found in template.")
             return

        layout_idx = layout_indices[layout_name]
        layout = prs.slide_masters[0].slide_layouts[layout_idx]
        slide = prs.slides.add_slide(layout)
        
        ph_map = self.layout_mapping[layout_name]
        
        # Text Content
        for field, config in ph_map.items():
            if field == "description": continue
            target_idx = config["idx"]
            
            # Resolve content
            content_value = slide_info.get(field)
            if content_value is None:
                 if field == "content" and "body" in slide_info: content_value = slide_info["body"]
                 elif field == "body" and "content" in slide_info: content_value = slide_info["content"]

            if content_value:
                self._set_placeholder_content(slide, target_idx, content_value)

        # Charts
        if "charts" in slide_info:
            for chart_info in slide_info["charts"]:
                try:
                    chart_utils.add_chart_to_slide(slide, chart_info, colors=self.palette)
                except Exception as e:
                    print(f"Error adding chart: {e}")

        # Images
        if "images" in slide_info:
            for image_info in slide_info["images"]:
                try:
                    image_utils.add_image_to_slide(slide, image_info)
                except Exception as e:
                    print(f"Error adding image: {e}")

        # Diagrams (New)
        if "diagrams" in slide_info:
             for diag_info in slide_info["diagrams"]:
                 try:
                     diagram_utils.create_diagram(slide, diag_info, colors=self.palette)
                 except Exception as e:
                     print(f"Error adding diagram: {e}")

    def _set_placeholder_content(self, slide, idx, content):
        try:
            shape = slide.placeholders[idx]
            text_frame = shape.text_frame
            text_frame.clear() # clear existing
            
            if isinstance(content, list):
                for i, item in enumerate(content):
                    p = text_frame.paragraphs[0] if i == 0 else text_frame.add_paragraph()
                    p.text = item
                    p.level = 0
                    self._apply_font(p)
            else:
                shape.text = str(content)
                for p in text_frame.paragraphs:
                    self._apply_font(p)

        except KeyError:
            pass # Placeholder not found

    def _apply_font(self, paragraph):
        # Apply font to paragraph and runs
        paragraph.font.name = self.font_name
        if paragraph.runs:
            for run in paragraph.runs:
                run.font.name = self.font_name
