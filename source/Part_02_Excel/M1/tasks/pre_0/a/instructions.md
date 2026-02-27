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
  - PowerDataValues_pdf
  - PowerDataFormulas_pdf
---
```{include} /macros.md
```
(Ex:M1:task0)=
# PCA #1: Engineering Data Analysis in Excel

## Learning Objectives

{{PR01}}
{{PR02}}
{{PR03}}
{{DV01}}

## Files Needed
Download and open the following file for this activity:{download}`PCA01_PowerData_login.xlsx<PCA01_PowerData_login.xlsx>`

## Deliverables
You will complete your work in the provided Excel file and submit:
- A PDF showing calculated values
- A PDF showing formulas used
- Responses to questions directly in Gradescope

## Background
Engineers frequently analyze power usage data to evaluate system performance and efficiency.

You are given one week of electrical energy usage data for a laboratory system. Your task is to organize the data, perform calculations using built-in Excel functions, apply proper cell referencing, and create a clear chart to communicate results.

Follow the Spreadsheet Foundations guidelines from the PCM.

## Instructions
### Part A - Organizing Data
In the **Raw Data** section of the worksheet: 
- Ensure headers are clear and descriptive
- Include units in headers
- Keep one variable per column
- Do not use merged cells
- Ensure the dataset has no blank rows

Your spreadsheet should be readable by another engineer. 

### Part B - Built-in Functions
Using Excel built-in functions, calculate: 
1. Total weekly energy usage
2. Average daily energy usage
3. Maximum daily energy usage
4. Minimum daily energy usage
5. Number of recorded days

```{admonition} Functions
:class: tip
Use appropriate functions such as `=SUM()`, `=AVERAGE()`, `=MAX()`, `=MIN()`, and `=COUNT()`. Do not type numbers directly into your formulas. 
```

### Part C - Unit Conversion
Engineers often convert between measurement units. Convert the daily energy values from **kWh to Joules** using the built-in function: 

`=CONVERT(cell,"kWh","J")`

Requirements: 
- Use cell references (do not type the values manually)
- Copy the formula down the column
- Ensure all values calculate correctly

### Part D - Referencing and Constants
A performance adjustment factor of 1.08 is stored in a designated cell in the worksheet. Multiply each daily energy value by the adjustment factor. 

Your formula must: 
- Use a relative reference for the daily energy value
- Use an absolute reference for the adjustment factor

When copied down the column, your formula should work correctly without editing. 

### Part E - Data Visualization
Create a **bar chart (clustered column chart) that displays: 
- Day on the horizontal (x) axis
- Energy Usage (kWh) on the vertical (y) axis. 

Your chart must include: 
- A descriptive chart title
- Horizontal axis label: **Day**
- Vertical axis label: **Energy Usage (kWh)**
- Clear, readable formatting

The chart should clearly communicate the variation in energy usage across the week. Place the chart below the dataset without covering any data or calculations. 

### Expected Value Check
After completing your calculations: 
- The total weekly energy should be approximately 850 kWh. 
- The average daily energy should be approximately 121.43 kWh. 
- The adjusted energy on Friday should be approximately 124.2 kWh. 

If your results differ significantly, review your formulas and references. 

### Gradescope Submission Instructions
You will submit two PDF files and complete short-answer questions in Gradescope.

Follow these steps carefully.

#### Step 1 - Export Values PDF
1. In Excel, ensure: 
  - all calculations are visible
  - the chart is visible and readable
  - no error messages appear
2. Go to **File > Export > Create PDF** (or Save As > PDF)
3. Save the file as deliverable_PowerData_pdf, replacing "login" with your Purdue username. 

#### Step 2 - Export Formulas PDF
1. In Excel, enable **Show Formulas**: 
  - Windows: Press **Crtl + `**
  - Mac: Press **Control + `**
2. Confirm:
  - All formulas are visible
  - No values are displayed
3. Export again as a PDF.
4. Save the file as `PCA01_PowerData_formulas_login.pdf`, replacing "login" with your Purdue username. 

#### Step 3 - Upload Files to Gradescope
1. Go to the PCA #1 assignment in Gradescope. 
2. Upload both PDF files: 
  - `PCA01_PowerData_values_login.pdf`
  - `PCA01_PowerData_formulas_login.pdf`
3. Navigate to the short-answer questions. 
  1. Paste your formulas exactly as they appear in Excel. 
    - Include the equal sign `=`
    - Do not include extra spaces
  2. Answer the conceptual questions in 2-3 complete sentences. 
4. Click **Submit Assignment**
```