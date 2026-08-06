"""Render ground truth and four saved model predictions without rerunning inference."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont, ImageOps


MODEL_FILES = {
    "grounding_dino": ("Grounding DINO", "examples/outputs/grounding_dino_results.csv", "#2563EB"),
    "owlvit": ("OWL-ViT", "examples/outputs/owlvit_results.csv", "#F97316"),
    "gpt_vision": ("GPT Vision", "examples/outputs/gpt_vision_results.csv", "#DB2777"),
    "gpt_guided_owlvit": (
        "GPT-guided OWL-ViT",
        "examples/outputs/gpt_guided_owlvit/gpt_guided_owlvit_results.csv",
        "#7C3AED",
    ),
}
GROUND_TRUTH_COLOR = "#16A34A"
FAILED_COLOR = "#B91C1C"
BACKGROUND = "#111827"
TEXT_COLOR = "#F9FAFB"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"CSV is empty: {path}")
    return rows


def as_float(value: object) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def box_from_row(row: dict[str, str], prefix: str) -> tuple[float, float, float, float] | None:
    values = tuple(as_float(row.get(f"{prefix}_{axis}")) for axis in ("x_min", "y_min", "x_max", "y_max"))
    if any(value is None for value in values):
        return None
    x_min, y_min, x_max, y_max = values
    if x_max <= x_min or y_max <= y_min:
        return None
    return x_min, y_min, x_max, y_max


def load_font(size: int, bold: bool = False):
    candidates = (
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
    )
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def fit_text(draw: ImageDraw.ImageDraw, text: str, font, max_width: int) -> str:
    text = " ".join(str(text).split())
    if draw.textbbox((0, 0), text, font=font)[2] <= max_width:
        return text
    suffix = "…"
    while text and draw.textbbox((0, 0), text + suffix, font=font)[2] > max_width:
        text = text[:-1]
    return text.rstrip() + suffix


def draw_box(
    draw: ImageDraw.ImageDraw,
    box: tuple[float, float, float, float],
    *,
    color: str,
    label: str,
    width: int,
    font,
    image_width: int,
    image_height: int,
) -> None:
    x_min, y_min, x_max, y_max = box
    x_min = max(0, min(image_width - 1, round(x_min)))
    y_min = max(0, min(image_height - 1, round(y_min)))
    x_max = max(x_min + 1, min(image_width, round(x_max)))
    y_max = max(y_min + 1, min(image_height, round(y_max)))
    draw.rectangle((x_min, y_min, x_max, y_max), outline=color, width=width)

    text_box = draw.textbbox((0, 0), label, font=font)
    text_width = text_box[2] - text_box[0]
    text_height = text_box[3] - text_box[1]
    label_y = max(0, y_min - text_height - 12)
    if label_y == 0:
        label_y = min(image_height - text_height - 10, y_min + 6)
    label_x = min(max(0, x_min), max(0, image_width - text_width - 12))
    draw.rounded_rectangle(
        (label_x, label_y, label_x + text_width + 12, label_y + text_height + 8),
        radius=4,
        fill=color,
    )
    draw.text((label_x + 6, label_y + 2), label, fill="white", font=font)


def prompt_from_row(row: dict[str, str]) -> str:
    for key in (
        "model_grounding_prompt",
        "relational_prompt",
        "grounding_prompt",
        "original_grounding_prompt",
    ):
        if row.get(key):
            return row[key]
    return ""


def annotated_image(
    source: Image.Image,
    *,
    model_name: str,
    model_color: str,
    prediction: dict[str, str],
    ground_truth: dict[str, str],
) -> Image.Image:
    image = source.copy().convert("RGB")
    draw = ImageDraw.Draw(image)
    scale = max(1.0, min(image.width, image.height) / 720.0)
    line_width = max(4, round(7 * scale))
    label_font = load_font(max(15, round(18 * scale)), bold=True)

    gt_box = box_from_row(ground_truth, "gt")
    if gt_box:
        draw_box(
            draw,
            gt_box,
            color=GROUND_TRUTH_COLOR,
            label="Ground truth",
            width=line_width,
            font=label_font,
            image_width=image.width,
            image_height=image.height,
        )

    status = str(prediction.get("status", "failed")).strip().lower()
    pred_box = box_from_row(prediction, "pred") if status == "success" else None
    iou = as_float(prediction.get("iou")) or 0.0
    matched = prediction.get("matched_phrase") or prediction.get("selected_label") or "prediction"
    if pred_box:
        draw_box(
            draw,
            pred_box,
            color=model_color,
            label=f"{model_name}: {matched}",
            width=line_width,
            font=label_font,
            image_width=image.width,
            image_height=image.height,
        )

    banner_height = max(72, round(82 * scale))
    canvas = Image.new("RGB", (image.width, image.height + banner_height), BACKGROUND)
    canvas.paste(image, (0, banner_height))
    banner = ImageDraw.Draw(canvas)
    title_font = load_font(max(18, round(23 * scale)), bold=True)
    body_font = load_font(max(14, round(17 * scale)))
    banner.text((18, 10), model_name, fill=model_color, font=title_font)
    status_text = f"Status: {status}   IoU: {iou:.3f}"
    if not pred_box:
        status_text += "   No valid prediction box"
    banner.text((18, 42 * scale), status_text, fill=TEXT_COLOR if pred_box else FAILED_COLOR, font=body_font)
    return canvas


def resize_panel(image: Image.Image, width: int) -> Image.Image:
    if image.width == width:
        return image
    height = max(1, round(image.height * width / image.width))
    return image.resize((width, height), Image.Resampling.LANCZOS)


def combined_grid(
    panels: list[Image.Image],
    *,
    image_id: str,
    prompt: str,
    panel_width: int,
) -> Image.Image:
    resized = [resize_panel(panel, panel_width) for panel in panels]
    panel_height = max(panel.height for panel in resized)
    title_height = 92
    gap = 16
    grid = Image.new(
        "RGB",
        (panel_width * 2 + gap * 3, title_height + panel_height * 2 + gap * 3),
        BACKGROUND,
    )
    draw = ImageDraw.Draw(grid)
    title_font = load_font(25, bold=True)
    prompt_font = load_font(17)
    draw.text((gap, 12), image_id, fill=TEXT_COLOR, font=title_font)
    draw.text(
        (gap, 50),
        fit_text(draw, f"Prompt: {prompt}", prompt_font, grid.width - gap * 2),
        fill="#D1D5DB",
        font=prompt_font,
    )
    for index, panel in enumerate(resized):
        row, column = divmod(index, 2)
        x = gap + column * (panel_width + gap)
        y = title_height + gap + row * (panel_height + gap)
        grid.paste(panel, (x, y))
    return grid


def write_index(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_readme(path: Path, count: int) -> None:
    path.write_text(
        "\n".join(
            [
                "# Visual model comparisons",
                "",
                f"Generated overlays for {count} benchmark images without rerunning inference.",
                "",
                "- Green: corrected ground-truth box",
                "- Blue: Grounding DINO prediction",
                "- Orange: OWL-ViT prediction",
                "- Pink: GPT Vision prediction",
                "- Purple: GPT-guided OWL-ViT prediction",
                "",
                "`per_model/` contains one full-resolution annotated image per model and benchmark row.",
                "`combined/` contains one 2×2 comparison grid per benchmark row.",
                "`index.csv` records the status, IoU, and output paths for every comparison.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--panel-width", type=int, default=900)
    parser.add_argument("--jpeg-quality", type=int, default=88)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    root = args.project_root.expanduser().resolve()
    output = (args.output_dir or root / "results" / "visual_comparisons").resolve()
    combined_dir = output / "combined"
    combined_dir.mkdir(parents=True, exist_ok=True)

    ground_truth_rows = read_csv(root / "examples/ground_truth_boxes.csv")
    ground_truth = {row["image_id"]: row for row in ground_truth_rows}
    model_rows = {
        key: {row["image_id"]: row for row in read_csv(root / relative_path)}
        for key, (_, relative_path, _) in MODEL_FILES.items()
    }
    image_ids = sorted(ground_truth)
    if args.limit is not None:
        image_ids = image_ids[: args.limit]
    for key, rows in model_rows.items():
        if set(rows) != set(ground_truth):
            raise ValueError(f"{key} does not contain exactly the benchmark image IDs")

    per_model_dirs = {}
    for key in MODEL_FILES:
        model_dir = output / "per_model" / key
        model_dir.mkdir(parents=True, exist_ok=True)
        per_model_dirs[key] = model_dir

    index_rows: list[dict[str, object]] = []
    for number, image_id in enumerate(image_ids, start=1):
        gt = ground_truth[image_id]
        image_path = root / gt["image_path"]
        with Image.open(image_path) as handle:
            source = ImageOps.exif_transpose(handle).convert("RGB")

        panels = []
        index_row: dict[str, object] = {
            "image_id": image_id,
            "image_path": gt["image_path"],
            "prompt": prompt_from_row(model_rows["grounding_dino"][image_id]),
        }
        for key, (model_name, _, model_color) in MODEL_FILES.items():
            prediction = model_rows[key][image_id]
            rendered = annotated_image(
                source,
                model_name=model_name,
                model_color=model_color,
                prediction=prediction,
                ground_truth=gt,
            )
            per_model_path = per_model_dirs[key] / f"{image_id}.jpg"
            rendered.save(per_model_path, "JPEG", quality=args.jpeg_quality, optimize=True)
            panels.append(rendered)
            index_row[f"{key}_status"] = prediction.get("status", "")
            index_row[f"{key}_iou"] = as_float(prediction.get("iou")) or 0.0
            index_row[f"{key}_image"] = per_model_path.relative_to(root).as_posix()

        comparison = combined_grid(
            panels,
            image_id=image_id,
            prompt=index_row["prompt"],
            panel_width=args.panel_width,
        )
        combined_path = combined_dir / f"{image_id}.jpg"
        comparison.save(combined_path, "JPEG", quality=args.jpeg_quality, optimize=True)
        index_row["combined_image"] = combined_path.relative_to(root).as_posix()
        index_rows.append(index_row)
        print(f"[{number}/{len(image_ids)}] {image_id}")

    write_index(output / "index.csv", index_rows)
    write_readme(output / "README.md", len(index_rows))
    print(f"Visual comparisons written to {output}")


if __name__ == "__main__":
    main()
