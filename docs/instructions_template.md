# `instructions.md` Template

This is the canonical starting point for a new assignment's `instructions.md`.  Copy this
file into the assignment directory, rename it `instructions.md`, and fill in every
`PLACEHOLDER` token.  Delete comment lines (starting with `<!--`) before committing.

**Label conventions by assignment type:**

| assignment type | Label format example |
|---|---|
| Team project assignment | `(tp:m3:team:assignment_1)=` |
| Python module assignment | `(mod:py5_assignment)=` |
| Python module pre-class | `(mod:py5_pre_1)=` |

See sibling assignments in the same module for the exact prefix used in that module.

**Deliverable naming conventions:**

Deliverables are defined in the YAML frontmatter of an `instructions.md` file
under a `deliverables:` key.  `manage_deliverables.py` reads this list to
generate student-facing filenames and the glue keys used to display them.

Each list entry is a **token** of the form `label_ext` (split on the *last*
underscore).  `ext` becomes the file extension; `label` is prepended to the
assignment ID in the filename.  Omitting `deliverables:` entirely falls back to
the default set: `pdf`, `py`, `xlsx`, `zip`.

Anytime a deliverable is referenced in the body of `instructions.md`, the author
should use the `label_ext` token. This token will be replaced by its corresponding
glue key when the course website is published.

```yaml
# Single deliverable — no label, just an extension
deliverables:
  - py                 # → {assignment_id}_username.py

# Two deliverables of different types — labels are optional when extensions differ
deliverables:
  - report_pdf         # → {assignment_id}_report_username.pdf
  - py                 # → {assignment_id}_username.py

# Two PDFs — a unique label is required for each so their tokens differ
deliverables:
  - report_pdf         # → {assignment_id}_report_username.pdf
  - appendix_pdf       # → {assignment_id}_appendix_username.pdf
  - py                 # → {assignment_id}_username.py
```

To reference a deliverable in the body, use the **placeholder** pattern
`deliverable_TOKEN` (e.g. `deliverable_report_pdf`).  The
`audit_and_fix_references` pass in `manage_deliverables.py` (run via
`make deliverables`) will expand it to the correct `{glue:text}` directive with
the proper path and glue key automatically.
---

<!-- ================================================================
     BEGIN TEMPLATE — delete everything above this line when using
     ================================================================ -->
---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
<!-- Replace LABEL_EXT with the deliverable name (if needed) and extension
for this assignment (see conventions above) -->
deliverables:
  - LABEL_EXT
---
```{include} /macros.md
```

<!-- Replace ASSIGNMENT_LABEL with the label for this assignment (see conventions above) -->
(ASSIGNMENT_LABEL)=
# assignment N <!-- Replace N with the assignment number -->


## In this assignment you will:
<!-- List concrete, student-facing learning outcomes for this assignment. -->
- PLACEHOLDER

## Learning Objectives

<!-- List course learning objectives connected to this assignment. -->
- PLACEHOLDER
- PLACEHOLDER

## Q1: DESCRIPTIVE QUESTION TITLE

### Background

<!-- Conceptual and motivational content: why this technique is used, how it compares
     to alternatives, background theory, and illustrative figures.  This section
     should give students enough context to understand *what* they are building and
     *why*, before they see any implementation instructions. -->

PLACEHOLDER


### Deliverables


<!-- Replace the glue paths with the correct deliverable keys for this assignment. -->
Download the {program}`Python` template {download}`ENGR131_Python_Template.py </Part_04_Python/ENGR131_Python_Template.py>` and save it as LABEL_EXT. Use the sample output section below to verify that your program outputs correct values.

```{admonition} Deliverable Reminder
:class: note

Remember to include comments in your python script to practice professional programming standards.
```

### Program Requirements
<!-- Brief framing sentence for the assignment Instructions section if needed, e.g.:
     "In this assignment, you will build a ..."  Keep this short; details belong in Steps. -->

PLACEHOLDER


<!-- ----------------------------------------------------------------
     One block like the one below per function students must write.
     Number steps from 1 upward.  The last step is always main().
     ---------------------------------------------------------------- -->

<!-- Replace assignment_LABEL_step_1 with e.g. tp:m3:team:assignment_1_step_1 -->
(assignment_LABEL_step_1)=
## Step 1: Function Name

<!-- One sentence identifying the function. -->
Create a function named {python}`function_name`.

Arguments:

<!-- List every argument: {python}`name` (type): Capitalized description ending in a
     period.  For NumPy arrays, always state dtype and shape, e.g.:
         1D NumPy array of floats, shape `(m,)`
         2D NumPy array of floats, shape `(m, n)` -->
- {python}`arg1` (type): PLACEHOLDER.
- {python}`arg2` (type, default VALUE): PLACEHOLDER.

Returns:

- {python}`result` (type): PLACEHOLDER.

<!-- Numbered implementation steps.  Keep these focused on *what* to do, not *how*;
     use Hint admonitions for algorithmic details. -->
1. PLACEHOLDER.
2. PLACEHOLDER.

<!-- Optional: Hint admonition for non-obvious implementation details. -->
```{admonition} Hint
:class: tip

PLACEHOLDER
```

<!-- Optional: Note admonition when students must copy a function from a prior assignment.
     Reference the prior assignment with a {numref} or {ref} directive. -->
```{admonition} Note
:class: note

You will need the {python}`helper_function` function developed in
{numref}`PRIOR_assignment_LABEL`.  Copy it into your program.
```


(assignment_LABEL_step_N)=
## Step N: Main Function

<!-- The main function description.  No Arguments: / Returns: block needed unless the
     grader checks specific return values. -->
Create a {python}`main` function that PLACEHOLDER.

1. PLACEHOLDER.
2. PLACEHOLDER.

```{admonition} Note
:class: note

<!-- List any helper functions students must copy from prior assignments. -->
You will need the following functions developed in {numref}`PRIOR_assignment_LABEL`.
Copy them into your program.

- {python}`function_a`: PLACEHOLDER.
- {python}`function_b`: PLACEHOLDER.
```
