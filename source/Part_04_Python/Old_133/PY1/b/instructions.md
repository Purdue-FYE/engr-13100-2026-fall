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
    # Ensure these match the assigned values in the pre-task
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

# Team Task 1


## Learning Objectives

Create and execute simple scripts comprised of basic {program}`Python` concepts.
Apply course code standard in development of {program}`Python` scripts.
Modularize and comment code for readability and reusability.


## Task Instructions

Compare your results for the pre-task assignment with your team members (Task 0). Run each member's code and compare results with the given solutions. Discuss the differences and similarities of your approaches, highlighting strengths of each.

Choose one team member's pre-class activity working code file to turn in as a part of this reflection. Save the file as {glue:text}`../../../2_team_assignments.md::deliverable_py1_team_1_py:` and turn it in with the remainder of the team task assignment files in Gradescope.


1. Open the Reflection Template {download}`py1_team_1_teamnumber.docx`. Save it with
   your team number replacing {file}`teamnumber` in the file name and answer the questions.


1. What similarities did you notice between the team's codes? What differences?
2. Did you use `.3f` or `format()`? What are the benefits of each method?
3. How would your output change if you used `.,3f` instead? What about `._3f`? Why would you want to use these?
4. For each team member, rank your comfort level in the following skills from 1 (not comfortable) to 5 (most comfortable).

    a. Using {program}`Python` IDE

    b. Writing comments and print statements in {program}`Python`

    c. Mathematical operations in {program}`Python`

5. Which working code did the team decide to submit and why? What are the strengths of this approach?


Save the reflection as {glue:text}`../../../2_team_assignments.md::deliverable_py1_team_1_pdf:` and turn it in with the remainder of the team task assignment files in Gradescope.

```{list-table} Deliverables
:class: deliverables
:name: tab:Py:M1:team_1_deliverables
:header-rows: 1

* - Deliverables
  - Description

* - {glue:text}`../../../2_team_assignments.md::deliverable_py1_team_1_py:`
  - The {program}`Python` code file chosen by the team for submission.

* - {glue:text}`../../../2_team_assignments.md::deliverable_py1_team_1_pdf:`
  - The completed team reflection document.
```
