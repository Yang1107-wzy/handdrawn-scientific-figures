# Copyable master prompt

Copy the text block into ChatGPT or another assistant; replace only the CONTENT BRIEF. The English style block stays fixed. Attach a style reference and source materials when the interface supports them.

```text
Create a scientific figure in this fixed natural hand-drawn research style.

CONTENT BRIEF
Use: [paper figure / research presentation]
Main scientific message: [one sentence]
Research content and verified method: [source-grounded description]
Required entities and relations: [inputs, transformations, outputs, feedback]
Exact labels, equations and units: [verbatim list]
Data available: [CSV / aggregate values / none; provenance and denominators]
Final size: [venue size, or default paper 180 mm wide / PPT 16:9]
Deliverables: [rendered figure, editable text/connectors, art, prompt, source notes]

FIXED VISUAL LANGUAGE
Use a pure white (#FFFFFF) foundation and fine dark-charcoal (#252525) ink outlines with subtle natural irregularity. Use restrained flat pastel powder blue (#BFD8F0), lavender (#DCC7EB), butter yellow (#FFE5A3), muted orange (#F2B37E) and mint green (#C8E6C1). Make it feel like a carefully drawn scientific whiteboard or academic sketch: warm, clear, expressive and technically precise.

Build one coherent scientific story with one dominant scene or mechanism. Organize space around the real entities and relationships, not equal-sized cards. Use subject-specific illustrations, concise local notes, generous white gutters, a few dashed groups and hand-drawn underlines. Keep most labels to two to four words. Give colors consistent meanings within this figure. Route feedback around text, and give every connection an unmistakable origin and destination.

TYPESETTING
Use Kalam Bold for the main title, Patrick Hand for short labels and notes, DejaVu Sans for technical body text, numerical values, units and tick labels, and proper Computer Modern-style mathematical typesetting. Generate clean label-free raster art first, then add exact text, formulas and critical connectors as editable layers. Do not rely on a bitmap image model to spell equations or numerical results.

ACCURACY AND OUTPUT
Use only the supplied scientific content. Do not add modules, causal claims or experimental results. Draw quantitative charts from supplied data or explicitly identified aggregate values. Preserve coordinates, scales, denominators and units; never invent distributions or confidence intervals from summary values. Distinguish a conceptual illustration from a photograph or measured output.

Paper default: 180 mm wide, 300 dpi, PNG plus PDF and SVG. Presentation default: 16:9, 3840 × 2160 PNG plus a PPTX slide with editable text and connections. Retain the prompt, layer specification, art and data source notes. Raster illustrations remain raster inside vector containers.

AVOID
No neon, glow, glossy 3D, glassmorphism, cinematic lighting, full-canvas gradient, heavy shadow, corporate dashboard, repetitive number cards, irrelevant robot mascot or childish decoration. Do not copy the reference's paper content. Do not route arrows through words.

CHECK
Inspect the finished figure at its actual reading size. Check scientific relations, formula spelling, arrow destinations, clipped text and visual balance. If the required image-generation tool is unavailable, say which artifact is missing and deliver the exact art prompt and layer plan; do not claim the illustration has been generated.
```

## 中文填写说明

只替换内容简报：用途、核心信息、研究方法、必须出现的关系、精确文字与公式、数据来源、目标尺寸。视觉语言段落不随项目改变。

- 方法图：提供模块与有向关系，并指出反馈返回哪个模块。
- 场景图：说明需要画哪些真实实体，以及观察、几何或因果关系的区别。
- 数据组合图：提供 CSV 或已核对的汇总值，并给出单位、分母和统计口径。
- PPT：说明讲解重点，减少细节；仍使用同一色板和字体。

公式写成可核对的 LaTeX；普通标签给出最终拼写。没有逐样本数据时，不能把几个平均值写成误差分布。可以提供支持的汇总比较，并标明该比较的条件。

## 完整示例：方法与反馈

```text
Use: paper figure.
Main message: an estimate must share a floor reference and pass a quality check before human review.
Research content: field camera data and a ground reference enter data alignment; aligned data enter estimation; the estimate goes to a quality check.
Required relations: camera -> alignment; ground reference -> alignment; alignment -> estimation -> quality check; failed check -> alignment; passed check -> staff review.
Exact labels: Field camera, Ground reference, Align inputs, Estimate height, Quality check, Staff review, Pass, Realign.
Equation: h = z_{\mathrm{top}} - z_{\mathrm{floor}}.
Data: none. This is a conceptual teaching example, not an experimental result.
Final size: paper width 180 mm.
Deliverables: PNG/PDF/SVG, editable labels/connectors, art prompt, layer manifest and provenance.
Apply the FIXED VISUAL LANGUAGE and all accuracy/output rules above.
```
