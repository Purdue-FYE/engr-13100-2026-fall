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

# Team Task 3

## Learning Objectives

Read and interpret a flowchart that contains user-defined functions; Design a program
with user-defined functions; Understand the execution sequence for a program with
user-defined functions.


## Introduction

As the scripts and programs we write become more complex, we often do not want to put
all of our code directly in the {python}`main` function. {program}`Python` allows users
to easily write their own functions in order to modularize their programs; these are
called user-defined functions.


## Task Instructions

Your team is designing an electric vehicle that will be charged by a wind turbine. You
want to write a program that gives a rough estimate for how far the vehicle can travel
after a given amount of charging time. A flowchart for that program is shown in
{numref}`fig:Py:M1:task3:flowchart`.  Find the output of the program given the following
initial conditions:


```{table} Cases for M05 team task 3
:class: cases
:name: tab:M05:team_cases

| $\rho$ (${\kilo\gram}/{\meter^3}$) | A (${\meter^2}$) | $C_p$ | v (${\meter}/{\second}$)| t ($\text{hour}$) | $\epsilon_v$ |
|:----------------------------------:|:----------------:|:-----:|:-----------------------:|:----------:|:-------------|
|                                1.2 |              400 |   0.3 |                       6 |          1 |        0.007 |
|                                1.2 |             2500 |   0.3 |                       4 |          5 |        0.007 |
```

The power of the wind turbine is given by:

```{math}
:label: eq:py1:power

P =  \frac{1}{2} \rho A v^3 C_p
```

Where
- $P$ is the power
- $\rho$ is the air density
- $A$ is the rotor swept area
- $v$ is the wind velocity
- $C_p$ is a coefficient of efficiency

The energy in the car is given by:

```{math}
:label: eq:py1:energy

E = Pt
```

Where
- E is the energy
- P is the power
- t is the time

The distance that an electric vehicle can travel is given by:
```{math}
:label: eq:py1:distance

d = E\epsilon_v
```

Where
- d is the distance
- E is the energy
- $\epsilon_v$ is the vehicle efficiency

```{admonition} Note
   :class: note

   Convert the radius from m to km before printing to the terminal. This can be done using simple division in {program}`Python`
```

```{figure} flowchart.png
:name: fig:Py:M1:task3:flowchart

Flowchart for Team Task 3
```

Save your answers to a PDF named {glue:text}`../../../2_team_assignments.md::deliverable_py1_team_3_pdf:`.

```{list-table} Deliverables
:class: deliverables
:name: tab:Py:M1:team_3_deliverables
:header-rows: 1

* - Deliverables
  - Description

* - {glue:text}`../../../2_team_assignments.md::deliverable_py1_team_3_pdf:`
  - PDF with answers to the task
```
