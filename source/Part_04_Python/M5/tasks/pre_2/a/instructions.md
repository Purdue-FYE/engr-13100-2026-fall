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

(PY:M5:PCA2)=
# PCA: Linear Regression Analysis (Part 2)

## Learning Objectives

- [insert objectives here]

## Files Needed

Download the Python template {download}`ENGR131_Python_Template.py </Part_04_Python/ENGR131_Python_Template.py>` and save it as {glue:text}`../../../../../glue_factory.md::py5_pre_1_py:`.

Download the CSV file {download}`thermal_expansion_data.csv </Part_04_Python/M5/tasks/pre_1/a/thermal_expansion_data.csv>` for analyzing thermal expansion along an aluminum beam.

## Activity Instructions & Submission

You are analyzing thermal expansion of a long aluminum beam used in an engineering structure (e.g., bridge, rail, or turbine casing).
Measurements were taken at three different locations along the beam:

Site 1: Near a fixed support
Site 2: Mid-span
Site 3: Near a free end

Because of constraints, material inconsistencies, or temperature gradients, each location shows slightly different expansion behavior.

**Dataset Columns**

| Column       | Description                                                              |
|--------------|--------------------------------------------------------------------------|
| Temp_C       | Aluminum temperature (°C)                                                |
| Site         | Monitoring site (A = Near fixed point, B = Mid-span, C = Near free end)  |
| Expansion_mm | Thermal expansion at aluminum beam                                       |


**Use linear regression to**:

1. Model how thermal expansion depends on temperature
2. Compare expansion behavior across different locations
3. Interpret physical differences in the system

### Follow these steps:

#### Part 1

Import the required libraries:

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot
from sklearn.linear_model import LinearRegression
```

#### Part 2

Import the dataset ("thermal_expansion_data.csv") and store it in a pandas DataFrame. Then, display the first 12 rows of the DataFrame.

```{admonition} Note
   :class: note

See the sample output below for understanding how to format your program output.
```

#### Part 3

Plot the thermal expansion data for all three sites against the measured temperature range. The plot type should be a scatter plot with different colors and shapes for each site's data points. The legend should include clear labels for each site dataset. Set the figure size to 10 x 6.

Remember to following the recommended guidelines [INSERT LINK TO PLOT GUIDANCE HERE] for creating professional and comprehensive plots. Save the figure as "exp_temp_plot.png".

<!-- Once the figure is formatted and generated, save the figure as "exp_temp_plot.png" and close it using `plt.close()`. -->

#### Part 4

Use the `scikit-learn` library to compute a `LinearRegression` object and fit it to the data.

Then, display the linear regression results: model equation, slope, y-intercept, R^2 value, sum of squared errors (SSE), and sum of squares total (SST).

Review the pre-class materials [INSERT LINK HERE] from the Linear Regression Excel unit to refresh your memory on linear regression and least-squares regression formulas.

#### Part 5

Generate predicted y-values for the regression line, then add the regression line to your existing scatter plot. The regression line should appear black on the plot.

Add the regression model equation and r² to the plot legend along with data collected from the three sites along the aluminum beam. Save the figure as "exp_temp_regression_plot.png".

<!-- Once the figure is formatted and generated, save the figure as "exp_temp_regression_plot.png" and close it. -->

% Automatically generated Sample Output section.
```{include} /_build/intermediate/Part_04_Python/M5/tasks/pre_1/a/sample_output.md
```

### Deliverables

Submit your {program}`Python` file {glue:text}`../../../../../glue_factory.md::py5_pre_2_py:` and both plot images to (INSERT ASSIGNMENT NAME) on Gradescope.