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
(PY:M3:ICA1)=
# ICA: Looping Structures

## Learning Objectives

- PR01: Programming Standards
- PR02: Data Storage
- PR03: Calculations
- PR04: Modular Programming
- PR05: Code Structures
- PR06: Translate Program Descriptions
- PR07: Test cases & Tracking
- PR08: Debugging

## Background

You are at the park with your dog testing a new gadget: a super tennis ball launcher. As an aspiring engineer, you want to calculate how high the machine can throw a tennis ball.

<<<<<<< HEAD
One of Newton’s kinematic equations is:
=======
One of Newton’s kinematic equations for motion with constant acceleration is:
>>>>>>> 1079af7efff7bb6b24fb3a6cba2a9b586ec08884

```{math}
:label: eq:py3:P

x = vt + \frac{1}{2}at**2
```

Where:
- $x$ is displacement ($m$)
- $v$ is initial velocity ($\frac{m}{s}$)
- $a$ is acceleration ($\frac{m}{s^2}$)
- $t$ is time ($s$)

<<<<<<< HEAD
You also know that when an object is in free fall, it experiences a constant acceleration due to gravity (9.81 $\frac{m}{s^2}$).

## Files Needed

Download the Python template {download}`ENGR131_Python_Template.py </Part_04_Python/ENGR131_Python_Template.py>` 
=======
You also know that when an object is in free fall, it experiences a constant acceleration due to gravity of 9.81 $\frac{m}{s^2}$.

## Files Needed

Download the Python template {download}`ENGR131_Python_Template.py </Part_04_Python/ENGR131_Python_Template.py>`
>>>>>>> 1079af7efff7bb6b24fb3a6cba2a9b586ec08884

## Activity Instructions & Submission

Write a Python program that calculates and displays the height of a tennis ball at each second after it is launched straight up. Your program should calculate the height for each second from 1 to 5 seconds after launch.

Your program must prompt the user to enter the tennis ball’s initial velocity (in m/s).

For each second, your program should:
- Calculate the height of the tennis ball using the equation provided in the background section.
- Display the time and the calculated height.

Your program should also check for the following conditions during the calculation:
- If the tennis ball reaches a height greater than 25 meters, display the height and that you have lost the ball in the sun.

- If the tennis ball reaches the ground (height ≤ 0 meters), your program should display a message indicating that the ball has hit the ground and stop calculating additional time steps.

If neither condition occurs, the program should continue calculating and displaying the height for the remaining seconds, up to 5 seconds total.

For more information on program output and testing your Python code, see the sample input/output section.

% Automatically generated Sample Output section.
<<<<<<< HEAD
```{include} /_build/intermediate/Part_04_Python/M3/tasks/ICA_1/a/sample_output.md
```
=======
>>>>>>> 1079af7efff7bb6b24fb3a6cba2a9b586ec08884
