<!-- """
Course Number: ENGR 13100
Semester: Fall 2026

Description:
    Replace this line with a description of your program.

Assignment Information:
    Assignment:     7.1.2 pre_2
    Team ID:        LC0 - 00
    Author:         Dr. Holly Fortener, hforten@purdue.edu
    Date:           03/27/2026

Contributors:
    Name, login@purdue [repeat for each]

    My contributor(s) helped me:
    [ ] understand the assignment expectations without
        telling me how they will approach it.
    [ ] understand different ways to think about a solution
        without helping me plan my solution.
    [ ] think through the meaning of a specific error or
        bug present in my code without looking at my code.
    Note that if you helped somebody else with their code, you
    have to list that person as a contributor here as well.

Academic Integrity Statement:
    I have not used source code obtained from any unauthorized
    source, either modified or unmodified; nor have I provided
    another student access to my code.  The project I am
    submitting is my own original work.
""" -->

```python
import matplotlib.pyplot as plt
import pandas as pd

# Step 1: Import data from Excel into a Pandas DataFrame
file_path = "source/Part_04_Python/M4/tasks/pre_2/a/mild_steel_stress_strain.csv"
data = pd.read_csv(file_path)

# Step 2: Plot the original data
plt.figure(figsize=(10, 6))
plt.plot(data["strain_percent"], data["stress_MPa"], label="Original Data",
        marker="o", color="blue", linestyle="-")
plt.title("Mild Steel Stress-Strain Curve", fontsize=14)
plt.xlabel("Strain (%)", fontsize=12)
plt.ylabel("Stress (MPa)", fontsize=12)
plt.ylim(0, 500)
plt.xlim(0, 45)
plt.grid(True)
plt.minorticks_on()
plt.show()
```

#### Image of Plot:

![Line plot of engineering stress versus strain for mild steel, with stress shown in mega Pascals and strain in percent. The curve rises steeply at low strain, then transitions into a gradual increase, reaching a maximum stress of about 487 MPa near 30% strain, followed by a decline indicating necking and failure.](mild_steel_stress_strain_curve.jpg)