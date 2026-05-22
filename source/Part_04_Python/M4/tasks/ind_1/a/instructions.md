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

(PY:M4:A1)=
# PY: Data Analysis & Visualization

## In this assignment, you will:

- Import CSV data into Python
- Work with NumPy arrays and perform elementwise operations
- Manipulate pandas DataFrames
- Calculate summary statistics
- Create professional engineering plots
- Interpret data trends and communicate findings clearly

## Learning Objectives

- Insert text here

## Q1 Traffic Flow Data Analysis & Visualization
(XX Points)

### Background

Civil engineers frequently analyze transportation and roadway data to improve traffic efficiency and safety.

A city transportation department collected traffic data from roadway sensors during a one-week study. Engineers want to determine how traffic volume changes with vehicle speed and road surface temperature.

You have been hired as a junior transportation engineer to analyze the dataset and present your findings.

### Files Needed

Download the {program}`Python` template {download}`ENGR131_Python_Template.py </Part_04_Python/ENGR131_Python_Template.py>` and save it as {glue:text}`../../../../../glue_factory.md::py4_ind_1_py:`.

Download the CSV file {download}`traffic_data.csv </Part_04_Python/M4/tasks/ind_1/a/traffic_data.csv>` for analyzing the collected traffic data.

```{admonition} Note
   :class: note

Remember to include comments in your python script to practice professional programming standards.
```

### Program Requirements

#### Part 1

1. Import the required libraries:
- numPy
- pandas
- matplotlib.pyplot
2. Load the CSV file into a pandas DataFrame called `df`.
3. Display:
- The first 5 rows of `df`
- Column names
- Number of rows and columns

#### Part 2

Transportation engineers often estimate roadway density using relationships between traffic volume and speed.

1. Convert the following columns from `df` into NumPy arrays:
- Vehicle_Count
- Avg_Speed_mph
2. Create a new NumPy array called traffic_index using the equation: 

```{math}
:label: eq:py4:traffic_index

\text{Traffic Index} = \frac{\text{Vehicle Count}}{\text{Avg Speed}} 
```

3. Multiply the traffic index by 1.15 to simulate increased congestion during construction.
4. Print the first 10 values of the new array.

#### Part 3

1. Add the traffic index array data to a new column in the DataFrame called `Traffic_Index`.
2. Create a new filtered DataFrame called `high_volume_df` that only in includes rows of data when `Vehicle_Count` is more than 400.
3. Create another filtered DataFrame called `low_speed_df` for when `Avg_Speed_mph` is less than 45.
4. Display:
- The first 5 rows of each filtered DataFrame
- The number of rows in each filtered dataset

#### Part 4

Civil engineers use statistics to evaluate roadway performance.

Calculate the following summary statistics for:
- Vehicle_Count
- Avg_Speed_mph
- Traffic_Index

Statistics:
- Mean
- Maximum
- Minimum
- Standard deviation

Round all values to two decimal places.

#### Part 5

Because you are an engineer, you know that plots follow engineer presentation standards and therefore include:

- Descriptive titles
- Clearly labeled axes
- Units when appropriate
- Readable font sizes
- Legends when multiple datasets are shown
- Grid lines when useful
- Professional formatting


##### Scatter Plot

Create a scatter plot of `Vehicle_Count` vs. `Avg_Speed_mph`. The plotted data points should be black, your plot should have a grid, and the figure size should be 10 x 5.

Save a picture of your scatter plot as "py4_ind_1_scatter.png".

##### Line Plot

Create a line plot that displays how `Vehicle_Count` changes over time for the month of June. Althought this is a line plot, be sure to include marker symbols to showcase the datapoints. The plotted line and data points should be blue, your plot should have a grid, and the figure size should be 10 x 5. Additionally, your data axis should only show days in June for tick marks.

Save a picture of your line plot as "py4_ind_1_line.png".

```{admonition} Hint
   :class: hint

You will need to use the `.to_datetime()` function to help format and filter the June data before plotting.
```

##### Combined Plot

Create a figure that includes both a line plot of `Vehicle_Count` and a scatter plot of `Avg_Speed_mph` over time for the month of June. Be sure to include a legend and set the figure size to 11 x 6. The line plot should be blue while the scatter plot is black.

Save a picture of your line plot as "py4_ind_1_combined.png".

% Automatically generated Sample Output section.
```{include} /_build/intermediate/Part_04_Python/M4/tasks/ind_1/a/sample_output.md
```
Aside from your figures, ensure that your program output matches the sample output exactly to ensure you receive full points from the auto grader.

### Deliverables

Submit your {program}`Python` file {glue:text}`../../../../../glue_factory.md::py4_ind_1_py:` and all of your plot pictures to (INSERT ASSIGNMENT NAME) on Gradescope.

## Q2 Interpretation & Presentation Standards

Navigate to (INSERT ASSIGNMENT NAME) on Gradescope and answer the following:

Answer the following questions in complete sentences.
1. Describe the relationship between vehicle count and average speed.
2. During what times of the month of June do traffic congestion appear to be highest?
3. How does the traffic index help engineers evaluate roadway conditions?
4. What other data would be helpful to acquire when analyzing the traffic data? Additionally, How would you visualize it?
5. Describe at least two ways to improve the presentation quality of engineering plots.