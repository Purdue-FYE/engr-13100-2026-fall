"""Create archives from the exercise tests that are suitable for upload to
Gradescope.
"""

import os
import subprocess
from io import BytesIO
from pathlib import Path
from sys import argv
from zipfile import ZIP_DEFLATED, ZipFile

import yaml
from jinja2 import Environment, FileSystemLoader

EXERCISES = argv[1:]

# Grab the secret from the Codespace environment
DEPLOY_KEY = os.environ.get("GRADESCOPE_DEPLOY_KEY")
if not DEPLOY_KEY:
    print(
        "WARNING: GRADESCOPE_DEPLOY_KEY environment variable is not set. \
          deploy_key will NOT be included in the zip!"
    )

commit_id = subprocess.check_output(
    ["git", "rev-parse", "--short", "HEAD"],
    text=True,
).strip()

# Create a Jinja2 environment with custom delimiters.
j2_env = Environment(
    loader=FileSystemLoader("."),
    variable_start_string='{{"',
    variable_end_string='"}}',
)


def build_shared_autograder_zip() -> None:
    """Build a single shared autograder package named by commit id."""
    dst_dir = Path("grader")
    dst_dir.mkdir(parents=True, exist_ok=True)

    for old_zip in dst_dir.glob("autograder*.zip"):
        old_zip.unlink()

    zip_file_name = f"autograder_{commit_id}.zip"
    zip_file_path = dst_dir / zip_file_name

    with ZipFile(zip_file_path, "w", compression=ZIP_DEFLATED) as fo:
        # Write the deploy key directly to the root of the zip archive
        if DEPLOY_KEY:
            fo.writestr("deploy_key", f"{DEPLOY_KEY}\n")
        for path in sorted(Path("grader").glob("**/*")):
            if path.is_file():
                if path.name.startswith("autograder_") and path.suffix == ".zip":
                    continue
                # Place grader files at archive root as expected by Gradescope.
                fo.write(path, path.relative_to("grader"))

    print(f"built: {zip_file_path}")


def resolve_exercise_dir(dst_dir: Path) -> Path:
    """Resolve the source exercise directory from a build destination path.

    Supports legacy destination roots like `source/_build/graders/...` and
    custom roots such as `source/.grader_runtime/...`.
    """

    parts = dst_dir.parts

    # Prefer a Part_* anchor because it is stable across build roots.
    part_index = next((i for i, p in enumerate(parts) if p.startswith("Part_")), None)
    if part_index is None:
        raise ValueError(f"Could not resolve exercise path from destination: {dst_dir}")

    return Path("source", *parts[part_index:])


if not EXERCISES:
    build_shared_autograder_zip()
    raise SystemExit(0)

for exercise in EXERCISES:
    dst_dir = Path(exercise)
    dst_dir.mkdir(parents=True, exist_ok=True)

    exercise_dir = resolve_exercise_dir(dst_dir)
    part, unit, _, number, name = exercise_dir.parts[-5:]
    if "Excel" in part:
        unit = unit.replace("M", "ex")
    elif "Python" in part:
        unit = unit.replace("M", "py")
    elif "Team_Project" in part:
        unit = unit.replace("M", "tp")
    elif "MATLAB" in part:
        unit = unit.replace("M", "ma")

    zip_file_name = f"autograder_{unit}.{number}_{name}_{commit_id}.zip"
    zip_file_path = dst_dir / zip_file_name
    unzip_dir = zip_file_path.with_suffix("")

    # Create the results directory.
    (dst_dir / "results").mkdir(exist_ok=True)

    # Skip if already made.
    if zip_file_path.exists():
        print(f"no update: {zip_file_name}")
        continue

    # Skip if no tests.
    if not (exercise_dir / "test_config.py").exists():
        print(f"no grader config: {zip_file_name}")
        continue

    print(f"building: {zip_file_name}")

    # Load the task parameters from the instruction's YAML configuration.
    with open(exercise_dir / "instructions.md") as f:
        try:
            parameters = yaml.safe_load(f.read().split("---")[1])["myst"][
                "substitutions"
            ]
        except KeyError:
            parameters = {}

    with ZipFile(zip_file_path, "w", compression=ZIP_DEFLATED) as fo:
        # Write the deploy key directly to the root of the zip archive
        if DEPLOY_KEY:
            fo.writestr("deploy_key", f"{DEPLOY_KEY}\n")

        for path in Path("grader").iterdir():
            if path.is_file():
                fo.write(path, path.name)

        # Add source files to archive.
        for path in exercise_dir.iterdir():
            if path.is_dir() and "images" in path.name.lower():
                # Create and write image zip directly into fo
                img_zip_buffer = BytesIO()
                with ZipFile(img_zip_buffer, "w", compression=ZIP_DEFLATED) as img_zip:
                    for img_path in path.rglob("*"):
                        if img_path.is_file():
                            img_zip.write(
                                img_path,
                                img_path.relative_to(exercise_dir),
                            )
                img_zip_buffer.seek(0)
                fo.writestr(f"tests/{path.name}.zip", img_zip_buffer.read())
                continue

            if (
                path.suffix in (".py", ".txt", ".csv", ".png", ".jpg", ".xlsx", ".xlsm")
                and path.is_file()
            ):
                if path.name.endswith("solution.py"):
                    # Handle partial solutions
                    prefix = path.name.removesuffix("solution.py")
                    reference = j2_env.get_template(str(path)).render(**parameters)

                    # Change local imports to be relative imports
                    local_prefix = f"{unit}_{number}"
                    reference_lines = reference.splitlines()
                    for n, line in enumerate(reference_lines):
                        if line.startswith("from") and local_prefix in line:
                            line = line.replace(local_prefix, f".{local_prefix}")
                        reference_lines[n] = line
                    reference = "\n".join(reference_lines)
                    if unit in prefix and number in prefix:
                        file_name = f"{prefix}reference.py"
                    elif number in prefix:
                        file_name = f"{unit}_{prefix}reference.py"
                    else:
                        file_name = f"{unit}_{number}_{prefix}reference.py"

                    fo.writestr(str(Path("tests") / file_name), reference)
                    continue

                if path.name.endswith("solution.xlsx"):
                    prefix = path.name.removesuffix("solution.xlsx")
                    if unit in prefix and number in prefix:
                        file_name = f"{prefix}reference.xlsx"
                    elif number in prefix:
                        file_name = f"{unit}_{prefix}reference.xlsx"
                    else:
                        file_name = f"{unit}_{number}_{prefix}reference.xlsx"

                    fo.writestr(str(Path("tests") / file_name), path.read_bytes())
                    continue

                if path.name.endswith("test_cases.py"):
                    # Skip test cases
                    continue

                if path.name.endswith(".png") or path.name.endswith(".jpg"):
                    if path.name.startswith("grader_"):
                        # Add the grader image to the zip file.
                        new_name = path.name.replace("grader_", "")
                        fo.writestr(str(Path("tests") / new_name), path.read_bytes())
                    continue

                if path.name.endswith(".xlsx") or path.name.endswith(".xlsm"):
                    fo.writestr(str(Path("tests") / path.name), path.read_bytes())
                    continue

                rendered = j2_env.get_template(str(path)).render(**parameters)
                fo.writestr((str(Path("tests") / path.name)), rendered)

    # Unzip the archive
    with ZipFile(zip_file_path, "r") as fo:
        fo.extractall(unzip_dir)
        (unzip_dir / "deploy_key").unlink(missing_ok=True)

    # Copy the reference solution as the submitted solution.
    for path in exercise_dir.iterdir():
        if path.is_file():
            # Handle partial solutions
            if path.name.endswith("solution.py") or path.name.endswith("solutions.py"):
                # Render the reference solution.
                reference = j2_env.get_template(str(path)).render(**parameters)

                # Seeded local runtime files should use a reference suffix.
                id = "reference"
                if path.name.endswith("solution.py"):
                    prefix = path.name.removesuffix("solution.py")
                    if unit in prefix and number in prefix:
                        file_name = f"{prefix}{id}.py"
                    elif number in prefix:
                        file_name = f"{unit}_{prefix}{id}.py"
                    else:
                        file_name = f"{unit}_{number}_{prefix}{id}.py"
                else:
                    prefix = path.name.removesuffix("solutions.py")
                    file_name = f"{prefix}{id}.py"

                # Change imports in reference to match student-like file names
                reference_lines = reference.splitlines()
                for n, line in enumerate(reference_lines):
                    if "import" in line:
                        line = (
                            line.replace("solutions", id)
                            .replace("solution", id)
                            .replace("ref_", "")
                        )
                    else:
                        line = line.replace("ref_", "")
                    reference_lines[n] = line
                reference = "\n".join(reference_lines)

                # Write the reference solution under tests/ with test_config.
                with open(unzip_dir / "tests" / file_name, "w") as f:
                    f.write(reference)
            elif path.name.endswith("solution.xlsx"):
                id = "reference"
                prefix = path.name.removesuffix("solution.xlsx")
                if unit in prefix and number in prefix:
                    file_name = f"{prefix}{id}.xlsx"
                elif number in prefix:
                    file_name = f"{unit}_{prefix}{id}.xlsx"
                else:
                    file_name = f"{unit}_{number}_{prefix}{id}.xlsx"

                with open(unzip_dir / "tests" / file_name, "wb") as f:
                    f.write(path.read_bytes())
            elif path.name.endswith("test_cases.py") or path.name.endswith(
                "test_config.py"
            ):
                # Skip configuration.
                continue
            elif path.suffix == ".py":
                # Copy other .py files
                rendered = j2_env.get_template(str(path)).render(**parameters)
                with open(unzip_dir / path.name, "w") as f:
                    f.write(rendered)

    # Add an __init__.py file to the unzipped directory.
    (unzip_dir / "tests" / "__init__.py").touch()
