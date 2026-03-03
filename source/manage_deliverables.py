import os
import pathlib
import re

import yaml

# --- CONFIGURATION ---
DEFAULT_DELIVERABLE_EXTENSIONS = ["pdf", "py", "xlsx", "zip"]

TOKEN_SANITIZE_REGEX = re.compile(r"[^a-z0-9_]+")
FRONT_MATTER_REGEX = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|$)", re.DOTALL)

# Assumes structure: project_root/source/_toc.yml
TOC_FILE = "source/_toc.yml"
# Must be inside source/ to be visible to Jupyter Book
MASTER_NOTEBOOK = "source/glue_factory.md"

def load_toc(path):
    if not pathlib.Path(path).exists():
        print(f"Error: {path} not found.")
        return {}
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def clean_id(directory_name):
    return directory_name.replace("-", "_").replace(" ", "_").lower()

def sanitize_token(value):
    token = str(value).strip().lower().replace("-", "_").replace(" ", "_")
    token = TOKEN_SANITIZE_REGEX.sub("_", token)
    token = re.sub(r"_+", "_", token).strip("_")
    return token

def compute_assignment_id(path):
    dir_name_str = str(path.as_posix())
    unique_id = clean_id(dir_name_str)
    path_parts = unique_id.split("/")

    try:
        return (
            path_parts[1].split("_")[-1][0:2]
            + path_parts[2].replace('m', '')
            + "_"
            + path_parts[4]
        )
    except IndexError:
        print(f"⚠️ Warning: Fallback ID for {path}")
        return unique_id.replace("/", "_")

def select_canonical_assignments(assignments):
    canonical_by_id = {}

    for path in assignments:
        assignment_id = compute_assignment_id(path)
        if assignment_id in canonical_by_id:
            print(
                f"⚠️ Warning: Multiple versions found for '{assignment_id}'. "
                f"Keeping {canonical_by_id[assignment_id].as_posix()} and "
                f"skipping {path.as_posix()}."
            )
            continue

        canonical_by_id[assignment_id] = path

    return canonical_by_id

def load_front_matter(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    match = FRONT_MATTER_REGEX.match(content)
    if not match:
        return {}

    data = yaml.safe_load(match.group(1)) or {}
    if not isinstance(data, dict):
        return {}
    return data

def parse_deliverable_definition(raw_item, path):
    if isinstance(raw_item, str):
        token = sanitize_token(raw_item)
    elif isinstance(raw_item, dict):
        if "key" in raw_item:
            token = sanitize_token(raw_item.get("key", ""))
        else:
            label = sanitize_token(raw_item.get("label") or raw_item.get("name") or "")
            ext = sanitize_token(raw_item.get("ext") or raw_item.get("type") or "")
            if not ext:
                print(
                    f"⚠️ Warning: Skipping deliverable without 'ext' "
                    f"in {path.name}: {raw_item}"
                )
                return None
            token = f"{label}_{ext}" if label else ext
    else:
        print(f"⚠️ Warning: Unsupported deliverable item in {path.name}: {raw_item}")
        return None

    if not token:
        print(f"⚠️ Warning: Empty deliverable token in {path.name}: {raw_item}")
        return None

    if "_" in token:
        label, ext = token.rsplit("_", 1)
    else:
        label, ext = "", token

    return {
        "token": token,
        "label": label,
        "ext": ext,
    }

def get_assignment_deliverables(path, assignment_id):
    front_matter = load_front_matter(path)
    raw_deliverables = front_matter.get("deliverables")

    if raw_deliverables is None:
        raw_deliverables = list(DEFAULT_DELIVERABLE_EXTENSIONS)
    elif not isinstance(raw_deliverables, list):
        print(
            f"⚠️ Warning: 'deliverables' is not a list "
            f"in {path.name}; using defaults."
        )
        raw_deliverables = list(DEFAULT_DELIVERABLE_EXTENSIONS)

    deliverables = []
    seen_tokens = set()

    for raw_item in raw_deliverables:
        parsed = parse_deliverable_definition(raw_item, path)
        if not parsed:
            continue

        token = parsed["token"]
        if token in seen_tokens:
            print(
                f"⚠️ Warning: Duplicate deliverable token '{token}' "
                f"in {path.name}; keeping first."
            )
            continue

        label = parsed["label"]
        ext = parsed["ext"]
        stem = f"{assignment_id}_{label}" if label else assignment_id

        deliverables.append({
            "token": token,
            "placeholder": f"deliverable_{token}",
            "glue_key": f"{assignment_id}_{token}",
            "filename": f"{stem}_username.{ext}",
        })
        seen_tokens.add(token)

    if not deliverables:
        print(f"⚠️ Warning: No valid deliverables for {path.name}; using defaults.")
        for ext in DEFAULT_DELIVERABLE_EXTENSIONS:
            deliverables.append({
                "token": ext,
                "placeholder": f"deliverable_{ext}",
                "glue_key": f"{assignment_id}_{ext}",
                "filename": f"{assignment_id}_username.{ext}",
            })

    return deliverables

def find_assignment_files(toc_data, base_path=pathlib.Path("./source")):
    found_files = []
    items = toc_data if isinstance(toc_data, list) else [toc_data]
    
    for item in items:
        target = item.get('file') or item.get('root')
        if target:
            target_path = base_path / f"{target}"
            if not target_path.suffix:
                target_path = target_path.with_suffix(".md")
            
            if target_path.exists() and "instructions" in target_path.name:
                found_files.append(target_path)

        for key in ['chapters', 'sections', 'parts']:
            if key in item:
                found_files.extend(find_assignment_files(item[key], base_path))
    return found_files

def generate_master_notebook(assignments):
    # Added 'orphan: true' so it builds even if not in TOC
    content = """---
orphan: true
mystnb:
    execution_mode: force
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Glue Factory

Auto-generated glue key definitions for deliverable filenames.

```{code-cell} python3
:tags: [remove-cell]

from myst_nb import glue
import pathlib

# GLUE FACTORY: Auto-generated variables
# DO NOT EDIT THIS CELL MANUALLY
#
# Instructor front-matter template in assignment markdown files:
#
# ---
# deliverables:
#   - report_pdf
#   - appendix_pdf
#   - analysis_py
#   - data_xlsx
# ---
#
# Also supported:
# deliverables:
#   - key: report_pdf
#   - label: analysis
#     ext: py

"""
    canonical_by_id = select_canonical_assignments(assignments)
    seen_glue_keys = set()

    for assignment_id, path in canonical_by_id.items():
        assignment_id = compute_assignment_id(path)
        deliverables = get_assignment_deliverables(path, assignment_id)

        content += f"# {assignment_id}\n"
        for deliverable in deliverables:
            glue_key = deliverable["glue_key"]
            if glue_key in seen_glue_keys:
                print(
                    f"⚠️ Warning: Duplicate glue key '{glue_key}' from "
                    f"{path.as_posix()}; skipping duplicate entry."
                )
                continue

            content += (
                f"glue('{glue_key}', "
                f"'{deliverable['filename']}', "
                "display=False)\n"
            )
            seen_glue_keys.add(glue_key)
        content += "\n"

    content += "```\n"
    with open(MASTER_NOTEBOOK, 'w') as f:
        f.write(content)
    print(f"✅ Generated Glue Factory: {MASTER_NOTEBOOK}")

def audit_and_fix_references(assignments):
    placeholder_regex = re.compile(r"\bdeliverable_([A-Za-z0-9_]+)\b")
    glue_regex = re.compile(r"({glue:[a-z]+})`([^`]+)`")

    master_notebook_path = pathlib.Path(MASTER_NOTEBOOK)
    canonical_by_id = select_canonical_assignments(assignments)
    canonical_deliverables = {
        assignment_id: get_assignment_deliverables(path, assignment_id)
        for assignment_id, path in canonical_by_id.items()
    }

    for path in assignments:
        assignment_id = compute_assignment_id(path)
        deliverables = canonical_deliverables.get(
            assignment_id,
            get_assignment_deliverables(path, assignment_id)
        )
        token_lookup = {item["token"]: item for item in deliverables}
        ordered_tokens = sorted(token_lookup.keys(), key=len, reverse=True)

        # 2. Calculate RELATIVE PATH to glue_factory
        # From source/Part.../doc.md to source/glue_factory.md
        try:
            rel_dir = os.path.relpath(master_notebook_path.parent, path.parent)
        except ValueError:
            rel_dir = str(master_notebook_path.parent)

        if rel_dir == ".":
            doc_ref = "glue_factory.md"
        else:
            # Join with forward slash for MyST compatibility
            doc_ref = pathlib.Path(rel_dir) / "glue_factory.md"
            doc_ref = doc_ref.as_posix()

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Step 1: Expand Universal Placeholders
        def expand_placeholder(match):
            token = sanitize_token(match.group(1))
            deliverable = token_lookup.get(token)
            if not deliverable:
                print(
                    f"⚠️ Warning: Unknown placeholder in {path.name}: "
                    f"deliverable_{token}"
                )
                return match.group(0)

            new_tag = f"{{glue:text}}`{doc_ref}::{deliverable['glue_key']}:`"
            print(f"   [EXPAND] {path.name}: deliverable_{token} -> {new_tag}")
            return new_tag

        content = placeholder_regex.sub(expand_placeholder, content)

        # Step 2: Fix/Update Existing References
        def infer_token(existing_id):
            normalized_id = sanitize_token(existing_id.rstrip(":"))

            if normalized_id in token_lookup:
                return normalized_id

            if normalized_id.startswith(f"{assignment_id}_"):
                normalized_id = normalized_id[len(assignment_id) + 1:]
                if normalized_id in token_lookup:
                    return normalized_id

            for token in ordered_tokens:
                if normalized_id.endswith(f"_{token}"):
                    return token

            return None

        def fix_reference(match):
            role = match.group(1)       # {glue:text}
            full_ref = match.group(2)

            if "::" in full_ref:
                existing_id = full_ref.split("::")[-1]
            else:
                existing_id = full_ref

            token = infer_token(existing_id)
            if not token:
                return match.group(0)

            new_tag = f"{role}`{doc_ref}::{token_lookup[token]['glue_key']}:`"
            
            # Check for changes
            if new_tag != match.group(0):
                normalized_id = sanitize_token(existing_id.rstrip(":"))
                if normalized_id != token_lookup[token]["glue_key"]:
                    print(
                        f"   [FIX]    {path.name}: ID '{existing_id}' -> "
                        f"'{token_lookup[token]['glue_key']}'"
                    )
                else:
                    print(
                        f"   [FIX]    {path.name}: Updated path/format -> "
                        f"'{doc_ref}'"
                    )
            
            return new_tag

        content = glue_regex.sub(fix_reference, content)

        if content != original_content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
        else:
             print(f"   [OK]     {path.as_posix()}")

def main():
    print("--- Starting Deliverable Manager ---")
    toc = load_toc(TOC_FILE)
    assignments = find_assignment_files(toc['parts'] if 'parts' in toc else toc)
    print(f"Found {len(assignments)} instruction files.")
    
    # detect duplicate short_ids and optionally eliminate extras
    unique = []
    seen = {}
    for path in assignments:
        dir_name_str = str(path.as_posix())
        unique_id = clean_id(dir_name_str)
        path_parts = unique_id.split("/")
        try:
            short_id = (
                path_parts[1].split("_")[-1][0:2]
                + path_parts[2].replace('m', '')
                + "_"
                + path_parts[4]
            )
        except IndexError:
            short_id = unique_id.replace("/", "_")

        if short_id in seen:
            seen[short_id].append(path)
        else:
            seen[short_id] = [path]
            unique.append(path)

    # warn about duplicates
    for sid, paths in seen.items():
        if len(paths) > 1:
            print(f"⚠️ Duplicate deliverable id '{sid}' found in: {', '.join(str(p) for p in paths)}")

    assignments = unique
    print(f"Processing {len(assignments)} unique instruction files after deduplication.")

    generate_master_notebook(assignments)
    
    print("Auditing Markdown files...")
    audit_and_fix_references(assignments)
    print("--- Done ---")

if __name__ == "__main__":
    main()