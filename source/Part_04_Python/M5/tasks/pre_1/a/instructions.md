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

(PY:M5:PCA1)=
# PCA: Linear Regression Analysis

## Learning Objectives

- [insert objectives here]

## Files Needed

Download the Python template {download}`ENGR131_Python_Template.py </Part_04_Python/ENGR131_Python_Template.py>` and save it as {glue:text}`../../../../../glue_factory.md::py5_pre_1_py:`.

Download the CSV file {download}`radioactive_decay.csv </Part_04_Python/M5/tasks/pre_1/a/radioactive_decay.csv>` for analyzing thermal expansion along an aluminum beam.

## Activity Instructions & Submission

Radioactive materials decay over time. The activity of a radioactive sample (measured in counts per second, or cps) decreases as the material decays. For certain decay processes, we can model the relationship between variables using linear regression.

**Write a Python program that**:

1. Loads and inspects a radioactive decay dataset
2. Creates a scatter plot of the data
3. Fits a linear regression model using the `scikit-learn` library
4. Plots the linear regression model on top of the scatter plot
5. Reports the model equation and other regression statistics

### Follow these steps:

#### Part 1

Import the required libraries:

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot
from sklearn.linear_model import LinearRegression
```

#### Part 2: 

Load the dataset 'radioactive_decay.csv' into a pandas DataFrame and display the first 10 rows.

**Dataset columns**:

| Column             | Description                                        |
|--------------------|----------------------------------------------------|
| time_days          | Time elapsed since initial measurement (days)      |
| remaining_fraction | Fraction of material remaining (unitless)          |

```{admonition} Note
   :class: note

See the sample output below for understanding how to format your program output.
```

#### Part 3

Create a scatter plot of the data:
- x-axis: time_days
- y-axis: remaining fraction

Remember to following the recommended guidelines [INSERT LINK TO PLOT GUIDANCE HERE] for creating professional and comprehensive plots. Save the figure as "radioactive_decay_plot.png".

<!-- Once the figure is formatted and generated, save the figure as "radioactive_decay_plot.png" and close it using `plt.close()`. -->

#### Part 4

Use the `scikit-learn` library to compute a `LinearRegression` object and fit it to the data.

#### Part 5

Display the slope and y-intercept of the fitted model.

#### Part 6

Generate predicted y-values for the regression line.

#### Part 7

Add the regression line to your existing scatter plot. The regression line should appear red on the plot. Save the figure as "radioactive_decay_regression_plot.png".

<!-- Once the figure is formatted and generated, save the figure as "radioactive_decay_regression_plot.png" and close it. -->

<!-- #### Part 8 -->

<!-- After displaying the completed plot, analyze the plot and answer the questions below:

-  Write the model equation in the form: `remaining_fraction = m * time_days + b` substituting the actual slope (m) and intercept (b) values.

-  Based on the slope, approximately how much does the remaining fraction change for every additional day?

-  According to the model, when would the remaining fraction reach 0? (Solve for time_days when y = 0.) Does this seem physically reasonable? -->

% Automatically generated Sample Output section.
```{include} /_build/intermediate/Part_04_Python/M5/tasks/pre_1/a/sample_output.md
```

### Deliverables

Submit your {program}`Python` file {glue:text}`../../../../../glue_factory.md::py5_pre_1_py:` and both plot images to (INSERT ASSIGNMENT NAME) on Gradescope.
