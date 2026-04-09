---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
deliverables:

---
```{include} /macros.md
```
(EX:M2:PCA1)=
# PCA: Descriptive Statistics & Logical Functions

## Learning Objectives

{{PR02}}
{{PR03}}
{{PR05}}

## Files Needed
Download and open the following file for this activity:{download}`PCA_BatteryLife_login.xlsx<PCA_BatteryLife_login.xlsx>`

## Deliverables
You will complete your work in the provided Excel file and submit:
- A PDF showing calculated values
- A PDF showing formulas used

## Background
Engineers frequently analyze performance data to determine whether systems meet required specifications.

You are given the results from battery life tests for a prototype drone sensor. Each trial measures how long the sensor remained active during testing.

Your task is to summarize the dataset using descriptive statistics and apply logical functions to determine whether the sensor meets the required performance standard.

## Instructions
### Part A - Descriptive Statistics
Using Excel built-in functions, calculate the following values for the battery life dataset:

- Mean battery life
- Median battery life
- Mode (if one exists)
- Range of the dataset
- Standard deviation (sample)

Place your results in the designated summary cells using appropriate Excel built-in functions. Review {doc}`PCMs: Data Analysis & Histograms in Excel <../../../1.1_materials>` as needed. Do not type data values directly into your formulas.

### Part B - Logical Functions
Engineers must determine whether the sensor meets the minimum performance requirement. The sensor must operate for at least 80 minutes during a test.

In the column labeled **Requirement Met**, use an `IF` function that returns: 
- `PASS` if the battery life is greater than or equal to 80 minutes. 
- `FAIL` if the battery life is less than 80 minutes. 

Your formula should reference the appropriate cell containing the battery life value. Copy the formula down the column so that every trial is evaluated.

### Part C - Counting Results
Using Excel built-in functions, determine: 
- The number of trials that passed the requirement
- The number of trials that failed the requirement

```{admonition} Hint
:class: tip
Use the `=COUNTIF` function. Do not count these values manually.  
```

### Expected Value Check
After completing your calculations: 
- The mean battery life should be approximately 81-83 minutes.
- The standard deviation should be approximately 7-9 minutes.
- The number of trials that pass should be double the number of trials that fail. 

If your results differ significantly, review your formulas and references. 

### Gradescope Submission Instructions - NEEDS UPDATING
Follow these steps carefully.