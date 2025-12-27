# Proposal Generation System Walkthrough (Diagram Support)

## Overview
We added **Native Diagram Generation** to support flowcharts and process diagrams.
Users can define diagrams in Markdown using `diagram:type` blocks.

## New Syntax
```markdown
```diagram:process
Step 1: Planning
Step 2: Execution
```
```

## Supported Types
1.  **Process** (`diagram:process`): Linear flow (left to right) with arrows.
2.  **Cycle** (`diagram:cycle`): Circular arrangement.
3.  **List** (`diagram:list`): Simple boxed list (fallback for generic types).

## Verification
We generated [`output/diagram_test.pptx`](file:///Users/hiratani/Documents/AntigravityProjects/create_slide_template/output/diagram_test.pptx) from `sample_proposal.md`.
- **Result**: The slide "フロー図の自動生成デモ" contains:
    - A 4-step process flow (Rounded Rectangles with Arrows).
    - A 4-step cycle flow (Circular Ovals).
- All shapes are native PowerPoint shapes and can be edited, resized, or recolored by the user.
- Colors are applied from the global palette in `settings.yaml`.
