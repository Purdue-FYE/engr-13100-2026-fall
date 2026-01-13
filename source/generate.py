import atexit
import importlib
import os
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path
from shutil import copytree, ignore_patterns, move

import yaml
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from utils.formatters import (
    format_figure,
    format_io_log,
    format_output_file,
    format_test_case_table,
)
from utils.runner import Runner


@contextmanager
def path_tmp_dir_context(new_dir):
    """Temporarily change working directory to the new_dir and add it to the path."""
    original_path = sys.path.copy()
    sys.path.insert(0, str(new_dir))
    cwd = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(cwd)
        sys.path = original_path


def mk_tmp_dir(prefix):
    """Create a temporary directory for rendered files."""
    tmp_dir = tempfile.TemporaryDirectory(
        prefix=prefix, dir="source/_build/intermediate"
    )

    # Add a callback to clean up temporary directory when program exits.
    atexit.register(tmp_dir.cleanup)

    # Make returned path relative to source directory.
    return Path(*Path(tmp_dir.name).parts[-4:])


def get_all_files(directory):
    """Get all files in a directory."""
    return set(f for f in Path(directory).glob("**/*") if f.is_file())


def run_solution(
    tmp_dir, callable="main", entries=None, args=(), suppress_output=False
):
    files_before = get_all_files(tmp_dir)
    runner = Runner(str(tmp_dir / "solution"), callable)
    runner.call_obj(entries, args, suppress_output=suppress_output)
    return runner.read_log(), sorted(get_all_files(tmp_dir) - files_before)


def add_files(f, new_files, name, version_path, tmp_dir):
    # Copy the newly generated files to the intermediate directory
    intermediate_dir = Path("source/_build/intermediate")
    for file in new_files:
        if file.suffix in [".pyc"]:
            continue
        dst = (
            intermediate_dir / version_path / f"Case_{name}_{file.relative_to(tmp_dir)}"
        )
        os.makedirs(dst.parent, exist_ok=True)
        move(src=file, dst=dst)

        # Trim off source directory.
        path = dst.relative_to("source")
        if file.suffix in [".png", ".jpg", ".jpeg", ".gif", ".svg"]:
            # Handle images.
            f.write(format_figure(path))
        elif file.suffix in [".txt"]:
            # Handle text files.
            f.write(format_output_file(path))


def main():
    # Get the target from the first command line argument.
    target = Path(sys.argv[1])

    # Extract the part, module number, task, and version name from the target.
    # e.g.
    # source/_build/intermediate/Part_3_Python/M1/tasks/ind_2/version/a_sample_output.md
    # yields Part_3_Python, M1, ind_2, version, a_
    part, module, _, task, version = target.parts[-6:-1]
    task_part = target.stem.removesuffix("sample_output")

    version_path = Path(part, module, "tasks", task, version)

    # Load the task parameters from the instruction's YAML configuration.
    with open("source" / version_path / "instructions.md") as f:
        try:
            parameters = yaml.safe_load(f.read().split("---")[1])["myst"][
                "substitutions"
            ]
        except KeyError:
            parameters = {}

    # Determine if solution is a Python or MATLAB file based on the suffix.
    # Generate a list of all solution files in this directory.
    files = list(("source" / version_path).glob(f"{task_part}solution.*"))
    assert len(files) == 1, (
        f"Expected exactly one file matching {module}. Found: {files}"
    )
    main_solution_file = files[0]
    suffix = main_solution_file.suffix

    # Create a Jinja2 environment with custom delimiters.
    j2_env = Environment(
        loader=FileSystemLoader("."),
        variable_start_string='{{"',
        variable_end_string='"}}',
    )

    # Render the solution to a temporary directory.
    Path(target.parent).mkdir(parents=True, exist_ok=True)
    tmp_dir = mk_tmp_dir("ENGR133")
    solution = (tmp_dir / "solution").with_suffix(suffix)
    solution_template = j2_env.get_template(str(main_solution_file))
    with open(solution, "w") as f:
        f.write(solution_template.render(**parameters))

    # Copy non-templated dependencies to the temporary directory.
    copytree(
        src="source" / version_path,
        dst=tmp_dir,
        ignore=ignore_patterns("*solution.py", "*test_cases.py", "__pycache__/*"),
        dirs_exist_ok=True,
    )

    # Determine the appropriate title for the solution.
    title = f"{module}_{task}_{task_part}"
    if "Excel" in part:
        title = title.replace("M", "ex", 1)
    elif "Python" in part:
        title = title.replace("M", "py", 1)
    elif "Team_Project" in part:
        title = title.replace("M", "tp", 1)
    elif "MATLAB" in part:
        title = title.replace("M", "ma", 1)

    # Import the test cases dynamically.
    try:
        # Render the test cases to a temporary directory.
        test_cases = f"{tmp_dir}/test_cases"
        test_cases_template = j2_env.get_template(
            str("source" / version_path / f"{task_part}test_cases.py")
        )
        with open(test_cases + ".py", "w") as f:
            f.write(test_cases_template.render(**parameters))

        # Import the test cases module and extract the cases, labels and note.

        with path_tmp_dir_context(tmp_dir):
            test_cases_module = importlib.import_module(
                test_cases.removeprefix("source/").replace("/", ".")
            )
        title = getattr(test_cases_module, "title", title)
        note = getattr(test_cases_module, "note", "")
        depth = getattr(test_cases_module, "depth", 3)
        labels = test_cases_module.labels
        cases = test_cases_module.cases
    except TemplateNotFound:
        title = title
        note = None
        depth = 3
        labels = []
        cases = {}

    # Write the sample output file.
    table_name = f"{part}:{module}:{task}:{version}:{task_part}"
    with open(target, "w") as f:
        f.write("% Do not edit this file. It is generated by generate.py.\n")
        f.write(f"(mod:{part}_{module}_{task}_{version}_{task_part}sample_output)=\n")
        f.write(f"{'#' * depth} Sample Output\n\n")

        if note:
            f.write(f" {note} " if note else "")

        if cases:
            f.write(format_test_case_table(cases, labels, table_name + "test_cases"))

            for case_name, case in cases.items():
                log, new_files = run_solution(
                    tmp_dir,
                    case["callable"],
                    case.get("entries"),
                    case.get("args", ()),
                    case.get("suppress_output", False),
                )
                if log:
                    f.write(
                        format_io_log(
                            log,
                            case_name,
                            title=title,
                            args=case.get("args"),
                            suppress_output=case.get("suppress_output", False),
                        )
                    )
                if new_files:
                    add_files(f, new_files, case_name, version_path, tmp_dir)

        else:
            log, new_files = run_solution(tmp_dir)
            if log:
                f.write(format_io_log(log, title=title))
            if new_files:
                add_files(f, new_files, "", version_path, tmp_dir)


if __name__ == "__main__":
    main()
