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

(Py:M1:py1_pre_0)=
# PCA #X: Python Foundations

## Learning Objectives

- PR01: Programming Standards
- PR02: Data Storage
- PR03: Calculations
- PR08: Debugging

## Introduction

{program}`Python 3` is a powerful programming language for performing computations,
scripting, and database management. As an engineering tool, it offers standard
mathematical operations as part of its basic environment.  Therefore, you can design
standard computational models, process data, and generate reports. The language must
work within the limits of the machine it is running on. As a result, there may be
differences between what you compute by hand and what {program}`Python` computes.

## Files Needed

Unless mentioned otherwise, for all {program}`Python` assignments (pre-class, team and individual) you will be writing your scripts using {download}`ENGR131_Python_Template.py
</Part_04_Python/ENGR131_Python_Template.py>`. 
This template contains header information that must always be edited to reflect the task your {program}`Python` file is meant to solve, and you will always be prompted in the problem statement to rename the file.

The template contains a section for importing modules, and a function called
{python}`main()` where you will be writing your code. While user-defined functions will be taught in more detail in the next {program}`Python` module, for now you will just need to remember to write all your code within {python}`main()`. Note that, when writing code inside a function, it must be indented 1 tab (or 4 spaces) relative to the indentation level of the function.

For this assignment, download the {program}`Python` template {download}`ENGR131_Python_Template.py
</Part_04_Python/ENGR131_Python_Template.py>` and save as "py1_pre_1_username.py."

## Activity Instructions & Submission

Write, run, and test python code for the following questions. Remember to include comments throughout your code to practice professional coding etiquette.

### Q1 Mathematical Report Generator

#### Program Requirements:

1.	Ask the user to input a value between 1 and 10 and assign the input value to variable `a`.
2.	Ask the user to input a value between 3 and 8 and assign the input value to variable `b`.
3.	Convert both input values to float.
4.	Calculate and store the following separate variables:
- Sum
- Difference
- Product
- Quotient
- Power – first number (a) raised to the second (b)
5.	Calculate the square root of the absolute value of each number
6.	Display a clearly labeled, multi-line output
7.	Format all numerical values to two decimal places.

% Automatically generated Sample Output section.
```{include} /_build/intermediate/Part_04_Python/M1/tasks/pre_0/b/sample_output.md
```

### Deliverables

Submit your python file (py1_pre_X_username.py) to (INSERT ASSIGNMENT NAME) on GradeScope.