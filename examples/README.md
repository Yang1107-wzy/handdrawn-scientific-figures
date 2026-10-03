# Original examples

The three examples are illustrative teaching figures. They do not represent a submitted paper, a validated field deployment or an experimental result.

- method: a generic field-height workflow with two inputs, data alignment, estimation, a quality check, a realignment feedback edge and human review.
- scene: a conceptual environmental observation scene with weather, river-level and remote observations.
- hybrid: an illustrative sensor setup next to deterministic synthetic teaching signals, explicitly labeled.

Original generated illustrations and exact prompts are retained in art/ and art-prompts.json. Six method spot illustrations are presentation crops of method-atlas.png. No source research photograph was altered.

Run `python examples/build_examples.py` from the repository root. It rebuilds the manifests, synthetic teaching CSV, standalone plot SVG/PDF/PNG, and each example's paper and presentation exports from bundled artwork. The script regenerates only its own declared output files and does not need an image-generation tool or network connection.

Paper files: figure.png/pdf/svg and render-report. Presentation files: slide.png/pdf/svg/pptx and render-report. Scene illustration pixels remain raster; exact labels/connections are editable layers. The hybrid quantitative chart also has standalone plot.svg/pdf so it can be edited as a vector plot.

For a real project, use your own source-grounded method and measured data; do not reuse the teaching CSV as evidence.
