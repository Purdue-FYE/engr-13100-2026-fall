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

(Py:M3:py3_pre_1)=
# PCA #X: Looping Structures

## Learning Objectives

- PR01: Programming Standards
- PR02: Data Storage
- PR03: Calculations
- PR04: Modular Programming
- PR05: Code Structures
- PR06: Translate Program Descriptions
- PR07: Test cases & Tracking
- PR08: Debugging

## Files Needed

Download the {program}`Python` template {download}`ENGR131_Python_Template.py </Part_04_Python/ENGR131_Python_Template.py>` and save it as {glue:text}`../../../../../glue_factory.md::py3_pre_1_py:`.

## Activity Instructions & Submission

Write a Python program that repeatedly asks the user to enter a number. The program should stop only when the user enters 0.

Follow these steps:

1. Prompt the user to enter a number and store it in a variable called `num`.
2. Create a `while` loop that continues running as long as the number is not equal to 0.
3. Inside the `while` loop:
- Print the number the user entered.
- Ask the user to enter another number and store it again in `num`.
- When the user enters 0, the loop should stop and the program should print "Done!".

Test your program using the sample input/output below.

% Automatically generated Sample Output section.
```{include} /_build/intermediate/Part_04_Python/M3/tasks/pre_1/a/sample_output.md
```

## Deliverables

Submit your {program}`Python` file {glue:text}`../../../../../glue_factory.md::py3_pre_1_py:` to (INSERT ASSIGNMENT NAME) on Gradescope.