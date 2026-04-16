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

(PY:M2:A1)=
# PY: Logic & Modularity

## In this assignment, you will:

- Apply logical decision-making using `if`, `elif`, and `else` statements to solve real-world engineering problems.
- Validate and manage user input to ensure accurate and reliable program behavior.
- Translate written problem statements and flowcharts into functional Python code.
- Develop and implement user-defined functions (UDFs) to modularize and organize your programs.
- Perform engineering calculations using mathematical formulas and appropriate units.
- Practice professional programming standards, including commenting, readability, and structure.
- Test and debug your code using provided cases to verify correctness.

## Learning Objectives

- PR01: Programming Standards
- PR02: Data Storage
- PR03: Calculations
- PR04: Modular Programming
- PR05: Code Structures
- PR06: Translate Program Descriptions
- PR07: Test cases & Tracking
- PR08: Debugging

## Q1 Testing an Irrigation System
(XX Points)

### Background

You are a junior agricultural engineer supporting a local farmer who suspects the irrigation system isn’t watering consistently. Your supervisor asks you to create a tiny console tool that makes a clear recommendation—Run, Run Reduced, Delay, or Do Not Irrigate—based on a few simple inputs: soil moisture, forecast rain, and any obvious system issues.

Your task is to write a short Python program using `if‑elif‑else` to decide the recommendation and validate inputs to prevent nonsense values. You’ll also sketch a small flowchart showing your program’s decision path.

### Files Needed

Download the {program}`Python` template {download}`ENGR131_Python_Template.py </Part_04_Python/ENGR131_Python_Template.py>` and save it as {glue:text}`../../../../../glue_factory.md::py2_ind_1_py:`. Use the sample output section below to verify that your program outputs correct values.

```{admonition} Note
   :class: note

Remember to include comments in your python script to practice professional programming standards.
```

### Program Requirements

#### Part 1

Prompt the user for the following:

- Soil moisture (unit: percentage; float, 0-60)
- Forecasted rain (unit: mm; float, 0-50)
- Low pressure (yes/no)
- Maintenance needed (yes/no)

#### Part 2

Validate the user input:

- If a numeric input is outside the expected range, print a warning and use `return` to end the main function.
- If a yes/no input is something else, print a warning and treat it as "no" be default.

#### Part 3

Your program must follow this order of decisions:

1. If the user specifies that maintenance is required for the irrigation system, print "DO NOT IRRIGATE - maintenance required."
2. If the user specifies that the irrigation system is experiencing low pressure, print "DO NOT IRRIGATE - low pressure condition."
3. If the forecast is expecting 10 mm or more of rain, print "DELAY - significant rainfall expected."
4. If the soil moisture is measured at less than 20%, print "RUN FULL" to indicate the irrigation system will output the normal amount needed.
5. If soil moisture is greater than or equal to 20% AND less than or equal to 25%, print "RUN REDUCED" to indicate that system will output less water than normal.
6. Otherwise, if the soil moisture is greater than 25%, then print "SKIP - soil moisture is adequate".

% Automatically generated Sample Output section.
```{include} /_build/intermediate/Part_04_Python/M2/tasks/ind_1/a/sample_output.md
```

#### Part 4

Create a flowchart that shows your program’s decision path.

We recommend using https://app.diagrams.net/ to design and export your flowchart as a .pdf file. Reference the Flowcharts [INSERT LINK TO PRE-CLASS MATERIALS HERE] section of the Python 2 pre-class materials for which shapes to use.

### Deliverables

Submit your python file {glue:text}`../../../../../glue_factory.md::py2_ind_1_py:` to (INSERT ASSIGNMENT NAME) on Gradescope.

## Q2 Escaping an Unknown Planet
(XX Points)

### Background

You find yourself abandoned on an unknown planet! However, since you are an aspiring engineer, you plan to design a rocket cable of getting you back home. To do so, you need to write a python program that estimates the minimum velocity your rocket must achieve to escape the gravitational field of this mystery planet. This minimum required velocity is commonly known as the escape velocity. However, you are only aware of the average density of the planet and its radius.

### Files Needed

Download the {program}`Python` template {download}`ENGR131_Python_Template.py </Part_04_Python/ENGR131_Python_Template.py>` and save it as {glue:text}`../../../../../glue_factory.md::py2_ind_1_py:`.

### Program Requirements

As the scripts and programs we write become more complex, we often do not want to put all of our code directly in the `main` function. Python allows users to easily write their own functions in order to modularize their programs; these are called user-defined functions (UDFs).

For this assignment, a flowchart for your {program}`Python` program is shown in {numref}`fig:Py:M2:ind_1:flowchart`. Using the flowchart and the following initial conditions, develop a {program}`Python` program to determine the escape velocity.


```{table} 
:class: cases
:name: tab:M2:ind_2_cases

| $\rho$ $({\kilo\gram}/{\meter^3})$ | $r$ $({\meter})$ | $G$ $({\meter^3}/{\kg*\s^2})$ |
|:----------------------------------:|:---------------:|:------------------------------:|
|                             5513.0 |         6371000 |         $6.6743\times10^{-11}$ |
|                             1879.8 |         2574730 |         $6.6743\times10^{-11}$ |
```

The escape velocity of the projectile is given by:

```{math}
:label: eq:py2:v_e

v_e =  \sqrt(\frac{2Gm}{r})
```

Where
- $v_e$ is the escape velocity
- $G$ is the gravitational constant
- $m$ is the mass of the planet
- $r$ is the radius of the planet

The mass of the planet is given by:

```{math}
:label: eq:py2:mass

m = \rho*V
```

Where
- $\rho$ is the planet's average density
- $V$ is the volume

The volume of a sphere is given by (we approximate the planet’s shape to be a sphere):
```{math}
:label: eq:py2:volume_of_sphere

V = \frac{4}{3}*\pi*r^3
```

Where
- $r$ is the radius

```{admonition} Note
   :class: note

Convert the radius from m to km before printing to the terminal. This can be done using simple division in  {program}`Python`.
```

```{figure} flowchart.jpg
:name: fig:Py:M2:ind_1:flowchart

Flowchart for Individual Assignment
```

```{admonition} Hint
:class: hint

The flowchart includes multiple UDFs. Be sure to include all of the UDFs represented in the flowchart in your Python program.
```

### Deliverables

Submit your {program}`Python` file {glue:text}`../../../../../glue_factory.md::py2_ind_1_py:` to (INSERT ASSIGNMENT NAME) on Gradescope.

## Q3 Analysis Questions

Navigate to (INSERT ASSIGNMENT NAME) on GradeScope and answer the following:

1. How do you think the {program}`Python` program you wrote Q1 or Q2 could be more efficient?

2. For Q1 and Q2, how is the context of each problem important?