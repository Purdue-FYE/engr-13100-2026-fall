# `instructions.md` Template

This is the canonical starting point for a new task's `instructions.md`.  Copy this
file into the task directory, rename it `instructions.md`, and fill in every
`PLACEHOLDER` token.  Delete comment lines (starting with `<!--`) before committing.

**Label conventions by task type:**

| Task type | Label format example |
|---|---|
| Team project task | `(tp:m3:team:task_1)=` |
| Python module pre-class| `(mod:py5_team_3)=` |
| Python module assignment | `(mod:py5_ind_1)=` |
| Python module pre-task | `(mod:py5_pre_0)=` |

See sibling tasks in the same module for the exact prefix used in that module.

**Deliverable naming conventions:**

Deliverables are defined in the frontmatter of an `instructions.md` file. You
may define as many deliverables as you like. If multiple deliverables have the
same file extension (e.g. pdf), each one will need a unique name. 
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
---
```{include} /macros.md
```

<!-- Replace TASK_LABEL with the label for this task (see conventions above) -->
(TASK_LABEL)=
# Task N <!-- Replace N with the task number -->


## Learning Objectives

<!-- List 3-5 concrete, student-facing learning outcomes for this task. -->
- PLACEHOLDER
- PLACEHOLDER


## Introduction

<!-- Conceptual and motivational content: why this technique is used, how it compares
     to alternatives, background theory, and illustrative figures.  This section
     should give students enough context to understand *what* they are building and
     *why*, before they see any implementation instructions. -->

PLACEHOLDER


## Task Instructions

```{admonition} Deliverable Reminder
:class: tip

<!-- Replace the glue paths with the correct deliverable keys for this task. -->
Create a flowchart of your algorithm and save it as
{glue:text}`../../../1_team_assignments.md::DELIVERABLE_KEY_PDF:`.
Start your program from a copy of the
{download}`ENGR133_Python_Template.py<../../../../ENGR133_Python_Template.py>`
template and name it
{glue:text}`../../../1_team_assignments.md::DELIVERABLE_KEY_PY:`.
```

<!-- Brief framing sentence for the Task Instructions section if needed, e.g.:
     "In this task, you will build a ..."  Keep this short; details belong in Steps. -->

PLACEHOLDER


<!-- ----------------------------------------------------------------
     One block like the one below per function students must write.
     Number steps from 1 upward.  The last step is always main().
     ---------------------------------------------------------------- -->

<!-- Replace TASK_LABEL_step_1 with e.g. tp:m3:team:task_1_step_1 -->
(TASK_LABEL_step_1)=
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

<!-- Optional: Note admonition when students must copy a function from a prior task.
     Reference the prior task with a {numref} or {ref} directive. -->
```{admonition} Note
:class: note

You will need the {python}`helper_function` function developed in
{numref}`PRIOR_TASK_LABEL`.  Copy it into your program.
```


(TASK_LABEL_step_N)=
## Step N: Main Function

<!-- The main function description.  No Arguments: / Returns: block needed unless the
     grader checks specific return values. -->
Create a {python}`main` function that PLACEHOLDER.

1. PLACEHOLDER.
2. PLACEHOLDER.

```{admonition} Note
:class: note

<!-- List any helper functions students must copy from prior tasks. -->
You will need the following functions developed in {numref}`PRIOR_TASK_LABEL`.
Copy them into your program.

- {python}`function_a`: PLACEHOLDER.
- {python}`function_b`: PLACEHOLDER.
```
