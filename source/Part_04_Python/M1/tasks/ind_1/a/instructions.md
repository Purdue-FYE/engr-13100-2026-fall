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
    a: "5" # any integer
    b: "a^{1/3}" # a small integer
    c: "\\sin(\\sqrt{b})"
    d: "\\lfloor -90.5 \\rfloor"
    e: "254 \\bmod 66"

    ## Fall 2025
    a: "4" # any  small integer
    b: "3^{1/a}"
    c: "\\log_2(b)"
    d: "\\lceil -3.25 \\rceil"
    e: "315 \\bmod 27"

    ## Spring 2026
    a: "8" # any  small integer
    b: "3^{a/3}"
    c: "\\cos{\\sqrt{b}}"
    d: "\\lfloor 13 * c \\rfloor"
    e: "613 \\bmod d"
---
```{include} /macros.md
```

(mod:py1_ind_task_1)=
# Individual Task 1


## Learning Objectives

Create and execute simple scripts comprised of basic {program}`Python` concepts; Apply
course code standard in development of {program}`Python` scripts; Modularize and comment
code in {program}`Python` for readability and reusability.


## Task Instructions

In this task, you will be doing calculations using both {program}`Python` and
{program}`MS Excel`. By performing the calculations with both tools, you will gain
insight into the differences in syntax between the two


(mod:py1_ind_task_1_part_a)=
### Part A

1. Open the {program}`MS Word` template: {download}`py1_ind_1_username.docx`

2. Open a new {program}`MS Excel` sheet.

3. Assuming problems 1--5 shown in {numref}`tab:py1:eqns1` are computed sequentially in
   the order shown,

   1. Calculate the result of each expression using {program}`MS Excel`.

   2. Calculate the result of each expression using {program}`Python`'s interactive
      mode.  Use the same variable names as in the equations.

   3. Fill in the table in your {program}`MS Word` document, using 4 decimal places when
      necessary. Be sure to include the result AND the syntax used for the calculation.

      ```{admonition} Note
      :class: note

      You should get the same results in both {program}`MS Excel` and {program}`Python`.
      ```

   ```{list-table} Equations in MS Excel and Python
   :name: tab:py1:eqns1
   :class: col-1-center
   :header-rows: 1

   * - Problem Number
     - Equation
     - {program}`MS Excel` Calculations
     - {program}`Python` Calculations

   * - {math}`1`
     - {{ "$a = {}$".format(a) }}
     - Cell A1: {{ a }}
     - a = {{ a }}

   * - {math}`2`
     - {{ "$b = {}$".format(b) }}
     -
     -

   * - {math}`3`
     - {{ "$c = {}$".format(c) }}
     -
     -

   * - {math}`4`
     - {{ "$d = {}$".format(d) }}
     -
     -

   * - {math}`5`
     - {{ "$e = {}$".format(e) }}
     -
     -
   ```

   ```{admonition} Hint
   :class: hint

   The brackets {math}`\lfloor \,  \rfloor` denote the floor operation, while
   {math}`\lceil \, \rceil` denote the ceiling operation . See [floor and ceiling
   functions](https://en.wikipedia.org/wiki/Floor_and_ceiling_functions#:~:text=In%20mathematics%2C%20the%20floor%20function,%E2%8C%89%20or%20ceil(x).)
   for more information.
   ```

4. Repeat Step 3 for problems 6--10 in {numref}`tab:py1:eqns2`, using the values of $a$,
   $b$, $c$, $d$, and $e$ computed above as a data set.  It helps to put the results
   from problems 1--5 in the same row/column in {program}`MS Excel`, and put them in a
   list in {program}`Python` e.g {python}`values = [a, b, c, d, e]`.

   ```{list-table} Statistical Calculations in MS Excel and Python.
   :name: tab:py1:eqns2
   :header-rows: 1

   * - Problem Number
     - Calculation
     - {program}`MS Excel` Calculations
     - {program}`Python` Calculations

   * - 6
     - Find the mean
     -
     -

   * - 7
     - Find the median
     -
     -

   * - 8
     - Find the maximum
     -
     -

   * - 9
     - Find the range
     -
     -

   * - 10
     - Find the standard deviation
     -
     -
   ```

   ```{admonition} Hint
   :class: hint

   {program}`Python`'s [`math`](https://docs.python.org/3/library/math.html) and/or
   [`statistics`](https://docs.python.org/3/library/statistics.html) modules may be
   helpful.
   ```


### Part B

Complete the following steps in your previously created {program}`MS Word` document:

1. For each problem, describe any differences you noticed between the {program}`MS
   Excel` calculations and the {program}`Python` calculations in the "Differences"
   column.

2. Did you use any imported libraries in {program}`Python`, or did you find everything
   you needed in the standard library?  If you used any imported libraries, list which
   one(s).

3. What syntax differences exist between {program}`Python` and {program}`MS Excel`? Be
   specific.

Save the {program}`MS Word` document as a PDF with the name
{glue:text}`../../../3_ind_assignments.md::deliverable_py1_ind_1_pdf:`.

```{list-table} Deliverables
:class: deliverables
:name: tab:Py:M1:individual_1_deliverables
:header-rows: 1

* - Deliverables
  - Description

* - {glue:text}`../../../3_ind_assignments.md::deliverable_py1_ind_1_pdf:`
  - A PDF of your completed {program}`MS Word` document with all calculations and
    answers to the questions.
```