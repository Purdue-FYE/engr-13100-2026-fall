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

(PY:M4:PCA1)=
# PCA: Data Manipulation

## Learning Objectives

- PR01: Programming Standards
- PR02: Data Storage
- PR03: Calculations
- PR05: Code Structures

## Files Needed

Download the Python template {download}`ENGR131_Python_Template.py </Part_04_Python/ENGR131_Python_Template.py>` and save it as {glue:text}`../../../../../glue_factory.md::py4_pre_1_py:`.

Download the CSV file {download}`metal_mass_volume.csv <metal_mass_volume.csv>` for importing purposes.

## Activity Instructions & Submission

Write a python script that calculates density using the mass and volume data in metal_mass_volume.csv using a Pandas DataFrame and NumPy arrays. The equation for density is shown below:

$$
\rho = \frac{m}{V}
$$

where:
- $ \rho $ is density
- $ m $ is mass
- $ V $ is volume


### Follow these steps:

1. Load data from metal_mass_volume.csv into a Pandas DataFrame called `df`.
2. Print "Original Data:" and display the DataFrame on a new line.
3. Extract the data columns "Mass_g" and "Volume_cm3" from `df` and convert them to NumPy arrays called `mass` and `volume`.
4. Calculate `density` using the NumPy arrays.

```{admonition} Note
   :class: note

While it is possible to calculate density directly using Pandas DataFrame operations, this assignment emphasizes the use of NumPy arrays for numerical calculations. NumPy is specifically optimized for efficient, vectorized mathematical operations, making it significantly faster and more memory‑efficient than performing the same calculations directly within a Pandas DataFrame—especially when working with large datasets. By converting the data to NumPy arrays, this exercise demonstrates best practices for high‑performance numerical computing commonly used in engineering and scientific applications.
```

5. Add the density results to the DataFrame `df` with the column header `Density_g/cm3`.
6. Round the density values to one decimal place for clean presentation.
7. Print "DataFrame with Calculated Density" on a new line (skip one line) and display `df` on a new line.

**Reference the following terminal output when writing your Python script.**

    Original Data:
      Sample  Mass_g  Volume_cm3
    0      A     5.4           2
    1      B     9.0           2
    2      C    23.5           3
    3      D    25.8           3
    4      E    44.8           5
    5      F    62.4           8

    DataFrame with Calculated Values:
      Sample  Mass_g  Volume_cm3  Density_g/cm3
    0      A     5.4           2            2.7
    1      B     9.0           2            4.5
    2      C    23.5           3            7.8
    3      D    25.8           3            8.6
    4      E    44.8           5            9.0
    5      F    62.4           8            7.8

<!-- Test your program using the sample input/output below. -->

<!-- % Automatically generated Sample Output section.
```{include} /_build/intermediate/Part_04_Python/M4/tasks/pre_1/a/sample_output.md
``` -->

## Deliverables

Submit your Python file {glue:text}`../../../../../glue_factory.md::py4_pre_1_py:` to (INSERT ASSIGNMENT NAME) on Gradescope.
