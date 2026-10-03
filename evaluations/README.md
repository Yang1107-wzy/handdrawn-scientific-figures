# Behavioral evaluation

The baseline uses a fresh-context agent, the same style reference and a research request containing a height formula, a failed-check feedback edge, two MAE aggregates with no sample records, and no raster image tool. A second scenario asks for a 16:9 presentation version.

## Baseline observation

Scientific integrity already passed: the agent did not infer an error distribution, invent units or claim unavailable images. It specified the correct feedback destination and preserved the equation.

Persistent style defaults were not locked: the response used generic handwriting rather than named Kalam/Patrick Hand fonts, did not fix exact palette hex values, and selected a 1920×1080 presentation instead of the agreed 3840×2160 preset. This is the style-reproducibility gap the skill addresses; it is not evidence of a general scientific failure.

The public repository contains only this summary. The user's original style screenshots and raw evaluation context are not redistributed.

## Skill-loaded evaluation

Executed with a second fresh-context agent using the same request and reference, plus the skill. Observed: exact named fonts, full fixed palette, paper180x110mm/300dpi and PPT3840x2160, preserved formula and feedback edge, no invented distributions from aggregates and no false raster-generation claim. It documented editable text/connectors, bitmap art, PPTX formula/font limitations and a native SVG fallback when appropriate.

The evaluation produced instructions/prompt and syntax-checked composition code, not an executed raster figure. It is one observed agent comparison, not a model-wide benchmark. Actual rendering, scientific-data preservation and file safety are separately exercised by offline tests. A Claude runtime session was not run; compatibility describes packaging and documented discovery, not identical behavior.


## Artifact and native-slide checks

39 offline tests passed on the local macOS Python3.12 environment. Ruff checks and skill metadata/resource validation passed. Three paper figures and three4K presentation figures rebuilt offline. Their original art bytes were preserved. Native PPTX was rendered through LibreOffice; a font-substitution/title-box defect and inherited connector shadows were found and fixed with failing-then-passing regression tests. Native rendering was checked again with the packaged handwriting fonts installed. This is not a Microsoft PowerPoint execution claim.

The configured GitHub CI matrix covers Linux, Windows and macOS with Python3.11/3.13; remote execution has not yet occurred.

Final independent review identified two additional issues: feedback crossing a label and missing dependencies in the skill-only bundle. Both were reproduced by new failing tests, corrected, and rechecked.
