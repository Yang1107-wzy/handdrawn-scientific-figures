---
name: handdrawn-scientific-figures
description: Use when creating or restyling natural hand-drawn scientific figures, research scenes, methodology diagrams, mechanism schematics, technical pathways, or research presentation graphics. Also applies to 手绘科研配图、论文方法图、场景图、机制示意和科研 PPT 配图.
license: MIT
---

# Handdrawn Scientific Figures

Preserve a warm, precise scientific sketch style across changing research topics. Build a content-specific composition; do not reuse a fixed dashboard of boxes.

## Start with the research

Read the supplied method, source images or data. Identify one main scientific message, exact terms, required relations and intended final size. Distinguish observations, interpretations and conceptual illustrations. Missing methods, units or denominators must not be invented. Two aggregate means cannot reconstruct a distribution.

## Fixed visual system

Read [the style guide](references/style-guide.md) and use [the portable master prompt](references/master-prompt.md). The machine-readable preset is [assets/style.json](assets/style.json).

Use pure white, fine slightly irregular charcoal outlines, restrained pastel fills, clear gutters and a dominant meaningful visual. Main titles use Kalam Bold; short notes use Patrick Hand; numbers, units and technical text use DejaVu Sans; mathematical labels use proper math typesetting. Fonts are bundled in assets/fonts.

Choose a scene, spatial layout, cutaway or method composition that explains the subject. Small icons should represent actual concepts. Use one coherent color meaning per figure and short labels. Every connector needs a clear origin and destination; feedback goes around labels. Decorative irregularity must never move plotted data or alter axis scales.

## Produce the layers

1. Choose the matching template in [figure templates](references/figure-templates.md). Fix the semantic graph and accurate text before generating art.
2. Use the available image-generation tool for original hand-drawn raster scenes or illustrations. Generate clean label-free art; save the exact prompt and original output.
3. Add accurate text, equations and important connectors programmatically. Read [composition](references/composition.md) and run scripts/compose_figure.py with the layer manifest.
4. Draw quantitative panels from supplied CSV or explicitly identified aggregate values. Use scripts/chart_style.py for appearance without changing coordinates. Save data and a standalone vector chart.
5. Inspect the actual PNG/PDF at its final reading size. Fix clipping, overlaps, ambiguous arrows, malformed formulas or misleading data annotations.

If raster generation is unavailable, deliver its complete prompt and layout specification, and state the missing artifact. Native SVG can still handle diagrams when appropriate; do not report an illustration as generated.

## Deliver

Paper defaults: 180 × 110 mm, 300 dpi, PNG/PDF/SVG. Respect a supplied journal size. PPT defaults: 16:9, 3840 × 2160 PNG and one editable PPTX slide, with larger labels and less detail.

Include rendered files, layer manifest, art, prompts and source notes. SVG/PDF retain text and vector connections; raster art stays raster. PPTX text/connectors are editable; equations and illustrations have documented limitations.

Use [platform instructions](references/platforms.md) for Codex, Claude Code or paste-only chat. The skill does not install an image model, call a paid API automatically, publish research or certify journal acceptance.
