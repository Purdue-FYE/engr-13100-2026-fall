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

(PY:M3:A1)=
# PY: Looping Structures

## In this assignment, you will:

- Design a flowchart that models a robot’s decision-making process in a conveyor belt system
- Interpret a written process description and translate it into a visual algorithm
- Use loops and conditional logic to represent how the robot evaluates different item types
- Convert user input into a usable data structure (array/list) for processing
- Write a Python program that implements the logic shown in your flowchart
- Apply modular programming and coding standards to organize and document your code
- Test your program using different inputs to verify correct behavior
- Identify and fix errors through debugging and test case analysis
- Reflect on how the algorithm could be improved for efficiency and real-world applications

## Learning Objectives

- PR01: Programming Standards
- PR02: Data Storage
- PR04: Modular Programming
- PR05: Code Structures
- PR06: Translate Program Descriptions
- PR07: Test cases & Tracking
- PR08: Debugging

## Q1 Robot Workflow Optimization
(XX Points)

### Background

Industrial engineers design efficient workflows for systems such as manufacturing lines and robotic processes.

In this assignment, you will first create a flowchart that models how a robot responds to different conditions in a workflow. You will then translate this flowchart into a Python program that executes the same process.

Think of your flowchart as a visual representation of an algorithm, and your code as the step-by-step decision-making system that a robot would follow in a real-world environment.

## Files Needed

Download the {program}`Python` template {download}`ENGR131_Python_Template.py
</Part_04_Python/ENGR131_Python_Template.py>` and save it as py2_ind_1_username.py.

```{admonition} Note
   :class: note

Remember to include comments in your python script to practice professional programming standards.
```

## Program Requirements

### Part 1

Create a flowchart that represents your robot’s decision-making process. Use the description below to guide your design.

We recommend using https://app.diagrams.net/ to design and export your flowchart as a .pdf file. Save and name your flowchart **py3__ind_1_flowchart_username.pdf**.

**Process Description:**

A robot moves through a sequence of items on a conveyor belt. Each item may require a different action.

First, The robot receives an input from the user ("user_input") in the form of a list separated by commas with no spaces. The list is then converted to an array called "items." Each item in the list may be one of the following: "normal," "fragile," "heavy," "error."

The robot will loop through the list one item at a time and decide what action to take based on the type of item.

**Robot Actions**

Your flowchart must display how the robot responds to each type of item:

- "normal" → "Moving item to standard bin"
- "fragile" → "Handling fragile item with care"
- "heavy" → "Activating lift assist for heavy item"
- "error" → "ALERT: Item error detected – robot needs help!"
- Any other value → "Sending item to inspection"

Additionally, if the list contains at least 3 "error" items, then the robot should stop looking at items on the conveyor belt and display: "ALERT: Too many errors - sending robot to inspection".

**Requirements**

Your flowchart should:

- Clearly show a for loop that processes each item in the list
- Include a conditional structure for item types
- Display the robot action/output for each possible condition

### Part 2

Write a Python program that executes the algorithm displayed in your flowchart. Remember to prompt the user for a list of items (```user_input```) separated by commas (no spaces). Then convert the user input into an array of strings called ```items```.

Use the sample output section below to verify that your program outputs correct values.

% Automatically generated Sample Output section.
```{include} /_build/intermediate/Part_04_Python/M3/tasks/ind_1/a/sample_output.md
```
### Part 3

Respond to the following short answer questions:

1. How would you improve the robot's algorithm to become more efficient?
2. What might an Industrial Engineer change in a real robot system?

### Deliverables

Submit your flowchart **py3_ind_1_flowchart_username.pdf**, python file {glue:text}`../../../../../glue_factory.md::py3_ind_1_py:`, and responses to the short answer questions to (INSERT ASSIGNMENT NAME) on Gradescope.
