"""Rebuild three original educational examples offline from bundled art and exact CSV."""

from copy import deepcopy
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills/handdrawn-scientific-figures/scripts"
sys.path.insert(0, str(SCRIPTS))
from chart_style import chart_context  # noqa: E402 - standalone installed skill helper
from compose_figure import compose_figure  # noqa: E402 - standalone installed skill helper

INK = "#252525"
BLUE = "#BFD8F0"
PURPLE = "#DCC7EB"
YELLOW = "#FFE5A3"
ORANGE = "#F2B37E"
MINT = "#C8E6C1"


def text(value, x, y, font="hand", size=10, max_width=None):
    item = dict(type="text", text=value, x=x, y=y, font=font, font_size=size)
    if max_width is not None:
        item["max_width"] = max_width
    return item


def image(path, x, y, width, height):
    return dict(type="image", path=path, x=x, y=y, width=width, height=height)


def arrow(points, color=INK, width=0.85):
    return dict(type="arrow", points=points, color=color, line_width=width)


def underline(x, y, width, color):
    return dict(
        type="line",
        points=[[x, y], [x + width * 0.35, y + 0.3], [x + width * 0.72, y - 0.2], [x + width, y]],
        color=color,
        line_width=2.4,
    )


def method_manifest():
    return {
        "profile": "paper",
        "layers": [
            text("Field height estimation", 8, 6, "title", 16),
            underline(8, 14, 79, YELLOW),
            text(
                "Conceptual teaching workflow with a shared vertical reference.", 8, 19, "body", 8.5
            ),
            image("../art/method-1.png", 7, 31, 30, 28),
            image("../art/method-2.png", 7, 64, 30, 25),
            image("../art/method-3.png", 48, 40, 24, 27),
            image("../art/method-4.png", 82, 30, 34, 38),
            image("../art/method-5.png", 121, 40, 21, 27),
            image("../art/method-6.png", 150, 37, 24, 27),
            text("Field camera", 7, 59, size=10),
            text("Ground reference", 7, 90, size=10),
            text("Align inputs", 48, 70, size=10),
            text("Estimate height", 80, 70, size=10),
            text("Quality check", 119, 70, size=10),
            text("Staff review", 150, 69, size=10),
            arrow([[38, 44], [47, 44]], "#55768F"),
            arrow([[38, 78], [45, 78], [45, 48], [47, 48]], "#55768F"),
            arrow([[74, 50], [81, 50]]),
            arrow([[116, 50], [120, 50]]),
            arrow([[142, 50], [149, 50]], "#62977A"),
            text("Pass", 142, 44, "body", 8.5),
            arrow([[139, 63], [146, 63], [146, 98], [76, 98], [76, 60], [72, 60]], "#C48455"),
            text("Fail: realign", 82, 91, size=10),
            dict(
                type="math",
                text="h = z_{\\mathrm{top}} - z_{\\mathrm{floor}}",
                x=80,
                y=80,
                font_size=10,
            ),
            text("Exact labels and feedback are editable layers.", 8, 103, "body", 8.5),
        ],
    }


def scene_manifest():
    return {
        "profile": "paper",
        "layers": [
            text("Environmental observation", 8, 6, "title", 16),
            underline(8, 14, 74, MINT),
            image("../art/field-scene.png", 7, 19, 132, 83),
            text("Satellite observation", 144, 26, size=10, max_width=29),
            arrow([[143, 37], [113, 37], [95.0, 24.9]], "#55768F"),
            text("Weather station", 6, 25, size=10, max_width=35),
            arrow([[19, 31], [19.8, 40.6]], "#55768F"),
            text("River-level gauges", 144, 64, size=10, max_width=29),
            arrow([[143, 76], [114, 76], [112.1, 64.8]], "#55768F"),
            text("Subsurface context", 144, 85, size=10, max_width=29),
            arrow([[143, 98], [114, 98], [105.6, 89.7]], "#62977A"),
            text("Conceptual scene", 7, 105, "body", 8.5),
        ],
    }


def teaching_data(folder):
    path = folder / "teaching_signal.csv"
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["time_h", "analytic_m", "illustrative_m"])
        for t in range(25):
            base = 1.2 + 0.3 * math.sin(2 * math.pi * t / 24)
            second = base + 0.03 * math.cos(math.pi * t / 3)
            writer.writerow([t, f"{base:.10f}", f"{second:.10f}"])
    return path


def plot_signal(folder, source, profile="paper"):
    import matplotlib.pyplot as plt

    with source.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    xs = [float(r["time_h"]) for r in rows]
    a = [float(r["analytic_m"]) for r in rows]
    b = [float(r["illustrative_m"]) for r in rows]
    with chart_context(profile):
        size = (85, 57) if profile == "paper" else (85 * 338.666667 / 180, 57 * 190.5 / 110)
        fig, ax = plt.subplots(figsize=(size[0] / 25.4, size[1] / 25.4))
        fig.subplots_adjust(left=0.20, right=0.97, bottom=0.24, top=0.96)
        ax.plot(xs, a, color="#55768F", linewidth=1.1, label="Analytic signal")
        ax.plot(xs, b, color="#C48455", linewidth=0.9, linestyle="--", label="Synthetic variation")
        ax.set(xlim=(0, 24), ylim=(0, 1.7), xlabel="Time (h)", ylabel="Level (m)")
        ax.set_xticks([0, 6, 12, 18, 24])
        ax.set_yticks([0, 0.5, 1, 1.5])
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(labelsize=8.5 if profile == "paper" else 18)
        ax.grid(color="#E7E8EA", linewidth=0.6)
        ax.legend(frameon=False, fontsize=8.5 if profile == "paper" else 18, loc="lower left")
        prefix = "plot" if profile == "paper" else "plot-ppt"
        fig.savefig(folder / (prefix + ".png"), dpi=300)
        stamp = datetime.fromtimestamp(1791072000, timezone.utc)
        fig.savefig(
            folder / (prefix + ".pdf"),
            metadata={
                "CreationDate": stamp,
                "ModDate": stamp,
                "Creator": "handdrawn-scientific-figures",
            },
        )
        with plt.rc_context({"svg.hashsalt": "hdsf-teaching-signal"}):
            fig.savefig(folder / (prefix + ".svg"), metadata={"Date": "2026-10-04"})
        plt.close(fig)
    record = {
        "kind": "deterministic synthetic teaching data; not experimental observations",
        "rows": 25,
        "time_unit": "h",
        "value_unit": "m",
        "analytic": "1.2 + 0.3 * sin(2*pi*t/24)",
        "illustrative": "analytic + 0.03 * cos(pi*t/3)",
        "file": source.name,
        "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
    }
    (folder / "data-source.json").write_text(json.dumps(record, indent=2) + "\n")


def hybrid_manifest():
    return {
        "profile": "paper",
        "layers": [
            text("Illustrative water-level signals", 8, 6, "title", 16),
            underline(8, 14, 124, PURPLE),
            text(
                "Synthetic teaching example with an analytic reference signal.", 8, 20, "body", 8.5
            ),
            text("Conceptual apparatus", 7, 30, size=10),
            image("../art/signal-scene.png", 5, 38, 79, 53),
            text("Every point comes from CSV", 93, 30, size=10),
            image("plot.png", 90, 38, 85, 57),
            text("Art explains the apparatus;\nCSV fixes every plotted point.", 7, 96, "body", 8.5),
            dict(type="math", text="u(t)=1.2+0.3\\sin(2\\pi t/24)", x=92, y=98, font_size=9.5),
        ],
    }


def presentation(manifest, name):
    """Use the same semantics, with larger labels and shortened prose for projection."""
    result = deepcopy(manifest)
    result["profile"] = "ppt"
    sx, sy = 338.666667 / 180, 190.5 / 110
    for layer in result["layers"]:
        for key in ("x", "width", "max_width"):
            if key in layer:
                layer[key] *= sx
        for key in ("y", "height"):
            if key in layer:
                layer[key] *= sy
        if "points" in layer:
            layer["points"] = [[x * sx, y * sy] for x, y in layer["points"]]
        if layer["type"] == "text":
            layer["font_size"] = (
                30 if layer.get("font") == "title" else (18 if layer.get("font") == "body" else 24)
            )
        if layer["type"] == "math":
            layer["font_size"] = 20
    if name == "method":
        short = {
            "Align inputs": "Align",
            "Estimate height": "Estimate",
            "Ground reference": "Ground reference",
            "Quality check": "Check",
            "Staff review": "Review",
        }
        for layer in result["layers"]:
            if layer["type"] == "text":
                layer["text"] = short.get(layer["text"], layer["text"])
    if name == "scene":
        # Recompute annotation tips from the exact fitted artwork bounds.
        art = next(item for item in result["layers"] if item["type"] == "image")
        actual_h = min(art["height"], art["width"] / 1.5)
        actual_w = actual_h * 1.5
        left = art["x"] + (art["width"] - actual_w) / 2
        top = art["y"] + (art["height"] - actual_h) / 2
        points = [(1040, 73), (111, 267), (1250, 565), (1170, 872)]
        arrows = [item for item in result["layers"] if item["type"] == "arrow"]
        for layer, (px, py) in zip(arrows, points):
            layer["points"][-1] = [left + actual_w * px / 1536, top + actual_h * py / 1024]
    if name == "hybrid":
        for layer in result["layers"]:
            if layer["type"] == "image" and layer["path"] == "plot.png":
                layer["path"] = "plot-ppt.png"
    return result


def main():
    result = {}
    for name, build in [
        ("method", method_manifest),
        ("scene", scene_manifest),
        ("hybrid", hybrid_manifest),
    ]:
        folder = ROOT / "examples" / name
        folder.mkdir(exist_ok=True)
        if name == "hybrid":
            source = teaching_data(folder)
            plot_signal(folder, source)
            plot_signal(folder, source, "ppt")
        config = build()
        (folder / "figure.json").write_text(json.dumps(config, indent=2) + "\n")
        paper = compose_figure(folder / "figure.json", folder / "figure", overwrite=True)
        (folder / "slide.json").write_text(json.dumps(presentation(config, name), indent=2) + "\n")
        slide = compose_figure(folder / "slide.json", folder / "slide", overwrite=True)
        result[name] = {
            "paper_pixels": paper["dimensions"]["pixels"],
            "ppt_pixels": slide["dimensions"]["pixels"],
            "bounds_warnings": paper["bounds_warnings"] + slide["bounds_warnings"],
        }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
