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

(PY:M5:A1)=
# PY: Regression

## In this assignment, you will:

- Load and explore a real-world-style environmental dataset
- Create professional scientific visualizations using `matplotlib`
- Build a linear regression model using `scikit-learn`
- Evaluate model performance using statistical metrics
- Interpret the physical meaning of your results

## Learning Objectives

- [insert objectives here]

## Q1 Wabash River Health: Dissolved Oxygen Analysis
(90 pts)

### Background

Dissolved Oxygen (DO) is one of the most critical indicators of river health. Fish and aquatic organisms need adequate DO to survive. DO levels are strongly influenced by water temperature: warmer water holds less dissolved oxygen (an inverse relationship).

As a junior environmental engineer at the fictional Wabash River Authority, you have been given 20 water quality measurements collected over a summer monitoring campaign. Your task is to:

1. Visualize the relationship between temperature and DO
2. Build a linear regression model to predict DO from temperature
3. Evaluate your model's performance
4. Use your model to make engineering decisions

### Files Needed

Download the {program}`Python` template {download}`ENGR131_Python_Template.py </Part_04_Python/ENGR131_Python_Template.py>` and save it as {glue:text}`../../../../../glue_factory.md::py5_ind_1_py:`.

Download the CSV file {download}`river_data.csv </Part_04_Python/M5/tasks/ind_1/a/river_data.csv>` for analyzing the Wabash river dissolved oxygen data.

### Program Requirements

**Dataset Description**

You are provided with a CSV file named: river_data.csv. The dataset contains water quality measurements collected at three Wabash River monitoring sites.

**Dataset Columns**

| Column     | Description                                                     |
|------------|-----------------------------------------------------------------|
| sample_id  | Unique sample identifier                                        |
| site       | Monitoring site (A = upstream, B = midstream, C = downstream)   |
| temp_c     | Water temperature (°C)                                          |
| do_mg_l    | Dissolved oxygen concentration (mg/L)                           |
| ph         | Water pH                                                        |

**Required Libraries**

- numpy
- pandas
- matplotlib
- scikit-learn

#### Part 1: Load and Explore the Dataset

1. Import the required libraries

2. Load the CSV file into a pandas DataFrame

3. Print the first five rows of the DataFrame

3. Print:
    - A formatted assignment header
    - summary statistics for:
      - temperature
      - dissolved oxygen
      - pH

See the sample output below to review formatting for print statements.

```{admonition} Hint
   :class: hint

Use the `describe()` function to generate summary statistics.
```

#### Part 2: Exploratory Scatter Plot

Create a scatter plot showing the relationship between water temperature (x-axis) and dissolved oxygen concentration.

Use a separate color and marker shape for each monitoring site. Be sure to follow the professional plotting guidelines (see "Data Analysis & Visualization" materials) to ensure readability.

Save the figure as "DO_temp_plot.png".

#### Part 3: Linear Regression Analysis

Use the **scikit-learn** library to model the relationship between temperature and dissolved oxygen.

1. Define the independent variable (x, temperature) and dependent variable (y, dissolved oxygen concentration).

```{admonition} Hint
   :class: hint

Rememeber: scikit-learn requires a 2D feature array.
```

2. Use `LinearRegression()` to fit the model to your data.

3. Compute slope, intercept, and predicted y-values.

4. Calculate Sum of Squared Errors (SSE), Sum of Square Total (SST), and r² value.


```{admonition} Hint
   :class: hint

Refer back to the "Linear Regression" materials from our Excel unit to refresh your memory on the purpose of linear regression and least-squares regression.
```

5. Print your results in the following order (see sample output) and format values to 3 decimal places.
    - Regression equation
    - Slope
    - Intercept
    - R²
    - SSE
    - SST

#### Part 4: Regression Line Plot

Create another plot showing the original scatter plot and the fitted regression model.

1. Use the `np.linspace()` function to generate evenly spaced temperature values across the observed range. Then, predict dissolved oxygen values using your regression model.

2. Overlay the original scatter data points and the regression model.

3. Add the regression model equation and R² to the plot legend.

4. Save the figure as: "DO_temp_regression_plot.png".

% Automatically generated Sample Output section.
```{include} /_build/intermediate/Part_04_Python/M5/tasks/ind_1/a/sample_output.md
```

### Deliverables

Submit your {program}`Python` file {glue:text}`../../../../../glue_factory.md::py5_ind_1_py:` and both plot images to (INSERT ASSIGNMENT NAME) on Gradescope.

## Q2 Reflection Questions
(10 pts)

1. What does the sign of the slope tell you physically about the relationship between temperature and dissolved oxygen?

2. Your R² value should be close to 1.0. What does this indicate about how well temperature explains dissolved oxygen variation? Name ONE additional environmental variable that could affect dissolved oxygen.

3. Do the data points appear to follow a linear trend? Additionally, what might suggest that a nonlinear model would work better?

4. Why would it be physically unreasonable to use this regression model to predict dissolved oxygen at 0 °C? 50 °C? What is this modeling limitation called?

5. Site C is downstream and tends to have lower dissolved oxygen than Sites A and B. Suggest ONE engineering or environmental reason why downstream dissolved oxygen may be lower.

