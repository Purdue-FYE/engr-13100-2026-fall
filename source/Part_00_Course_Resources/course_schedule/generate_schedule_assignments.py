#!/usr/bin/env python3
"""Generate temporary assignment CSVs from TOC structure and assignment pages.

Auto-generated fields:
- assignment_id (public format, e.g. EX 4.1.2)
- name
- points (defaults by type)
- type

Manual source of truth:
- source/Part_00_Course_Resources/course_schedule/schedule_assignments.csv

Deprecated input (ignored):
- assignment_overrides.csv in the same directory

Outputs are temporary build artifacts under source/_build/intermediate/course_schedule/:
- schedule_assignments.generated.csv (from TOC/task pages)
- schedule_assignments.merged.csv (generated rows merged with manual schedule_assignments.csv)
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
SOURCE_DIR = REPO_ROOT / "source"
TOC_PATH = SOURCE_DIR / "_toc.yml"
MANUAL_CSV = Path(__file__).resolve().parent / "schedule_assignments.csv"
OVERRIDES_CSV = Path(__file__).resolve().parent / "assignment_overrides.csv"
BUILD_DIR = SOURCE_DIR / "_build" / "intermediate" / "course_schedule"
GENERATED_CSV = BUILD_DIR / "schedule_assignments.generated.csv"
MERGED_CSV = BUILD_DIR / "schedule_assignments.merged.csv"

OUTPUT_COLUMNS = ["class_slot", "assignment_id", "name", "points", "type", "due_date"]

DEFAULT_POINTS_BY_TYPE = {
    "Pre-Class Assignment": "0",
    "Individual Assignment": "10",
    "Team Assignment": "20",
}

ASSIGNMENT_ANCHOR_RE = re.compile(r"^\(([A-Za-z0-9:_\-.]+)\)\s*=\s*$", re.MULTILINE)
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
PRE_TASK_RE = re.compile(r"/tasks/pre_(\d+)/")
IND_TASK_RE = re.compile(r"/tasks/ind_(\d+)/")
NUMERIC_TASK_RE = re.compile(r"/tasks/(\d+)/")
TEAM_TASK_RE = re.compile(r"/tasks/team_(\d+)/")


def _to_md_path(raw_file: str) -> Path:
    if raw_file.endswith(".md"):
        return SOURCE_DIR / raw_file
    return SOURCE_DIR / f"{raw_file}.md"


def _read_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _strip_front_matter(text: str) -> str:
    if not text.startswith("---"):
        return text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return text
    return parts[2].lstrip("\n")


def _extract_anchor_id(markdown_text: str) -> str:
    body = _strip_front_matter(markdown_text)
    match = ASSIGNMENT_ANCHOR_RE.search(body)
    return match.group(1).strip() if match else ""


def _extract_title(markdown_text: str, fallback: str) -> str:
    body = _strip_front_matter(markdown_text)
    match = H1_RE.search(body)
    if match:
        return match.group(1).strip()
    return fallback


def _is_assignment_candidate(path: Path) -> bool:
    path_posix = path.as_posix().lower()
    name = path.name.lower()

    if "part_00_course_resources" in path_posix:
        return False
    if "/in-class/" in path_posix or "/ica_" in path_posix:
        return False
    if "catme_inst.md" in path_posix:
        return False

    if name == "instructions.md":
        return True
    if name == "1.1_materials.md":
        return True
    if "_pcm_" in name:
        return True
    if name.endswith("_inst.md"):
        return True

    return False


def _module_prefix(chapter_file: str) -> str:
    if chapter_file.startswith("Part_02_Excel/"):
        return "EX"
    if chapter_file.startswith("Part_04_Python/"):
        return "PY"
    if chapter_file.startswith("Part_05_Team_Project/"):
        return "TP"
    if chapter_file.startswith("Part_01_Professional_Development/M2_Teaming/"):
        return "TM"
    if chapter_file.startswith("Part_01_Professional_Development/"):
        return "PP"
    return "AS"


def _infer_type(path: Path) -> str:
    p = path.as_posix().lower()

    if "part_05_team_project" in p or "/tasks/team_" in p:
        return "Team Assignment"
    if IND_TASK_RE.search(p) or NUMERIC_TASK_RE.search(p):
        return "Individual Assignment"
    return "Pre-Class Assignment"


def _extract_module_id(path: Path) -> str:
    return next((part for part in path.parts if re.fullmatch(r"M\d+", part)), "M0")


def _derive_kind_from_path(path: Path) -> str:
    p = path.as_posix()
    name = path.name.lower()

    if name == "1.1_materials.md" or "_pcm_" in name:
        return "pre-class-mats"

    match = PRE_TASK_RE.search(p)
    if match:
        return f"PCA{match.group(1)}"

    match = IND_TASK_RE.search(p)
    if match:
        return f"A{match.group(1)}"

    match = TEAM_TASK_RE.search(p)
    if match:
        return f"TA{match.group(1)}"

    match = NUMERIC_TASK_RE.search(p)
    if match:
        return f"A{match.group(1)}"

    return path.stem.upper().replace("-", "_")


def _build_canonical_id(anchor_id: str, path: Path, chapter_prefix: str) -> str:
    if anchor_id:
        return anchor_id

    module_id = _extract_module_id(path)
    kind = _derive_kind_from_path(path)
    return f"{chapter_prefix}:{module_id}:{kind}"


def _walk_nested_sections(node: dict[str, Any]) -> list[dict[str, Any]]:
    return [section for section in node.get("sections", []) if isinstance(section, dict)]


def _build_row(
    path: Path,
    prefix: str,
    chapter_idx: int,
    section_idx: int,
    item_idx: int,
) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    anchor_id = _extract_anchor_id(text)
    canonical_id = _build_canonical_id(anchor_id, path, prefix)
    title = _extract_title(text, fallback=path.stem.replace("_", " ").title())
    assignment_type = _infer_type(path)

    return {
        "canonical_id": canonical_id,
        "assignment_id": f"{prefix} {chapter_idx}.{section_idx}.{item_idx}",
        "name": title,
        "points": DEFAULT_POINTS_BY_TYPE[assignment_type],
        "type": assignment_type,
        "class_slot": "",
        "due_date": "",
        "source_path": str(path.relative_to(REPO_ROOT).as_posix()),
        "manual_only": "false",
    }


def _collect_rows_from_toc(toc_data: dict[str, Any]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    chapter_index = 0

    for part in toc_data.get("parts", []):
        if not isinstance(part, dict):
            continue

        for chapter in part.get("chapters", []):
            if not isinstance(chapter, dict):
                continue

            chapter_file = chapter.get("file", "")
            if not isinstance(chapter_file, str):
                continue

            if not chapter_file.startswith(
                (
                    "Part_01_Professional_Development/",
                    "Part_02_Excel/",
                    "Part_03_AI/",
                    "Part_04_Python/",
                    "Part_05_Team_Project/",
                )
            ):
                continue

            chapter_index += 1
            prefix = _module_prefix(chapter_file)

            top_sections = [section for section in chapter.get("sections", []) if isinstance(section, dict)]
            for section_idx, section in enumerate(top_sections, start=1):
                section_file = section.get("file", "")
                nested_sections = _walk_nested_sections(section)

                if isinstance(section_file, str) and section_file:
                    section_path = _to_md_path(section_file)
                    if section_path.exists() and _is_assignment_candidate(section_path):
                        rows.append(
                            _build_row(
                                path=section_path,
                                prefix=prefix,
                                chapter_idx=chapter_index,
                                section_idx=section_idx,
                                item_idx=1,
                            )
                        )

                for item_idx, nested in enumerate(nested_sections, start=1):
                    nested_file = nested.get("file", "")
                    if not isinstance(nested_file, str) or not nested_file:
                        continue

                    nested_path = _to_md_path(nested_file)
                    if not nested_path.exists() or not _is_assignment_candidate(nested_path):
                        continue

                    rows.append(
                        _build_row(
                            path=nested_path,
                            prefix=prefix,
                            chapter_idx=chapter_index,
                            section_idx=section_idx,
                            item_idx=item_idx,
                        )
                    )

    deduped: list[dict[str, str]] = []
    seen: set[str] = set()
    for row in rows:
        canonical_id = row["canonical_id"]
        if canonical_id in seen:
            continue
        deduped.append(row)
        seen.add(canonical_id)

    return deduped


def _warn_if_deprecated_overrides_present(path: Path) -> None:
    if not path.exists():
        return

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        has_data_rows = any(
            any((value or "").strip() for value in row.values()) for row in reader
        )

    if has_data_rows:
        print(
            "Warning: assignment_overrides.csv is deprecated and ignored. "
            "Move any remaining values into schedule_assignments.csv.",
            file=sys.stderr,
        )


def _load_manual_schedule(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows: list[dict[str, str]] = []
        for row in reader:
            cleaned = {key: (value or "").strip() for key, value in row.items()}
            if not any(cleaned.values()):
                continue
            if not cleaned.get("assignment_id"):
                continue
            rows.append(cleaned)
    return rows


def _apply_manual_schedule(
    generated_rows: list[dict[str, str]],
    manual_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    merged_rows = [dict(row) for row in generated_rows]
    by_assignment_id = {row["assignment_id"]: row for row in merged_rows}

    for manual in manual_rows:
        assignment_id = manual.get("assignment_id", "")
        if not assignment_id:
            continue

        target = by_assignment_id.get(assignment_id)
        if target is None:
            appended = {
                "canonical_id": manual.get("canonical_id", ""),
                "assignment_id": assignment_id,
                "name": manual.get("name", ""),
                "points": manual.get("points", ""),
                "type": manual.get("type", ""),
                "class_slot": manual.get("class_slot", ""),
                "due_date": manual.get("due_date", ""),
                "source_path": manual.get("source_path", ""),
                "manual_only": "true",
            }
            merged_rows.append(appended)
            by_assignment_id[assignment_id] = appended
            continue

        for key in ["name", "points", "type", "class_slot", "due_date"]:
            value = manual.get(key, "")
            if value:
                target[key] = value

    return merged_rows


def _slot_sort_key(slot: str) -> tuple[int, int]:
    slot = slot.strip()
    match = re.fullmatch(r"(\d+)([AB])", slot)
    if not match:
        return (10**9, 10**9)

    week = int(match.group(1))
    meeting = 0 if match.group(2) == "A" else 1
    return (week, meeting)


def _sort_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    def key(row: dict[str, str]) -> tuple[Any, ...]:
        return (
            _slot_sort_key(row.get("class_slot", "")),
            row.get("assignment_id", ""),
            row.get("name", ""),
        )

    return sorted(rows, key=key)


def _write_output(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in OUTPUT_COLUMNS})


def build_merged_rows() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    toc_data = _read_yaml(TOC_PATH)
    generated_rows = _collect_rows_from_toc(toc_data)
    _warn_if_deprecated_overrides_present(OVERRIDES_CSV)

    manual_rows = _load_manual_schedule(MANUAL_CSV)
    merged_rows = _apply_manual_schedule(generated_rows, manual_rows)

    return generated_rows, merged_rows


def main() -> None:
    if not TOC_PATH.exists():
        raise FileNotFoundError(f"Missing TOC file: {TOC_PATH}")

    generated_rows, merged_rows = build_merged_rows()
    generated_output_rows = _sort_rows(generated_rows)
    merged_output_rows = _sort_rows(merged_rows)

    _write_output(GENERATED_CSV, generated_output_rows)
    _write_output(MERGED_CSV, merged_output_rows)

    unresolved = [
        row for row in merged_output_rows if not row.get("class_slot") or not row.get("due_date")
    ]
    print(f"Wrote assignments CSVs: {GENERATED_CSV} and {MERGED_CSV}")
    print(
        f"Merged rows: {len(merged_output_rows)} (manual review needed for {len(unresolved)} rows)"
    )


if __name__ == "__main__":
    main()
