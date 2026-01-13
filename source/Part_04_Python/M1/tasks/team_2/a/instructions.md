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
    seed: 5
    seed2: 42
    precision: 3
    precision_str: "{math}`3`"
    max_denominator: 1000  # max denominator must be 10**precision
    max_denominator_str: "{math}`1000`"
---
```{include} /macros.md
```

# Team Task 2


## Learning Objectives

Perform arithmetic operations in {program}`Python` (i.e., addition, subtraction,
multiplication, division, and exponentiation), while keeping in mind order of
operations; Employ {program}`VS Code` to write, edit, and save {program}`Python`
code; Output {program}`Python` data from script to screen; use various built-in
and imported functions; import modules into script.


## Introduction

As you further explore programming, you will find that there are several
concepts and features hidden within each language that lend greatly to the
usability of the language in a niche field or when looking to solve a specific
problem in a specific way.

{program}`Python` contains several elements within its built-in modules that
apply to unique situations or tasks. In this activity, you will be asked to
delve deeper into the world of {program}`Python` modules. To learn about and
apply these modules, you will need to do some research on your own. Being able
to use your resources to help you find answers to difficult problems will be an
important skill for you to master, not only for this class, but also going
forward as an engineer.


## Part A: Finding and using {program}`Python` documentation

Open a {program}`MS Word` document and name it as
{glue:text}`../../../2_team_assignments.md::deliverable_py1_team_2_part_a_pdf:`. Either
use the internet or type {python}`help function_name` (e.g., {python}`help(round)`) into
the {program}`Python` console to answer the following questions. Also, not all questions
should be answered by the same student, so the name of the student who answered that
question should be listed.  Each student in the team should answer at least 1 of the
questions.

- For the {python}`random` module, what does the {python}`seed` function do, and
  why would you want to set a seed?

- What function in the {python}`random` module would you use to generate a
  random number between some value, `a`, and another value, `b`? Provide an
  example of a command that would give a random number between $5$ and $200$.

- From the {python}`fractions` module, what does the {python}`limit_denominator`
  function do, and why might it be useful?

- From the {python}`math` module, what range of values will the {python}`asin()`
  function accept?

- From the {python}`math` module, what does the {python}`exp` function do?

- From the {python}`math` module, what does the {python}`sqrt` function do and
  what range of values will it accept?

- From the {python}`math` module, what do the {python}`degrees` and
  {python}`radians` functions do?

- What does the built-in {python}`input()` function do?

- What inputs does the built-in {python}`round()` function take?

- What do the {python}`int()` and {python}`float()` built-in functions do?

- Investigate the difference between the following import methods and how they affect
  the calling of functions:

  ```python
  from <module> import <function>
  import <module>
  ```

Save your document as a PDF file (By going to {menuselection}`File --> Print -->
Microsoft Print to PDF`).


## Part B: Using these modules in a script

You are spending your next summer consulting at a start-up company that creates on-line
educational tools to assist elementary school students in practicing math. You are
working on a tool that demonstrates to students the equivalence between doing
calculations with decimal numbers and doing the same calculations with fractions. The
tool should randomly generate four numbers as follows:

- The first number must be between $0$ and $100$.
- The second number must be between $10$ and $50$.
- The third number must be between $20$ and $40$.
- The fourth number must be between $100$ and $200$.

Add the numbers together, and then convert these numbers to fractions and repeat the
addition using the fractions. The random numbers should all be rounded to
{{ precision_str }} decimal digits, as should the sum of these numbers. The fractions
should be printed to the screen with a denominator smaller or equal to
{{ max_denominator_str }}. An example output is shown below.

Open the template, {download}`ENGR131_Python_Template.py
</Part_04_Python/ENGR131_Python_Template.py>`, and rename it as
{glue:text}`../../../2_team_assignments.md::deliverable_py1_team_2_py:` that will follow
the procedure outlined above. Utilizing {python}`random.seed(int(input("Enter the seed:
")))` before generating the random numbers initially is required in your program for it
to be graded properly.

% Automatically generated Sample Output section.
```{include} /_build/intermediate/Part_04_Python/M1/tasks/team_2/a/sample_output.md
```

Before you start programming in {program}`Python`, create a flow chart
representing the algorithm and save it in a PDF file that will be named
{glue:text}`../../../2_team_assignments.md::deliverable_py1_team_2_pdf:`.

Note that your program will be graded based upon the output and the process that you
used to reach this output. Your program should not produce any errors when running or
points will be deducted. Do not use the {python}`input()` function except to set the
seed for the pseudo-random number generator.

```{list-table} Deliverables
:class: deliverables
:name: tab:Py:M1:team_2_deliverables
:header-rows: 1

* - Deliverables
  - Description
* - {glue:text}`../../../2_team_assignments.md::deliverable_py1_team_2_part_a_pdf:`
  - Your PDF document answering the questions in Part A.
* - {glue:text}`../../../2_team_assignments.md::deliverable_py1_team_2_py:`
  - Your completed {program}`Python` code.
* - {glue:text}`../../../2_team_assignments.md::deliverable_py1_team_2_pdf:`
  - Flowchart(s) for this task.
```
