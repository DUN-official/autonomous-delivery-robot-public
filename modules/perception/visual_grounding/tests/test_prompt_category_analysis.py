import importlib.util
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "analyze_prompt_category_performance.py"
SPEC = importlib.util.spec_from_file_location("prompt_category_analysis", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def test_prompt_categories_are_deterministic_and_multi_label():
    between = MODULE.prompt_categories("package between books and shoes")
    assert "spatial_relation" in between
    assert "multiple_reference_objects" in between
    assert "complex_instruction" in between
    assert "simple_target" not in between

    plural = MODULE.prompt_categories("packages on table")
    assert "spatial_relation" in plural
    assert "multi_instance_or_ordinal" in plural
    assert "complex_instruction" in plural

    assert MODULE.prompt_categories("elevator button panel") == [
        "all_prompts",
        "simple_target",
    ]

    for category, prompt in MODULE.CATEGORY_EXAMPLES.items():
        assert category in MODULE.prompt_categories(prompt)


def test_saved_results_produce_guided_spatial_uplift():
    project_root = Path(__file__).resolve().parents[1]
    assignments, metrics, uplift = MODULE.calculate_metrics(project_root)

    assert len(assignments) == 105
    assert len(metrics) == len(MODULE.CATEGORY_ORDER) * len(MODULE.MODEL_FILES)
    spatial = next(row for row in uplift if row["category_key"] == "spatial_relation")
    assert spatial["scenario_count"] == 27
    assert spatial["guided_uplift_primary_success_rate_iou_025"] > 0
