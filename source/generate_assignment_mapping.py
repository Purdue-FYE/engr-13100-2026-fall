#!/usr/bin/env python3
"""Generate grader/assignment_mapping.json for run_autograder.

This script reuses the schedule assignment generation internals so it can access
source_path metadata that is not persisted in schedule_assignments.csv.
"""

from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
GSA_PATH = (
    REPO_ROOT
    / "source"
    / "Part_00_Course_Resources"
    / "course_schedule"
    / "generate_schedule_assignments.py"
)
OUTPUT_JSON = REPO_ROOT / "grader" / "assignment_mapping.json"

PREFIX_RE = re.compile(r"^[A-Z]{2,3}\s+")


def load_gsa_module():
    spec = importlib.util.spec_from_file_location(
        "generate_schedule_assignments", GSA_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {GSA_PATH}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def strip_subject_prefix(assignment_id: str) -> str:
    # Gradescope assignment names are expected to be numeric-only IDs.
    return PREFIX_RE.sub("", assignment_id).strip()


def main() -> None:
    gsa = load_gsa_module()

    _, merged_rows = gsa.build_merged_rows()

    mapping: dict[str, str] = {}
    for row in merged_rows:
        source_path = (row.get("source_path") or "").strip()
        assignment_id = (row.get("assignment_id") or "").strip()
        name = (row.get("name") or "").strip()

        # Autograded assignments must point to a concrete task directory.
        if not source_path or "/tasks/" not in source_path:
            continue
        if not assignment_id or not name:
            continue

        numeric_id = strip_subject_prefix(assignment_id)
        key = f"{numeric_id}. {name}"
        value = str(Path(source_path).parent.as_posix())

        if key in mapping and mapping[key] != value:
            raise ValueError(
                f"Duplicate assignment title with different paths: {key} -> "
                f"{mapping[key]} vs {value}"
            )

        mapping[key] = value

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(dict(sorted(mapping.items())), f, indent=4)
        f.write("\n")

    print(f"Wrote {len(mapping)} mappings to {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
