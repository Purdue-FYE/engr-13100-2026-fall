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

(Py:M2:py2_pre_0_b)=
# Pre-Class Activity #X: Logic & Modularity

## Learning Objectives Covered

- PR01: Programming Standards
- PR02: Data Storage
- PR03: Calculations
- PR04: Modular Programming
- PR05: Code Structures
- PR06: Translate Program Descriptions
- PR07: Test cases & Tracking
- PR08: Debugging

## Q1 Escaping an Unknown Planet
(XX Points)

### Background

You find yourself abandoned on an unknown planet! However, since you are an aspiring engineer, you plan to design a rocket cable of getting you back home. To do so, you need to write a python program that estimates the minimum velocity your rocket must achieve to escape the gravitational field of this mystery planet. This minimum required velocity is commonly known as the escape velocity. However, you are only aware of the average density of the planet and its radius.

### Files Needed

Download the {program}`Python` template {download}`ENGR131_Python_Template.py
</Part_04_Python/ENGR131_Python_Template.py>` and save it as py2_ind_2_username.py. Use the sample output section below to verify that your program outputs correct values.

```{admonition} Note
   :class: note

Remember to include comments in your python script to practice professional programming standards.
```

### Program Requirements

As the scripts and programs we write become more complex, we often do not want to put all of our code directly in the `main` function. Python allows users to easily write their own functions in order to modularize their programs; these are called user-defined functions (UDFs).

For this assignment, a flowchart for your {program}`Python` program is shown in {numref}`fig:Py:M2:ind_1:flowchart`. Find the output of the program given the following initial conditions:

```{table} Table 6.1
:class: cases
:name: tab:M2:ind_2_cases

| $\rho$ $({\kilo\gram}/{\meter^3})$ | $r$ $({\meter})$ | $G$ $({\meter^3}/{\kg*\s^2})$ |
|:----------------------------------:|:---------------:|:----------------------------:|
|                             5513.0 |         6371000 |       $6.6743\times10^{-11}$ |
|                             1879.8 |         2574730 |       $6.6743\times10^{-11}$ |
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

Convert the radius from m to km before printing to the terminal. This can be done using simple division in  {program}`Python`
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

Submit your python file (py2_ind_1_username.py) to (INSERT ASSIGNMENT NAME) on GradeScope.