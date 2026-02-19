import yaml
import pathlib
import re
import os

# --- CONFIGURATION ---
DELIVERABLE_TYPES = {
    "pdf":  "{dir_name}_username.pdf",
    "py":   "{dir_name}_username.py",
    "xlsx": "{dir_name}_username.xlsx",
    "zip":  "{dir_name}_username.zip"
}

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

```{code-cell} python3
:tags: [remove-cell]

from myst_nb import glue
import pathlib

# GLUE FACTORY: Auto-generated variables
# DO NOT EDIT THIS CELL MANUALLY

"""
    seen_ids = set()
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
             print(f"⚠️ Warning: Fallback ID for {path}")
             short_id = unique_id.replace("/", "_")

        if short_id in seen_ids:
            print(f"   [SKIP]   duplicate deliverable id '{short_id}' from {path}")
            continue
        seen_ids.add(short_id)

        content += f"# {short_id}\n"
        for suffix, pattern in DELIVERABLE_TYPES.items():
            filename = pattern.format(dir_name=short_id)
            glue_key = f"{short_id}_{suffix}"
            content += f"glue('{glue_key}', '{filename}', display=False)\n"
        content += "\n"

    content += "```\n"
    with open(MASTER_NOTEBOOK, 'w') as f:
        f.write(content)
    print(f"✅ Generated Glue Factory: {MASTER_NOTEBOOK}")

def audit_and_fix_references(assignments):
    suffixes_list = list(DELIVERABLE_TYPES.keys())
    suffixes_pattern = "|".join(suffixes_list)
    
    # Pattern 1: Universal Placeholders (e.g. deliverable_pdf)
    placeholder_regex = re.compile(rf"\bdeliverable_({suffixes_pattern})\b")

    # Pattern 2: Existing Glue Tags
    # Matches {glue:text}`[PATH::]ID_SUFFIX[:]?`
    # Captures the existing path (optional), ID part, and optional trailing colon
    glue_regex = re.compile(rf"({{glue:[a-z]+}})`(.*?)_({suffixes_pattern}):?`")

    master_notebook_path = pathlib.Path(MASTER_NOTEBOOK)

    for path in assignments:
        # 1. Calculate ID
        dir_name_str = str(path.as_posix())
        unique_id = clean_id(dir_name_str)
        path_parts = unique_id.split("/")
        try:
            correct_prefix = (
                path_parts[1].split("_")[-1][0:2]
                + path_parts[2].replace('m', '')
                + "_"
                + path_parts[4]
            )
        except IndexError:
            correct_prefix = unique_id.replace("/", "_")

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
            suffix = match.group(1)
            # Include .md in path and trailing colon
            new_tag = f"{{glue:text}}`{doc_ref}::{correct_prefix}_{suffix}:`"
            print(f"   [EXPAND] {path.name}: deliverable_{suffix} -> {new_tag}")
            return new_tag

        content = placeholder_regex.sub(expand_placeholder, content)

        # Step 2: Fix/Update Existing References
        def fix_reference(match):
            role = match.group(1)       # {glue:text}
            full_ref = match.group(2)   # e.g. ../glue_factory::py1_ind_1 OR py1_ind_1
            suffix = match.group(3)     # pdf
            
            # Extract just the ID if a path exists
            if "::" in full_ref:
                existing_id = full_ref.split("::")[-1]
            else:
                existing_id = full_ref

            # Rebuild with CURRENT relative path and CURRENT prefix AND trailing colon
            new_tag = f"{role}`{doc_ref}::{correct_prefix}_{suffix}:`"
            
            # Check for changes
            if new_tag != match.group(0):
                 if existing_id != correct_prefix:
                     print(f"   [FIX]    {path.name}: ID '{existing_id}' -> '{correct_prefix}'")
                 else:
                     print(f"   [FIX]    {path.name}: Updated path/format -> '{doc_ref}'")
            
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