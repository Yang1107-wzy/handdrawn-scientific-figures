"""Offline Matplotlib styling. No sketching, coordinate transforms or data edits.

Use ``with chart_context():`` around chart creation and export. Font files and
palette come from ../assets/style.json; the caller retains axes and data control.
"""

import argparse
from contextlib import contextmanager
import json
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / "assets"


def load_style(path=None):
    return json.loads(Path(path or ASSETS / "style.json").read_text(encoding="utf-8"))


def font_paths(style=None):
    return {key: ASSETS / value["file"] for key, value in (style or load_style())["fonts"].items()}


@contextmanager
def chart_context(profile="paper", style_path=None):
    """Temporarily apply fonts/palette. Quantitative geometry remains unchanged."""
    import matplotlib as mpl
    from matplotlib import font_manager
    from cycler import cycler

    style = load_style(style_path)
    if profile not in style["profiles"]:
        raise ValueError(f"Unknown chart profile: {profile}")
    for path in font_paths(style).values():
        if not path.is_file():
            raise FileNotFoundError(f"Missing font: {path.name}")
        font_manager.fontManager.addfont(str(path))
    palette, settings = style["palette"], style["profiles"][profile]
    params = {
        "font.family": style["fonts"]["body"]["family"],
        "font.size": settings["body_pt"],
        "axes.titlesize": settings["title_pt"],
        "axes.labelsize": settings["label_pt"],
        "axes.prop_cycle": cycler(
            color=[palette[k] for k in ("blue", "orange", "mint", "lavender", "coral", "yellow")]
        ),
        "text.color": palette["ink"],
        "axes.edgecolor": palette["ink"],
        "axes.labelcolor": palette["ink"],
        "xtick.color": palette["ink"],
        "ytick.color": palette["ink"],
        "figure.facecolor": palette["white"],
        "axes.facecolor": palette["white"],
        "savefig.facecolor": palette["white"],
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "text.usetex": False,
        "mathtext.fontset": style["math"]["fontset"],
        "path.sketch": None,
    }
    with mpl.rc_context(params):
        yield style


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--show", action="store_true", help="Print shared palette/fonts/profile metadata as JSON"
    )
    args = parser.parse_args()
    if args.show:
        print(json.dumps(load_style(), indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
