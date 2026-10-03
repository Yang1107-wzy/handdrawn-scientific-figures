# Exact composition and chart layers

Install the skill's own [runtime requirements](../requirements.txt) in your environment. This list is included in the installed folder and skill-only ZIP, so the repository checkout is not required. The skill folder includes all fonts/presets needed by its two helpers; scripts have no network or image-model dependency.

```sh
python -m pip install -r requirements.txt
python scripts/compose_figure.py figure.json --output-prefix output/figure
python scripts/chart_style.py --show
```

Run from the installed skill directory, or use the helper's full path. Image paths resolve relative to the JSON manifest. Output prefix has no extension. Existing outputs are preserved; use `--overwrite` only for the explicitly intended generated prefix. Source art is not modified.

## Manifest

Coordinates are millimetres; (0,0) is upper left. Font sizes and line widths are points. `profile` is `paper` or `ppt`. Defaults are defined in [style.json](../assets/style.json); optional width_mm, height_mm and dpi override them.

```json
{
  "profile": "paper",
  "layers": [
    {"type":"text","text":"A measured world","font":"title","font_size":16,"x":8,"y":7},
    {"type":"image","path":"scene.png","x":8,"y":22,"width":100,"height":66},
    {"type":"text","text":"Ground reference","font":"hand","font_size":10,"x":114,"y":33,"max_width":55},
    {"type":"arrow","points":[[113,43],[94,69]],"color":"#252525","line_width":0.9},
    {"type":"math","text":"h = z_{\\mathrm{top}} - z_{\\mathrm{floor}}","x":110,"y":73,"font_size":10}
  ]
}
```

Supported layers:

| Type | Fields |
|---|---|
| image | path, x, y, width, height; fits while preserving aspect |
| text | text, x, y, font: title/hand/body/bold, font_size, optional max_width/color |
| math | text in MathText-compatible LaTeX, x, y, font_size, optional color |
| arrow / line | points: ordered coordinate pairs; optional color/line_width |
| rect | x, y, width, height; optional fill/stroke/line_width/dash/rough |

Place decorative panels below their content in the ordered list. Decorative roughness does not apply to chart geometry. Unsupported math or missing art fails before outputs are written; it is not replaced with invented glyphs. The example `scene.png` is an input you supply.

## Exports

The helper emits PNG, PDF, SVG and a render-report JSON; PPT adds a one-slide PPTX. The report records text bounds, placed image resolution and canvas warnings. Check it and inspect the finished files. It is not a semantic reviewer and does not automatically prove arrows or labels are correct.

PDF uses embedded fonts and retains selectable authored text. SVG embeds image/font resources and retains text/vector connection layers; MathText formulas use glyph paths. Raster art stays raster. PPTX text and connections are editable, but fonts are referenced, not embedded. Install the bundled fonts on the presentation device. PPTX formulas are images; edit their MathText source in the JSON. Decorative rough rectangles become native straight rectangles in PPTX.

Graph text is normally English. A requested language outside the bundled fonts' coverage needs an appropriate licensed font preset; do not silently replace unsupported characters.

## Quantitative plots

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path("scripts").resolve()))
from chart_style import chart_context
import matplotlib.pyplot as plt

with chart_context():
    fig, ax = plt.subplots(figsize=(3.2, 2.2))
    ax.plot(sample_time, supplied_values, color="#55768F")
    ax.set_xlabel("Time (h)")
    ax.set_ylabel("Water level (m)")
    fig.savefig("data-panel.svg")
    fig.savefig("data-panel.pdf")
    fig.savefig("data-panel.png", dpi=300)
```

This is a usage excerpt: sample_time and supplied_values come from your actual data. The context changes fonts/colors only, never observations, axes or coordinates. Keep a standalone vector chart alongside the composite figure; the current compositor embeds an image panel as raster, so an embedded chart PNG is not an editable vector plot.
