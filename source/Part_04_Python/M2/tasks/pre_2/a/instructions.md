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

(Py:M2:py2_pre_2)=
# Pre-Class Activity #X: Logic & Modularity

## Learning Objectives

- PR01: Programming Standards
- PR02: Data Storage
- PR03: Calculations
- PR04: Modular Programming
- PR05: Code Structures
- PR06: Translate Program Descriptions
- PR07: Test cases & Tracking
- PR08: Debugging

## Background

Ohm’s Law $(V = I*R)$ relates voltage (V), current (I), and resistance (R) in electric circuits.
Using this, the power dissipated by a resistor in a circuit can be calculated using the equation below:

```{math}
:label: eq:py2:P

P = \frac{V^2}{R}
```

Where:
- $P$ is power measured in Watts (W)
- $V$ is voltage in measured in Volts (V)
- $R$ is resistance measured in ohms ($\Omega$)

This is useful for estimating heating in resistors and designing safe circuits.

## Files Needed

For this assignment, download the {program}`Python` template {download}`ENGR131_Python_Template.py </Part_04_Python/ENGR131_Python_Template.py>` and save as {glue:text}`../../../../../glue_factory.md::py2_pre_2_py:`.

## Activity Instructions & Submission

Write a user-defined function (UDF) that calculates power ($P$) using the following information:

    Function name: calc_power
    Inputs: V, R
    Output: P

Your Python code should prompt user for voltage and resistance, calculate power using the calc_power function, then print the results for power in Watts (W) formatted to two decimal places.

Test your Python code using the sample input/output below.

% Automatically generated Sample Output section.
```{include} /_build/intermediate/Part_04_Python/M2/tasks/pre_2/a/sample_output.md
```

### Deliverables

Submit your python file {glue:text}`../../../../../glue_factory.md::py2_pre_2_py:` to (INSERT ASSIGNMENT NAME) on GradeScope.