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

(PY:M3:PCA1b)=
# PCA: Nested Loops

## Learning Objectives

- PR01: Programming Standards
- PR02: Data Storage
- PR03: Calculations
- PR04: Modular Programming
- PR05: Code Structures
- PR06: Translate Program Descriptions
- PR07: Test cases & Tracking
- PR08: Debugging

## Activity Instructions & Submission

Navigate to [INSERT ASSIGNMENT NAME] on Gradescope and complete the following:

### Part A

The `while` loop below contains an `if` statement. Review the code and determine the following:

1. What will be displayed in the terminal when the program is run?

2. How many times will the `while` loop iterate?

```python
x = 1
i = 1

print(f"Starting while loop iteration: i = {i}, x = {x}")
while i < 10:
    if x < 3:
        x += 1
        print(f"Incremented x; Current x = {x}")
    i += 2
print(f"Final value of i: {i}")
```

### Part B

Create a flowchart for the `while` loop in Part A. Reference the "Loop Basics" video [INSERT LINK HERE] for how to create flowcharts with loops. When you are finished, upload your flowchart as a .pdf file.

We recommend using https://app.diagrams.net/ to design and export your flowchart as a .pdf file. Reference the Flowcharts [INSERT LINK TO PRE-CLASS MATERIALS HERE] section of the Python 2 pre-class materials for which shapes to use.

### Part C

1. How would you change the `while` loop to run infinitely? Include two ways you could do this in your answer.
