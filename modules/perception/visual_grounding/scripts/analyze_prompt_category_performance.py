"""Analyze saved grounding results by prompt category."""

from __future__ import annotations

import argparse
import csv
import math
import re
from collections import defaultdict
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
UNGUIDED_MODELS = ("grounding_dino", "owlvit", "gpt_vision")
CATEGORY_ORDER = (
    "all_prompts",
    "simple_target",
    "spatial_relation",
    "attribute_selection",
    "multiple_reference_objects",
    "multi_instance_or_ordinal",
    "negation",
    "occlusion",
    "complex_instruction",
)
CATEGORY_LABELS = {
    "all_prompts": "All prompts",
    "simple_target": "Direct target",
    "spatial_relation": "Spatial relation",
    "attribute_selection": "Attribute selection",
    "multiple_reference_objects": "Multiple references",
    "multi_instance_or_ordinal": "Multi-instance / ordinal",
    "negation": "Negation",
    "occlusion": "Occlusion",
    "complex_instruction": "Complex instruction",
}
CATEGORY_DEFINITIONS = {
    "all_prompts": "Every benchmark prompt.",
    "simple_target": "Target naming without a spatial, attribute, multiplicity, negation, or occlusion constraint.",
    "spatial_relation": "Uses a location, direction, proximity, support, or ordinal spatial relation.",
    "attribute_selection": "Uses colour, clothing, posture, or visible-state information to select the target.",
    "multiple_reference_objects": "Uses two or more reference objects or a chained relation.",
    "multi_instance_or_ordinal": "Requests plural targets or selects one instance by rank, such as second closest.",
    "negation": "Excludes a target by a negative constraint.",
    "occlusion": "Describes a target as covered, hidden, or occluded.",
    "complex_instruction": "Combines at least two independent constraints, two spatial operators, or multiple references.",
}
CATEGORY_EXAMPLES = {
    "all_prompts": "man by door",
    "simple_target": "elevator button panel",
    "spatial_relation": "package beside the chair",
    "attribute_selection": "man in blue",
    "multiple_reference_objects": "package between books and shoes",
    "multi_instance_or_ordinal": "second closest package",
    "negation": "package not red",
    "occlusion": "package partially covered by chair",
    "complex_instruction": "man by the elevator green shirt",
}
MODEL_COLORS = {
    "grounding_dino": "#7c3aed",
    "owlvit": "#0891b2",
    "gpt_vision": "#db2777",
    "gpt_guided_owlvit": "#16a34a",
}


def parse_float(value: object, default: float = 0.0) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return default
    return parsed if math.isfinite(parsed) else default


def parse_optional_bool(value: object) -> bool | None:
    normalized = str(value or "").strip().lower()
    if normalized in {"true", "1", "yes"}:
        return True
    if normalized in {"false", "0", "no"}:
        return False
    return None


def has_valid_prediction(row: dict[str, str]) -> bool:
    if str(row.get("status", "")).strip().lower() != "success":
        return False
    coordinates = [
        parse_float(row.get(key), math.nan)
        for key in ("pred_x_min", "pred_y_min", "pred_x_max", "pred_y_max")
    ]
    return (
        all(math.isfinite(value) for value in coordinates)
        and coordinates[2] > coordinates[0]
        and coordinates[3] > coordinates[1]
    )


def prompt_features(prompt: str) -> dict[str, bool | int]:
    text = f" {re.sub(r'[^a-z0-9]+', ' ', prompt.lower()).strip()} "
    spatial_terms = (
        " by ", " beside ", " on ", " under ", " at end ", " right ",
        " left ", " between ", " opposite ", " in front ", " infront ",
        " closest ", " near ", " behind ", " above ", " below ", " inside ",
    )
    attribute_terms = (
        " red ", " green ", " blue ", " grey ", " gray ", " white ",
        " shirt ", " top ", " sitting ", " standing ",
    )
    relation_count = sum(term in text for term in spatial_terms)
    multiple_references = (
        (" between " in text and " and " in text)
        or (" by wall " in text and " opposite " in text)
    )
    multi_instance = (
        re.search(r"\bpackages\b", text) is not None
        or re.search(r"\b(second|third|fourth)\b", text) is not None
    )
    negation = any(term in text for term in (" not ", " without ", " excluding "))
    occlusion = any(term in text for term in (" covered ", " hidden ", " occluded "))
    spatial = relation_count > 0
    attribute = any(term in text for term in attribute_terms)
    independent_constraints = sum((spatial, attribute, multi_instance, negation, occlusion))
    complex_instruction = multiple_references or relation_count >= 2 or independent_constraints >= 2
    return {
        "spatial_relation": spatial,
        "attribute_selection": attribute,
        "multiple_reference_objects": multiple_references,
        "multi_instance_or_ordinal": multi_instance,
        "negation": negation,
        "occlusion": occlusion,
        "complex_instruction": complex_instruction,
        "spatial_operator_count": relation_count,
    }


def prompt_categories(prompt: str) -> list[str]:
    features = prompt_features(prompt)
    categories = ["all_prompts"]
    reasoning_categories = CATEGORY_ORDER[2:-1]
    categories.extend(key for key in reasoning_categories if features[key])
    if not any(features[key] for key in reasoning_categories):
        categories.append("simple_target")
    if features["complex_instruction"]:
        categories.append("complex_instruction")
    return [key for key in CATEGORY_ORDER if key in categories]


def load_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise FileNotFoundError(f"Required CSV is missing: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"Required CSV is empty: {path}")
    return rows


def write_csv(path: Path, rows: list[dict[str, object]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def prepare_data(project_root: Path):
    benchmark_path = project_root / "examples" / "grounding_benchmark_with_task_parser.csv"
    benchmark = load_csv(benchmark_path)
    by_image = {row["image_id"]: row for row in benchmark}
    if len(by_image) != len(benchmark):
        raise ValueError("Benchmark contains duplicate image_id values")

    assignments: list[dict[str, object]] = []
    categories_by_image: dict[str, list[str]] = {}
    for row in benchmark:
        image_id = row["image_id"]
        prompt = (row.get("original_grounding_prompt") or row.get("grounding_prompt") or "").strip()
        match = re.match(r"(vid_res_\d+)", image_id)
        scenario_id = match.group(1) if match else re.sub(r"_frame_\d+$", "", image_id)
        features = prompt_features(prompt)
        categories = prompt_categories(prompt)
        categories_by_image[image_id] = categories
        assignments.append(
            {
                "image_id": image_id,
                "scenario_id": scenario_id,
                "prompt": prompt,
                "categories": " | ".join(CATEGORY_LABELS[key] for key in categories),
                **features,
            }
        )

    model_rows: dict[str, list[dict[str, str]]] = {}
    expected_ids = set(by_image)
    for model_key, (_, relative_path) in MODEL_FILES.items():
        rows = load_csv(project_root / relative_path)
        image_ids = [row.get("image_id", "") for row in rows]
        if len(image_ids) != len(set(image_ids)):
            raise ValueError(f"{model_key} contains duplicate image_id values")
        if set(image_ids) != expected_ids:
            raise ValueError(f"{model_key} does not use the benchmark image set")
        model_rows[model_key] = rows
    return by_image, assignments, categories_by_image, model_rows


def calculate_metrics(project_root: Path):
    benchmark, assignments, categories_by_image, model_rows = prepare_data(project_root)
    scenario_by_image = {row["image_id"]: row["scenario_id"] for row in assignments}
    metrics: list[dict[str, object]] = []

    for category in CATEGORY_ORDER:
        category_ids = {
            image_id for image_id, keys in categories_by_image.items() if category in keys
        }
        for model_key, (model_name, source_csv) in MODEL_FILES.items():
            selected = [row for row in model_rows[model_key] if row["image_id"] in category_ids]
            if not selected:
                continue
            ious = [parse_float(row.get("iou")) for row in selected]
            valid = [has_valid_prediction(row) for row in selected]
            target_values = [parse_optional_bool(row.get("target_correct")) for row in selected]
            target_known = [value for value in target_values if value is not None]
            relation_values = [parse_optional_bool(row.get("relation_match")) for row in selected]
            relation_known = [value for value in relation_values if value is not None]
            metrics.append(
                {
                    "category_key": category,
                    "category": CATEGORY_LABELS[category],
                    "model_key": model_key,
                    "model": model_name,
                    "sample_count": len(selected),
                    "scenario_count": len({scenario_by_image[row["image_id"]] for row in selected}),
                    "mean_iou": mean(ious),
                    "median_iou": median(ious),
                    "prediction_success_rate": sum(valid) / len(valid),
                    "primary_success_rate_iou_025": sum(value >= 0.25 for value in ious) / len(ious),
                    "strict_success_rate_iou_050": sum(value >= 0.50 for value in ious) / len(ious),
                    "target_correct_rate": (
                        sum(target_known) / len(target_known) if target_known else ""
                    ),
                    "relation_match_rate": (
                        sum(relation_known) / len(relation_known) if relation_known else ""
                    ),
                    "source_csv": source_csv,
                }
            )

    indexed = {(row["category_key"], row["model_key"]): row for row in metrics}
    uplift: list[dict[str, object]] = []
    for category in CATEGORY_ORDER:
        guided = indexed.get((category, "gpt_guided_owlvit"))
        baselines = [indexed[(category, key)] for key in UNGUIDED_MODELS if (category, key) in indexed]
        if not guided or not baselines:
            continue
        row: dict[str, object] = {
            "category_key": category,
            "category": CATEGORY_LABELS[category],
            "sample_count": guided["sample_count"],
            "scenario_count": guided["scenario_count"],
        }
        for metric in (
            "mean_iou",
            "primary_success_rate_iou_025",
            "strict_success_rate_iou_050",
        ):
            best = max(baselines, key=lambda item: float(item[metric]))
            row[f"guided_{metric}"] = guided[metric]
            row[f"best_unguided_{metric}"] = best[metric]
            row[f"best_unguided_{metric}_model"] = best["model"]
            row[f"guided_uplift_{metric}"] = float(guided[metric]) - float(best[metric])
        uplift.append(row)
    return assignments, metrics, uplift


def create_plots(output_dir: Path, metrics: list[dict[str, object]], uplift: list[dict[str, object]]) -> None:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError as exc:
        raise RuntimeError("Plot generation requires the evaluation dependencies") from exc

    indexed = {(row["category_key"], row["model_key"]): row for row in metrics}
    categories = [key for key in CATEGORY_ORDER if (key, "gpt_guided_owlvit") in indexed]
    models = list(MODEL_FILES)
    matrix = np.array(
        [[float(indexed[(category, model)]["mean_iou"]) for model in models] for category in categories]
    )
    figure, axis = plt.subplots(figsize=(10.5, 7.2))
    image = axis.imshow(matrix, cmap="YlGn", vmin=0, vmax=max(0.7, float(matrix.max())))
    axis.set_xticks(range(len(models)), [MODEL_FILES[key][0] for key in models], rotation=18, ha="right")
    axis.set_yticks(range(len(categories)), [CATEGORY_LABELS[key] for key in categories])
    axis.set_title("Mean IoU by Prompt Category")
    for y in range(len(categories)):
        for x in range(len(models)):
            sample_count = indexed[(categories[y], models[x])]["sample_count"]
            axis.text(x, y, f"{matrix[y, x]:.3f}\nn={sample_count}", ha="center", va="center", fontsize=8)
    figure.colorbar(image, ax=axis, label="Mean IoU", shrink=0.82)
    figure.tight_layout()
    figure.savefig(output_dir / "prompt_category_mean_iou_heatmap.png", dpi=220)
    plt.close(figure)

    x_values = np.arange(len(categories))
    width = 0.19
    figure, axis = plt.subplots(figsize=(14, 7.2))
    for index, model in enumerate(models):
        values = [float(indexed[(category, model)]["primary_success_rate_iou_025"]) for category in categories]
        axis.bar(
            x_values + (index - 1.5) * width,
            values,
            width,
            label=MODEL_FILES[model][0],
            color=MODEL_COLORS[model],
        )
    axis.set_xticks(
        x_values,
        [
            f"{CATEGORY_LABELS[key]}\n(n={indexed[(key, 'gpt_guided_owlvit')]['sample_count']})"
            for key in categories
        ],
        rotation=25,
        ha="right",
    )
    axis.set_ylim(0, 1.06)
    axis.set_ylabel("Primary localization success rate (IoU ≥ 0.25)")
    axis.set_title("Localization Success by Prompt Category")
    axis.grid(axis="y", alpha=0.25)
    axis.legend(ncol=2)
    figure.tight_layout()
    figure.savefig(output_dir / "prompt_category_primary_success.png", dpi=220)
    plt.close(figure)

    uplift_categories = [row for row in uplift if row["category_key"] != "all_prompts"]
    labels = [f"{row['category']} (n={row['sample_count']})" for row in uplift_categories]
    primary = [float(row["guided_uplift_primary_success_rate_iou_025"]) for row in uplift_categories]
    strict = [float(row["guided_uplift_strict_success_rate_iou_050"]) for row in uplift_categories]
    y_values = np.arange(len(labels))
    figure, axis = plt.subplots(figsize=(11, 7))
    axis.barh(y_values - 0.18, primary, 0.36, label="Primary success uplift", color="#16a34a")
    axis.barh(y_values + 0.18, strict, 0.36, label="Strict success uplift", color="#2563eb")
    axis.axvline(0, color="#111827", linewidth=1)
    axis.set_yticks(y_values, labels)
    axis.invert_yaxis()
    axis.set_xlabel("GPT-guided OWL-ViT minus best unguided model (percentage points)")
    axis.xaxis.set_major_formatter(lambda value, position: f"{value * 100:.0f}")
    axis.set_title("Guided Pipeline Uplift by Prompt Category")
    axis.grid(axis="x", alpha=0.25)
    axis.legend()
    figure.tight_layout()
    figure.savefig(output_dir / "gpt_guided_uplift_by_prompt_category.png", dpi=220)
    plt.close(figure)


def write_report(path: Path, metrics: list[dict[str, object]], uplift: list[dict[str, object]]) -> None:
    indexed = {(row["category_key"], row["model_key"]): row for row in metrics}
    lines = [
        "# Prompt-category performance analysis",
        "",
        "This report uses the existing saved predictions. It does not rerun a model and is separate from the live application.",
        "",
        "## Headline results",
        "",
        "| Model | Mean IoU | IoU ≥ 0.25 | IoU ≥ 0.50 |",
        "|---|---:|---:|---:|",
    ]
    for model_key, (model_name, _) in MODEL_FILES.items():
        row = indexed[("all_prompts", model_key)]
        lines.append(
            f"| {model_name} | {float(row['mean_iou']):.3f} | "
            f"{float(row['primary_success_rate_iou_025']):.1%} | "
            f"{float(row['strict_success_rate_iou_050']):.1%} |"
        )

    lines.extend(["", "## What the category results show", ""])
    for model_key, (model_name, _) in MODEL_FILES.items():
        candidates = [
            row for row in metrics
            if row["model_key"] == model_key
            and row["category_key"] != "all_prompts"
            and int(row["scenario_count"]) >= 2
        ]
        strongest = max(candidates, key=lambda row: float(row["primary_success_rate_iou_025"]))
        weakest = min(candidates, key=lambda row: float(row["primary_success_rate_iou_025"]))
        lines.append(
            f"- **{model_name}:** strongest primary success on {strongest['category']} "
            f"({float(strongest['primary_success_rate_iou_025']):.1%}); weakest on "
            f"{weakest['category']} ({float(weakest['primary_success_rate_iou_025']):.1%})."
        )

    positive_primary = [row for row in uplift if float(row["guided_uplift_primary_success_rate_iou_025"]) > 0]
    non_positive_primary = [
        row for row in uplift
        if row["category_key"] != "all_prompts"
        and float(row["guided_uplift_primary_success_rate_iou_025"]) <= 0
    ]
    best_primary = max(uplift, key=lambda row: float(row["guided_uplift_primary_success_rate_iou_025"]))
    spatial = next(row for row in uplift if row["category_key"] == "spatial_relation")
    complex_row = next(row for row in uplift if row["category_key"] == "complex_instruction")
    lines.extend(
        [
            "",
            "## Why the guided setup is justified",
            "",
            f"GPT-guided OWL-ViT exceeds the best unguided result on primary localization in "
            f"{len(positive_primary)} of {len(uplift)} reported category views. Its largest primary gain is "
            f"{float(best_primary['guided_uplift_primary_success_rate_iou_025']):+.1%} on "
            f"{best_primary['category']}.",
            "",
            f"For spatial prompts, guided primary success is "
            f"{float(spatial['guided_primary_success_rate_iou_025']):.1%}, compared with "
            f"{float(spatial['best_unguided_primary_success_rate_iou_025']):.1%} for the best unguided model. "
            f"For complex prompts, the corresponding values are "
            f"{float(complex_row['guided_primary_success_rate_iou_025']):.1%} and "
            f"{float(complex_row['best_unguided_primary_success_rate_iou_025']):.1%}.",
            "",
            "The guided configuration is not uniformly superior. It does not exceed the best unguided "
            "primary-success result for "
            + ", ".join(str(row["category"]) for row in non_positive_primary)
            + ". This supports retaining selectable backends and treating the guided pipeline as the "
            "accuracy-oriented choice for relation-heavy prompts, not as proof that it is optimal for every prompt.",
            "",
            "The component pattern supports the architecture: GPT Vision is relatively effective at interpreting "
            "which object the instruction refers to, while OWL-ViT provides detector proposals and tighter boxes. "
            "The guided pipeline uses the language-aware stage to select/refine OWL-ViT candidates, addressing "
            "the standalone models' complementary weaknesses.",
            "",
            "## Prompt taxonomy",
            "",
            "Categories are deterministic, multi-label, and defined before aggregation. A prompt may therefore "
            "appear in more than one category.",
            "",
        ]
    )
    for key in CATEGORY_ORDER:
        lines.append(
            f"- **{CATEGORY_LABELS[key]}:** {CATEGORY_DEFINITIONS[key]} "
            f"Example: *{CATEGORY_EXAMPLES[key]}*."
        )

    lines.extend(
        [
            "",
            "## Interpretation limits",
            "",
            "- These are historical saved outputs, not a rerun of the latest Quality profile.",
            "- The benchmark contains 105 frames from 35 short scenarios. Adjacent frames are related observations.",
            "- Small categories, especially negation and multiple-reference prompts, should be treated as directional evidence rather than a final generalization claim.",
            "- Category overlap means results answer different diagnostic questions and should not be added together.",
            "- Target-correct and relation-match fields come from different evaluation procedures and are retained in the CSV but are not plotted as directly comparable measures.",
            "- YOLO is not included because there is no saved YOLO result CSV for this benchmark.",
            "- Latency was not measured in the saved result files, so this analysis supports accuracy claims only.",
            "",
            "The frame-level category assignments are recorded in `prompt_category_assignments.csv`; the full metrics and guided uplift values are in the companion CSV files.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output-dir", type=Path, default=None)
    args = parser.parse_args()
    project_root = args.project_root.expanduser().resolve()
    output_dir = (args.output_dir or project_root / "results" / "final" / "prompt_categories").resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    assignments, metrics, uplift = calculate_metrics(project_root)
    assignment_columns = [
        "image_id", "scenario_id", "prompt", "categories", "spatial_relation",
        "attribute_selection", "multiple_reference_objects", "multi_instance_or_ordinal",
        "negation", "occlusion", "complex_instruction", "spatial_operator_count",
    ]
    metric_columns = [
        "category_key", "category", "model_key", "model", "sample_count", "scenario_count",
        "mean_iou", "median_iou", "prediction_success_rate",
        "primary_success_rate_iou_025", "strict_success_rate_iou_050",
        "target_correct_rate", "relation_match_rate", "source_csv",
    ]
    uplift_columns = list(uplift[0])
    write_csv(output_dir / "prompt_category_assignments.csv", assignments, assignment_columns)
    write_csv(output_dir / "prompt_category_metrics.csv", metrics, metric_columns)
    write_csv(output_dir / "gpt_guided_uplift.csv", uplift, uplift_columns)
    create_plots(output_dir, metrics, uplift)
    write_report(output_dir / "README.md", metrics, uplift)
    print(f"Prompt-category analysis written to {output_dir}")


if __name__ == "__main__":
    main()
