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
  - report_pdf
  - py
---
```{include} /macros.md
```

(Py:M1:py1_ind)=
# Assignment #X: Python Foundations

## In this assignment, you will:

- Collect and validate user input using variables and appropriate data types
- Simulate medical device testing using randomly generated data
- Store, access, and analyze test results using lists and indexing
- Apply mathematical operations to evaluate device performance
- Use logical decision-making to determine pass/fail outcomes
- Format and display professional, clearly labeled program output
- Apply basic string manipulation to clean and organize input data
- Identify and explain common Python errors encountered in programming
- Communicate technical results clearly through a short, written report

## Learning Objectives

- PR01: Programming Standards
- PR02: Data Storage
- PR03: Calculations
- PR08: Debugging

## Q1 Medical Device Prototype Testing Program
(XX Points)

### Background

You are a Biomedical Engineer working in a research and development lab. Your supervisor has asked you to create a Python program that simulates testing a new medical device prototype.

### Files Needed

Download the {program}`Python` template {download}`ENGR131_Python_Template.py </Part_04_Python/ENGR131_Python_Template.py>` and save it as {glue:text}`../../../../../glue_factory.md::py1_ind_1_py:`. Use the sample output section below to verify that your program outputs correct values.

```{admonition} Note
   :class: note

Remember to include comments in your python script to practice professional programming standards.
```

### Program Requirements

#### Part 1: User Input

Your program must ask the user for:
1. The medical device name
2. Prototype ID number
3. Researcher’s last name
4. Researcher’s title

#### Part 2: Professional Header

Output a clear, professional header that includes:
- The test information provided by the user
- The date and time of the test (timestamp)

#### Part 3: Simulated Test Data

Generate at least 5 random test values between 5 and 100. Store the values in a list.

#### Part 4: Mathematical Analysis

Using the list of test values, your program must:
- Calculate and display the average test value
- Perform one additional math calculation. Choose one: square root, sine of the average, a pi-based calculation.

```{admonition} Note
   :class: note

All values must be clearly labeled and formatted with two decimal places.
```

#### Part 5: Pass/Fail Evaluation

You must determine whether the device passes or fails based on this rule:

If the average test value is greater than or equal to a defined passing threshold created by you (e.g., threshold = 6), the device passes. Otherwise, it fails.

```{admonition} Note
   :class: note

Because we have not covered {python}`if` statements yet in this course, you cannot use an {python}`if` statement for this part of the assignment.
```

#### Part 6: String Processing & Data Organization

Your program must demonstrate:
- String concatenation or repetition in at least one output line
- Splitting at least one piece of user input into a sequence and displaying the result

### Output Requirements

Your program output must include:
1. A professional header
2. Clearly labeled test values and calculations
3. Pass/fail result
4. Clean formatting and spacing for readability

% Automatically generated Sample Output section.
```{include} /_build/intermediate/Part_04_Python/M1/tasks/ind_1/b/sample_output.md
```

### Deliverables

Submit your python file {glue:text}`../../../../../glue_factory.md::py1_ind_1_py:` to (INSERT ASSIGNMENT NAME) on Gradescope.

## Q2 Medical Device Prototype Testing Report

### Background

Your supervisor has asked you to report back with testing results.

Your written report should be written as a professional technical memo to your laboratory supervisor. Assume your supervisor is scientifically knowledgeable but did not run your program themselves. The report should be 1-2 well-structured paragraphs and have a clear, professional tone (no casual language). You may include bullet points to list items, but the entire report cannot be organized in bullet points.

#### Content Requirements

Your memo must address the following:

**1.	Purpose of the Program**
- What the medical device testing program is designed to simulate
- What kind of data the program generates and why it is relevant to prototype evaluation

**2. Testing & Analysis Process**
- How test values were generated
- How the data was stored and analyzed

**3. Performance Evaluation**
- Pass/fail criteria used in the program
- How the program determines and report the final device status

**4. Technical Challenges & Debugging**
- One programming error you encountered
- What caused the error
- How you identified and corrected it

### Deliverables

Submit your report named {glue:text}`../../../../../glue_factory.md::py1_ind_1_report_pdf:` to (INSERT ASSIGNMENT NAME HERE) on Gradescope.

```{admonition} Note
   :class: note

We recommend writing and saving your report in a .txt file or MS Word document and then copy-paste it into Gradescope. You can reference your report in the saved file for future assignments with similar tasks.
```
