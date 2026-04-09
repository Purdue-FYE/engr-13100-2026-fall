# Task PR Review Guidelines

These guidelines describe the standard review process for task pull requests.  They
are written for use by AI agents and human reviewers alike.  Apply every check to each
task being modified before marking the PR ready.

See `docs/instructions_template.md` for the canonical skeleton to use when creating a
new `instructions.md` from scratch.

---

## 0. Before Opening the PR (Author Checklist)

Run these checks locally before pushing the branch.  They catch the most common review
findings in under a minute.

**`DUE_DATE` year** — confirm it matches the current semester:

```bash
grep DUE_DATE source/path/to/task/test_config.py
```

**Point weights** — confirm they sum to the expected total:

```bash
python - <<'EOF'
import ast, sys
src = open("source/path/to/task/test_config.py").read()
tree = ast.parse(src)
weights = [
    kw.value.n
    for node in ast.walk(tree)
    if isinstance(node, ast.Call)
    for kw in node.keywords
    if kw.arg == "weight" and isinstance(kw.value, ast.Constant)
]
print(f"weights: {weights}")
print(f"total:   {sum(weights):.4f}")
EOF
```

**Non-ASCII characters** — must return nothing:

```bash
grep -rnP '[^\x00-\x7F]' source/path/to/task/instructions.md source/path/to/task/solution.py
```

**Broken symlinks** — must return nothing:

```bash
find source/path/to/task -type l ! -exec test -e {} \; -print
```

**Line length** — must return nothing (88-char limit):

```bash
awk 'length > 88 {print FILENAME ":" NR ": " length " chars"}' \
    source/path/to/task/instructions.md source/path/to/task/solution.py
```

**Build** — must succeed with no warnings:

```bash
make
```

**Grader smoke test** — must score the expected total (see Section 3.2):

```bash
make graders
cd source/_build/graders/path/to/task/autograder_<hash>
python run_tests.py
# check sibling results/ directory for results.json
```

---

## 1. File Inventory

### 1.1  Remove leftover files

List every file in the task folder and any asset subdirectories.  Search each file's
name across `instructions.md`, `test_config.py`, `test_cases.py`, and `solution.py`.
Flag any file that is not referenced in any of those four files.

Delete flagged files.  If uncertain, check git history to confirm the file belongs to
a previous version of the exercise.

### 1.2  Verify reference asset names are consistent

When a reference file (data file, image, CSV, etc.) is renamed, every location that
uses it must be updated atomically:

| Location | What to check |
|---|---|
| `instructions.md` | `{download}` directives, `{python}` example filenames in step lists |
| `test_config.py` | asset lists in `init()`, module-level variable names, test case tuples |
| `test_cases.py` | `entries` values |
| Any generator script (e.g., `ref_encoder.py`) | output path arguments |
| Asset subdirectories on disk | Actual filenames |
| Task root directory | Actual filenames |

Variable names derived from a filename (e.g., `ref_data_a_result`) must also be
updated when the filename changes.

### 1.3  Verify symlinks

Symlinks to shared assets (data files, CSVs, etc.) must resolve from the local working
tree.  Absolute paths written in CI, Codespaces, or Docker environments will break on
any other machine.

Check for broken symlinks:

```bash
find source/path/to/task -type l ! -exec test -e {} \; -print
```

If any are found, replace with a relative path:

```bash
# Example: re-create a broken symlink as a relative one
ln -sf ../../../../M2/tasks/team_2/a/img_features.csv source/path/to/task/img_features.csv
```

Verify the relative path resolves correctly before committing:

```bash
ls -l source/path/to/task/img_features.csv   # should show the -> target
cat source/path/to/task/img_features.csv      # should print file contents
```

---

## 2. `instructions.md` Review

### 2.1  Headings

Section headings must not end with a colon.

- Wrong: `## Learning Objectives:`
- Correct: `## Learning Objectives`

**Spacing:** Place two blank lines before every heading and one blank line after.
The only exception is a MyST section label: if a heading has a label, place the
label on the line *immediately* above the heading with no blank line between them.
The two blank lines go before the label.

````markdown


(section-label)=
## Section Title

First paragraph of the section...
````

### 2.2  Cross-task references

Never reference other tasks by "Part N" or "Part 1 / Part 2" framing.  When the target
section has a label, use a `{numref}` or `{ref}` directive; this will fail loudly
during the build if the target is ever renamed or deleted, catching broken links early.
When no label exists, use a relative description.

- Wrong: `"In Part 1, you implemented..."`
- Better (plain text): `"In the previous task, you implemented..."`
- Best (labeled reference): `` "In {numref}`mod:py5_team_2`, you implemented..." ``

### 2.3  Structure — Introduction vs. Task Instructions

**Introduction** should contain all conceptual and motivational content: why the
technique is used, how it compares to alternatives, background theory, and illustrative
figures.

**Task Instructions** should be purely implementation-focused: what functions to write,
what inputs they take, and what they return.  Remove explanatory bullets from Task
Instructions if the same information is already in the Introduction.

### 2.4  Deliverable Reminder admonition

Replace any inline boilerplate about flowcharts, templates, and filenames with a
`tip`-class admonition at the top of the Task Instructions section:

````markdown
```{admonition} Deliverable Reminder
:class: tip

Create a flowchart of your algorithm and save it as
{glue:text}`path::deliverable_key_pdf:`.  Start your program from a copy of the
{download}`ENGR133_Python_Template.py<...>` template and name it
{glue:text}`path::deliverable_key_py:`.
```
````

### 2.5  Math blocks

Convert all `$$...$$` blocks to labeled `{math}` directives:

````markdown
```{math}
:label: eq:tp:m1:<task_identifier>:<concept_shortname>

<equation>
```
````

Label format: `eq:tp:m1:<task_identifier>:<concept_shortname>` (all lowercase,
underscores).  Reference equations with `{eq}` where needed.

### 2.6  Inline math

Use the `{math}` role for all inline mathematical expressions.  Do not use bare
dollar signs (`$...$`) for inline math.

- Wrong: `The value $x$ represents...`
- Correct: `` The value {math}`x` represents... ``

### 2.7  Program references

Replace `**Python**` with the `{program}` macro:

- Wrong: `**Python**`
- Correct: `` {program}`Python` ``

### 2.8  Return type specifications

Every function description must explicitly state:
- The return type (e.g., `float`, `int`, `str`, `2D NumPy array of floats`)
- Array dtype and dimensions when returning a NumPy array

### 2.9  Helper function notes

When students must reuse a function from a previous task, add a `note`-class admonition
in the relevant function section:

````markdown
```{admonition} Note
:class: note

You will need the {python}`function_name` function developed in
{numref}`mod:<previous_task_label>`.  Copy it into your program.
```
````

### 2.10  Typography

- **No non-ASCII characters.**  Every character in `instructions.md` must be
  plain ASCII (code points 0–127).  Common offenders:
  - Em dash (—, U+2014): use a comma, semicolon, or rewrite the sentence.
  - En dash (–, U+2013): use "to" for ranges (e.g., "0 to 255").
  - Curly quotes (‘’“”): use straight ASCII quotes `'` and `"`.
  - Ellipsis (…, U+2026): use three plain periods `...`.
  - Any other Unicode punctuation or letter: replace with ASCII equivalent or
    rewrite.
- Use two spaces after a sentence-ending period in running prose (matches existing
  codebase style).
- Lines should not exceed 88 characters in length.  If a sentence exceeds this limit,
  break it into multiple lines at logical points (e.g., after a comma or conjunction).

### 2.11  Inter-task style consistency

When a PR adds or significantly rewrites a task, compare `instructions.md` against
sibling tasks in the same module (i.e., tasks in the same `M<N>/tasks/` directory).
Verify that the following are consistent:

| Element | Expected style |
|---|---|
| Top-level task label and heading | `(label)=` immediately above `# Task N` (no blank line between) |
| Step headings | `## Step N: Function Name` at the `##` level |
| Step labels | `(label_step_N)=` immediately above each step heading |
| Function intro line | `Create a function named {python}\`funcname\`.` |
| Argument block header | `Arguments:` (plain text, no bold, followed by blank line) |
| Return block header | `Returns:` (plain text, no bold, followed by blank line) |
| Argument/return descriptions | `{python}\`name\` (type): Capitalized description ending in a period.` |
| Implementation hints | `{admonition} Hint :class: tip` block, not bold inline text |
| Helper function notes | `{admonition} Note :class: note` block (see Section 2.9) |
| Math role | `{math}\`` for inline math, never bare `$...$` |
| Python role | `{python}\`` for parameter names and inline code |

**For new tasks:** start from `docs/instructions_template.md` rather than copying from
a sibling task that may itself have diverged from the current style.

---

## 3. `test_config.py` Review

### 3.1  DUE_DATE

Verify the year in `DUE_DATE` matches the current semester.

### 3.2  Point weights

The required point total varies by task type:

| Task type | Total points |
|---|---|
| Pre-tasks | 2.0 |
| Team task 1 | 1.0 |
| Team task 2 | 2.0 |
| Team task 3 | 2.0 |
| Individual tasks | 5.0 |

Team project team tasks have different point totals (currently either 6.0 or 8.0)

All weights must sum to the correct total and be expressed as clean decimals with no
repeating digits.  Prefer explicit literals (e.g., `0.5`) over `constant / len(cases)`
expressions.  A division expression is acceptable only when it is guaranteed to produce
a clean decimal for the actual case count being used (e.g., `3.0 / 10` = `0.3`).

Use the weight-sum one-liner from Section 0 to verify the total before and after any
edits to `test_config.py`.

Standard allocation for an **8.0-point** team task (adjust counts as needed):

| Category | Allocation |
|---|---|
| Style tests (docstring, comments, length) | 3 × 0.05 = 0.15 (internally expands to 0.40) |
| Main function output tests | 2 × 1.2 = 2.40 |
| Other function return-value tests | distribute remaining 5.20 cleanly |

Example clean distributions of 5.20 across function test groups:
- Three groups: 4 × 0.4 + 2 × 0.7 + 1 × 1.0 = 1.6 + 1.4 + 1.0 + 1.2 (remaining)
- Pattern used in TP:M3: scale all per-case weights by 4/3 relative to the prior 6-pt version

### 3.3  Variable names derived from asset names

When a reference asset is renamed, update any module-level variable built from that
name and all places that variable is used in test case lists:

```python
# Wrong after renaming ref_data.csv -> ref_data_a.csv:
ref_result = compute(load("tests/ref_data_a.csv"))

# Correct:
ref_data_a_result = compute(load("tests/ref_data_a.csv"))
```

---

## 4. `solution.py` Review

### 4.1  Comments

The solution must have comments appropriate for learners at the course level.  Comments
should explain the *why*, not just restate what the code does.  Required locations:

- Every conditional branch that handles a non-obvious edge case
- Every formula or algorithm step that is not self-evident from the variable names
- Any specific constant, coefficient, or threshold whose origin may not be obvious

### 4.2  Helper functions from prior tasks

When a function is copied from a prior task, annotate it:

```python
# Copied from <prior_task_label>
def helper_function(...):
    ...
```

### 4.3  Return type consistency

Verify that the return type of every function in `solution.py` matches the
specification in `instructions.md`.  Common mismatches to check:
- Numeric type (float vs. int)
- NumPy array dtype (e.g., `np.uint8` vs. `float64`)
- Whether type conversion happens in an intermediate function or only in the final step

### 4.4  Typography

No non-ASCII characters anywhere in comments or string literals.  Use plain ASCII
punctuation.  See Section 2.10 for the full list of common offenders.

---

## 5. Cross-file Consistency Check

After addressing all individual file issues, confirm:

- [ ] Function names match between `solution.py` and `instructions.md`
- [ ] Parameter names match between `solution.py` and `instructions.md`
- [ ] Any example values used in `main()` (constants, filenames, etc.) match those
      stated in the instructions
- [ ] All reference asset filenames are consistent across all files (see Section 1.2)
- [ ] Point weights in `test_config.py` sum to the correct total for this task type (see Section 3.2) with clean decimals
- [ ] `DUE_DATE` year is correct

---

## 6. Grader Smoke Test

After all edits:

1. Run `make graders` from the repo root.
2. Locate the built autograder directory.  The path pattern is:
   ```
   source/_build/graders/<task-path>/autograder_<hash>/
   ```
   where `<task-path>` mirrors the task's location under `source/` (e.g.,
   `Part_4_Team_Project/M3/tasks/team_3/a`).  Use `ls` or tab-completion to
   find the `autograder_<hash>` directory name.
3. `cd` into the autograder directory and run:
   ```bash
   python run_tests.py
   ```
4. Results are written to the `results/` directory **sibling** to the autograder
   directory (not inside it):
   ```
   source/_build/graders/<task-path>/results/results.json
   ```
5. Confirm the `score` in `results.json` equals the expected total for this task
   type (see Section 3.2) and all tests show `"passed": true`.

If any test fails, resolve the discrepancy between `solution.py` and `test_config.py`
before proceeding.
