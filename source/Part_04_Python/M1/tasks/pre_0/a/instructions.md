---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
myst:
  substitutions:
    # Variations: place selected variation last

    ## Fall 2024
    a: 5 # any number
    b: 9 # a small integer
    c: 2 # any number but 0

    func_1_md: '{math}`a \cdot b^2 + \sin(c)`'
    func_1_py: 'a * math.pow(b, 2) + math.sin(c)'

    func_2_md: '{math}`\frac{\pi}{c} - b!`'
    func_2_py: '(math.pi / c) - math.factorial(b)'

    func_3_md: '{math}`b^3 + \frac{c}{4} + \sin^{-1}{(1)}`'
    func_3_py: 'math.pow(b, 3) + (c / 4) + math.asin(1)'

    precision: 4
    precision_str: 'four'

    ## Fall 2025
    a: 20 # any number
    b: 8 # a small integer
    c: 9.81 # any number but 0

    func_1_md: '{math}`a \cos(b!)`'
    func_1_py: 'a * math.cos(math.factorial(b))'

    func_2_md: '{math}`(a^2 - (a \cos(b))^2) / (2 c)`'
    func_2_py: '(math.pow(a,2) - math.pow(a * math.cos(b),2)) / (2 * c)'

    func_3_md: '{math}`\dfrac{a \sin^{-1}{(1/2)}}{c}`'
    func_3_py: 'a * math.asin(0.5) / c'

    precision: 4
    precision_str: 'four'

    ## Spring 2026
    a: 101 # any number
    b: 7 # a small integer
    c: 12.34 # any number but 0

    func_1_md: '{math}`c^2 - \sin(b)^2`'
    func_1_py: 'c**2 - math.sin(b)**2'

    func_2_md: '{math}`b!\cdot (\cos(\dfrac{\pi}{c})- a)`'
    func_2_py: 'math.factorial(b) * (math.cos(math.pi / c) - a)'

    func_3_md: '{math}`\dfrac{c^{\pi e} \sin^{-1}{(\sqrt{3}/2)}}{a^e b}`'
    func_3_py: 'math.pow(c, math.pi * math.e) * math.asin(math.sqrt(3) / 2) / (a**math.e * b)'

    precision: 3
    precision_str: 'three'
---
```{include} /macros.md
```

# Pre-Class Task 0


## Learning Objectives

Perform arithmetic operations (i.e., addition, subtraction, multiplication, division,
and exponentiation), in {program}`Python` while keeping in mind order of operations;
Employ {program}`Visual Studio Code` to write, edit, and save {program}`Python` code;
Output {program}`Python` data from script to screen.


## Introduction

{program}`Python 3` is a powerful programming language for performing computations,
scripting, and database management. As an engineering tool, it offers standard
mathematical operations as part of its basic environment.  Therefore, you can design
standard computational models, process data, and generate reports. The language must
work within the limits of the machine it is running on. As a result, there may be
differences between what you compute by hand and what {program}`Python` computes.

Unless mentioned otherwise, for all {program}`Python` tasks (pre-class, team and
individual) you will be writing your scripts using {download}`ENGR131_Python_Template.py
</Part_04_Python/ENGR131_Python_Template.py>`. This template contains header information
that must always be edited to reflect the task your {program}`Python` file is meant to
solve, and you will always be prompted in the problem statement to rename the file.

The template contains a section for importing modules, and a function called
{python}`main()` where you will be writing your code. While user-defined functions will
be taught in more detail in the next {program}`Python` module, for now you will just
need to remember to write all your code within {python}`main()`. Note that, when writing
code inside a function, it must be indented 1 tab (or 4 spaces) relative to the
indentation level of the function.


## Task Instructions

Before beginning this activity, read through the pre-class material, and completely
watch the pre-class videos. Additionally, do some research into some common
{program}`Python` libraries (i.e. the
[`math`](https://docs.python.org/3/library/math.html) library will be helpful for this
assignment). There are many functions within the `math` library in particular that will
be needed for this task. It is important for your learning and ability to contribute to
future assignments that you understand the covered topics.  In this task, you will be
doing calculations in {program}`Python`.

1. Make a copy of the {download}`ENGR131_Python_Template.py
</Part_04_Python/ENGR131_Python_Template.py>` {program}`Python` template and rename
   the file to .

2. Make sure to fill out all header information, including a short description
   of the code.

3. Include all needed import statements in the labeled section of the template.

   ```{admonition} Hint
   :class: hint

   The {python}`math` module may be useful.
   ```

4. In your main script, initialize three variables `a`, `b`, and `c` ({{
   "${}$".format(a) }}, {{ "${}$".format(b) }}, and {{ "${}$".format(c) }}) that
   can be used in the calculations.

5. Implement the following three equations in {program}`Python` using three more
   variables to store the results.  Use appropriate {python}`math` function calls where
   needed.  Be careful with order of operations.

   1. {{ func_1_md }}
   2. {{ func_2_md }}
   3. {{ func_3_md }}

   ```{admonition} Hint
   :class: hint

   In {program}`Python`, you can compute the inverse of a trigonometric function using
   the {code}`math` module. For example, the inverse sine function, denoted as
   {math}`\sin^{-1}` can be calculated using {code}`math.asin()`.
   ```

6. After each calculation, print the output to the command window rounded to {{
   precision_str }} decimal places.  Research
   [f-strings](https://docs.python.org/3/reference/lexical_analysis.html#formatted-string-literals)
   and the [format specification
   mini-language](https://docs.python.org/3/library/string.html#format-specification-mini-language)
   to learn how to round the output to {{ precision_str }} decimal places without
   changing the stored value.

   ```{admonition} Hint
   :class: hint

   Do not use the {python}`round()` function.
   ```

7. Save the file as
 and turn in
   the assignment on Gradescope.

% Automatically generated Sample Output section.
```{include} /_build/intermediate/Part_04_Python/M1/tasks/pre_0/a/sample_output.md
```