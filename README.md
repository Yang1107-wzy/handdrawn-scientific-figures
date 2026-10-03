# Handdrawn Scientific Figures

[中文说明](README.zh-CN.md)

A reusable natural scientific sketch style for paper figures and research slides: warm pen illustrations, fixed pastel colors, handwritten titles and notes, accurate numerical typography, and editable label/connection layers.

![Original hand-drawn scientific scene](skills/handdrawn-scientific-figures/assets/style-reference.png)

## Use it

**Codex / Claude Code**

```sh
git clone https://github.com/Yang1107-wzy/handdrawn-scientific-figures.git
cd handdrawn-scientific-figures
python -m pip install -r requirements.txt
python scripts/validate.py
python scripts/install.py --client codex
python scripts/install.py --client codex --apply
```

The first installer previews; `--apply` copies the complete self-contained skill. Codex user destination is `~/.agents/skills/handdrawn-scientific-figures`; Claude Code uses `--client claude` and `~/.claude/skills/handdrawn-scientific-figures`. `--client both` is explicit. Existing skill folders are preserved. Project scope: `--scope project --project-root /path/to/project`. No client settings, models or APIs are installed.

Codex prompt:

```text
Use $handdrawn-scientific-figures to create a paper method figure from these source materials, preserving the feedback edge and exact equations.
```

Claude Code prompt:

```text
/handdrawn-scientific-figures Draw this research scene for a 16:9 presentation, with large handwritten notes and precise scientific labels.
```

**ChatGPT / Claude chat**

Copy [the complete master prompt](skills/handdrawn-scientific-figures/references/master-prompt.md), fill the CONTENT BRIEF, and attach sources and a style reference. There are [four composition templates](skills/handdrawn-scientific-figures/references/figure-templates.md). No native skill installation is required for paste-only use.

For native PowerPoint typography, install Kalam-Bold.ttf and PatrickHand-Regular.ttf from the bundled fonts folder on the viewing computer. On macOS, open the files in Font Book and choose Install; on Windows, use the font file's Install command. The Python compositor reads bundled fonts directly, so its PNG/PDF/SVG needs no system font installation.

## What stays fixed

Pure white; fine charcoal pen outlines; pastel powder blue, lavender, butter yellow, orange and mint. Kalam Bold titles, Patrick Hand notes, DejaVu Sans technical/numerical text and proper mathematical typesetting.

The composition changes with the research. Avoid repeated dashboard cards, glossy rendering and irrelevant mascots. Generated art explains a scene; Python plots supplied data; vector layers carry exact labels and critical connections.

| Use | Default |
|---|---|
| Paper | 180 × 110 mm, 300 dpi PNG, PDF and self-contained SVG |
| Presentation | 16:9, 3840 × 2160 PNG and an editable one-slide PPTX |

Venue-specific dimensions override defaults. See [style rules](skills/handdrawn-scientific-figures/references/style-guide.md) and [layer composition](skills/handdrawn-scientific-figures/references/composition.md).

## Three reproducible examples

| Example | Purpose | Preview |
|---|---|---|
| Method | Two inputs, estimate, exact height equation and quality-check feedback | [Method](examples/method/figure.png) |
| Scene | Field, river, gauges and satellite observation | [Scene](examples/scene/figure.png) |
| Hybrid | Hand-drawn sensor setup with explicit synthetic teaching signal | [Hybrid](examples/hybrid/figure.png) |

```sh
python examples/build_examples.py
python -m unittest discover -s tests -v
python scripts/package.py --output dist/handdrawn-scientific-figures.zip
python scripts/package.py --skill-only --output dist/handdrawn-scientific-figures-skill.zip
```

Examples rebuild offline from original generated art, public manifests and explicitly synthetic CSV. Image generation itself is not deterministic and needs an available image tool. The helper scripts neither call paid APIs nor redraw research evidence. See [example provenance](examples/README.md), [behavioral evaluation](evaluations/README.md), and [source/license record](SOURCES.md).

SVG/PDF preserve text/vector connections while embedded art stays bitmap. Standalone chart SVG/PDF are supplied for quantitative editing. PPTX text/connectors are editable; formulas are images, fonts are referenced rather than embedded, and rough panel outlines use native straight rectangles. Install the bundled fonts when viewing PPTX elsewhere.

Claude natively supports diagrams/charts/SVG, not raster illustrations like an image model; connect an appropriate image tool for that layer. No raster image is claimed when the tool is unavailable. Platform capability differs from merely having this skill installed. [Official Claude capability note](https://support.claude.com/en/articles/9002504-can-claude-produce-images).

Original prompts/code use MIT; bundled fonts retain their licenses. The repository contains original illustrative art, not the user's style-reference screenshots, application portfolio or unpublished research data.
