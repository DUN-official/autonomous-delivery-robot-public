"""Build one apples-to-apples report from the four canonical model result CSVs."""

from __future__ import annotations

import argparse
import csv
import math
from collections import Counter
from pathlib import Path
from statistics import mean, median


MODEL_FILES = {
    "grounding_dino": ("Grounding DINO", "examples/outputs/grounding_dino_results.csv"),
    "owlvit": ("OWL-ViT", "examples/outputs/owlvit_results.csv"),
    "gpt_vision": ("GPT Vision", "examples/outputs/gpt_vision_results.csv"),
    "gpt_guided_owlvit": (
        "GPT-guided OWL-ViT",
        "examples/outputs/gpt_guided_owlvit/gpt_guided_owlvit_results.csv",
    ),
}
THRESHOLDS = (0.10, 0.25, 0.50)
QUALITY_ORDER = ("failed", "poor", "weak", "primary", "strict")


def parse_float(value: object, default: float = 0.0) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return default
    return parsed if math.isfinite(parsed) else default


def has_prediction(row: dict[str, str]) -> bool:
    if str(row.get("status", "")).strip().lower() != "success":
        return False
    coordinate_keys = ("pred_x_min", "pred_y_min", "pred_x_max", "pred_y_max")
    values = [parse_float(row.get(key), math.nan) for key in coordinate_keys]
    return all(math.isfinite(value) for value in values) and values[2] > values[0] and values[3] > values[1]


def quality_label(iou: float, valid: bool) -> str:
    if not valid:
        return "failed"
    if iou >= 0.50:
        return "strict"
    if iou >= 0.25:
        return "primary"
    if iou >= 0.10:
        return "weak"
    return "poor"


def load_rows(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise FileNotFoundError(f"Required model result is missing: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"Required model result is empty: {path}")
    required = {"image_id", "status", "iou", "pred_x_min", "pred_y_min", "pred_x_max", "pred_y_max"}
    missing = required.difference(rows[0])
    if missing:
        raise ValueError(f"{path} is missing columns: {sorted(missing)}")
    return rows


def write_csv(path: Path, rows: list[dict[str, object]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def validate_common_image_set(model_rows: dict[str, list[dict[str, str]]]) -> list[str]:
    image_sets = {
        key: {str(row["image_id"]) for row in rows}
        for key, rows in model_rows.items()
    }
    first_key = next(iter(image_sets))
    expected = image_sets[first_key]
    for key, image_ids in image_sets.items():
        if image_ids != expected:
            raise ValueError(
                f"{key} does not use the same image set as {first_key}; "
                f"missing={sorted(expected - image_ids)[:5]}, extra={sorted(image_ids - expected)[:5]}"
            )
        if len(image_ids) != len(model_rows[key]):
            raise ValueError(f"{key} contains duplicate image_id values")
    return sorted(expected)


def calculate(project_root: Path) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, Counter]]:
    loaded = {
        key: load_rows(project_root / relative_path)
        for key, (_, relative_path) in MODEL_FILES.items()
    }
    image_ids = validate_common_image_set(loaded)
    by_model_and_id = {
        key: {str(row["image_id"]): row for row in rows}
        for key, rows in loaded.items()
    }

    metrics: list[dict[str, object]] = []
    per_image: list[dict[str, object]] = []
    quality_counts: dict[str, Counter] = {}

    for model_key, (model_name, relative_path) in MODEL_FILES.items():
        rows = loaded[model_key]
        ious = [parse_float(row.get("iou")) for row in rows]
        valid = [has_prediction(row) for row in rows]
        counts = Counter(
            quality_label(iou, prediction_valid)
            for iou, prediction_valid in zip(ious, valid)
        )
        quality_counts[model_key] = counts
        metrics.append(
            {
                "model_key": model_key,
                "model_name": model_name,
                "rows": len(rows),
                "successful_predictions": sum(valid),
                "prediction_failures": len(rows) - sum(valid),
                "mean_iou": mean(ious),
                "median_iou": median(ious),
                "weak_rate_iou_010": sum(value >= THRESHOLDS[0] for value in ious) / len(ious),
                "primary_rate_iou_025": sum(value >= THRESHOLDS[1] for value in ious) / len(ious),
                "strict_rate_iou_050": sum(value >= THRESHOLDS[2] for value in ious) / len(ious),
                "source_csv": relative_path,
            }
        )

    for image_id in image_ids:
        row: dict[str, object] = {"image_id": image_id}
        for model_key in MODEL_FILES:
            source = by_model_and_id[model_key][image_id]
            row[f"{model_key}_iou"] = parse_float(source.get("iou"))
            row[f"{model_key}_status"] = source.get("status", "")
        per_image.append(row)

    return metrics, per_image, quality_counts


def create_plots(output_dir: Path, metrics: list[dict[str, object]], quality_counts: dict[str, Counter]) -> None:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise RuntimeError("Plot generation requires matplotlib. Install the evaluation extra.") from exc

    names = [str(row["model_name"]) for row in metrics]
    colors = ["#2563eb", "#16a34a", "#f59e0b", "#7c3aed"]

    figure, axis = plt.subplots(figsize=(10, 5.5))
    values = [float(row["mean_iou"]) for row in metrics]
    bars = axis.bar(names, values, color=colors)
    axis.set_ylim(0, 1)
    axis.set_ylabel("Mean IoU")
    axis.set_title("Visual Grounding Accuracy on the Same 105 Images")
    axis.bar_label(bars, fmt="%.3f", padding=3)
    axis.grid(axis="y", alpha=0.25)
    figure.tight_layout()
    figure.savefig(output_dir / "mean_iou_by_model.png", dpi=200)
    plt.close(figure)

    figure, axis = plt.subplots(figsize=(11, 6))
    x = list(range(len(metrics)))
    width = 0.24
    rate_columns = (
        ("weak_rate_iou_010", "IoU ≥ 0.10"),
        ("primary_rate_iou_025", "IoU ≥ 0.25"),
        ("strict_rate_iou_050", "IoU ≥ 0.50"),
    )
    for offset, (column, label) in zip((-width, 0, width), rate_columns):
        bars = axis.bar(
            [value + offset for value in x],
            [float(row[column]) for row in metrics],
            width,
            label=label,
        )
        axis.bar_label(bars, labels=[f"{bar.get_height():.0%}" for bar in bars], padding=2, fontsize=8)
    axis.set_xticks(x, names)
    axis.set_ylim(0, 1.08)
    axis.set_ylabel("Success rate")
    axis.set_title("Success Rates Using Identical IoU Thresholds")
    axis.legend()
    axis.grid(axis="y", alpha=0.25)
    figure.tight_layout()
    figure.savefig(output_dir / "success_rates_by_model.png", dpi=200)
    plt.close(figure)

    figure, axis = plt.subplots(figsize=(11, 6))
    bottoms = [0] * len(metrics)
    palette = {
        "failed": "#991b1b",
        "poor": "#ef4444",
        "weak": "#f59e0b",
        "primary": "#3b82f6",
        "strict": "#16a34a",
    }
    for quality in QUALITY_ORDER:
        values = [quality_counts[str(row["model_key"])][quality] for row in metrics]
        axis.bar(names, values, bottom=bottoms, label=quality.title(), color=palette[quality])
        bottoms = [bottom + value for bottom, value in zip(bottoms, values)]
    axis.set_ylabel("Images")
    axis.set_title("Bounding-Box Quality Distribution")
    axis.legend(ncol=5, loc="upper center", bbox_to_anchor=(0.5, 1.13))
    axis.grid(axis="y", alpha=0.2)
    figure.tight_layout()
    figure.savefig(output_dir / "bbox_quality_distribution.png", dpi=200)
    plt.close(figure)


def write_markdown(path: Path, metrics: list[dict[str, object]]) -> None:
    lines = [
        "# Final four-model metrics",
        "",
        "All models are evaluated on the same 105-image benchmark and the same corrected ground-truth boxes.",
        "",
        "| Model | Mean IoU | Median IoU | IoU ≥ 0.10 | IoU ≥ 0.25 | IoU ≥ 0.50 | Failures |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in metrics:
        lines.append(
            f"| {row['model_name']} | {float(row['mean_iou']):.3f} | "
            f"{float(row['median_iou']):.3f} | {float(row['weak_rate_iou_010']):.1%} | "
            f"{float(row['primary_rate_iou_025']):.1%} | "
            f"{float(row['strict_rate_iou_050']):.1%} | {row['prediction_failures']} |"
        )
    lines.extend(
        [
            "",
            "The CSV files in `examples/outputs/` are the authoritative per-image predictions.",
            "Re-run this report after regenerating any model result.",
            "Prompt-category diagnostics and guided-pipeline uplift are available under `results/final/prompt_categories/`.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Root of the visual-grounding module",
    )
    parser.add_argument("--output-dir", type=Path, default=None)
    args = parser.parse_args()

    project_root = args.project_root.expanduser().resolve()
    output_dir = (args.output_dir or project_root / "results" / "final").resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    metrics, per_image, quality_counts = calculate(project_root)
    metric_columns = [
        "model_key",
        "model_name",
        "rows",
        "successful_predictions",
        "prediction_failures",
        "mean_iou",
        "median_iou",
        "weak_rate_iou_010",
        "primary_rate_iou_025",
        "strict_rate_iou_050",
        "source_csv",
    ]
    write_csv(output_dir / "final_metrics.csv", metrics, metric_columns)
    write_csv(
        output_dir / "per_image_iou.csv",
        per_image,
        list(per_image[0]),
    )
    create_plots(output_dir, metrics, quality_counts)
    write_markdown(output_dir / "README.md", metrics)
    print(f"Final metrics written to {output_dir}")


if __name__ == "__main__":
    main()
