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

(Py:M4:py4_pre_2)=
# PCA #X: Plotting & Statistics

## Learning Objectives

- PR01: Programming Standards
- PR02: Data Storage
- DV01: Table & Plot Formatting

## Files Needed

Download the {program}`Python` template {download}`ENGR131_Python_Template.py </Part_04_Python/ENGR131_Python_Template.py>` and save it as {glue:text}`../../../../../glue_factory.md::py4_pre_2_py:`.

Download the .csv file {download}`mild_steel_stress_strain.csv <mild_steel_stress_strain.csv>` for importing purposes.

## Activity Instructions & Submission

Write a Python program that imports data from an Excel file, stores the data in a Pandas data frame for cleaning and analysis, and plots the data in a scatter plot with a clear plot title, axis titles, and axis labels.

### Follow these steps:

1. Load data from mild_steel_stress_strain.csv into a Pandas data frame called 'data'.
2. Plot the x (strain) and y-values (stress) using the matplotlib library:
  
```python
import matplotlib.pyplot as plt
```

3. Format the plot as follows:
  - Plot title: "Mild Steel Stress-Strain Curve"
  - x-axis title: 'Stress' with units of MPa, where Pa is Pascals
  - y-axis title: 'Strain' displayed as a percentage
  - x-axis limits: 0% to 45%
  - y-axis limits: 0 to 500 MPa
  - Minor tick marks: on
  - Line and data point color: blue
  - Font size:
    - Plot title: 14
    - Axis labels: 12
    - Axis tick values: default

**Reference {numref}`fig:Py:M4:pre_2:mild_steel_stress_strain_curve` below when creating your plot.**

```{figure} mild_steel_stress_strain_curve.jpg
:name: fig:Py:M4:pre_2:mild_steel_stress_strain_curve
:alt: Line plot of engineering stress versus strain for mild steel, with stress shown in mega Pascals and strain in percent. The curve rises steeply at low strain, then transitions into a gradual increase, reaching a maximum stress of about 487 MPa near 30% strain, followed by a decline indicating necking and failure.

Stress-strain curve for mild-steel
```

## Deliverables

Submit your {program}`Python` file {glue:text}`../../../../../glue_factory.md::py4_pre_2_py:` to (INSERT ASSIGNMENT NAME) on Gradescope.

