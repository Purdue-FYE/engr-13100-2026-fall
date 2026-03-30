<!-- Course Number: ENGR 13100
Semester: Fall 2026

Description:
Replace this line with a description of your program.

Assignment Information:
Assignment:     7.1.1 pre_1
Team ID:        LC0 - 00
Author:         Dr. Holly Fortener, hforten@purdue.edu
Date:           03/30/2026

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
submitting is my own original work. -->

```python
import numpy as np
import pandas as pd  

# Step 1: Import data from Excel into a Pandas DataFrame
file_path = "source/Part_04_Python/M4/tasks/pre_1/a/metal_mass_volume.csv"
df = pd.read_csv(file_path)

# Step 2: Print the original DataFrame
print("Original Data:")
print(df)

# Step 3: Convert columns to NumPy arrays
mass = df["Mass_g"].to_numpy()
volume = df["Volume_cm3"].to_numpy()

# Step 4: Use NumPy to calculate density
density = mass / volume

# Step 5: Add calculated data to the DataFrame
df["Density_g/cm3"] = density
df["Density_g/cm3"] = df["Density_g/cm3"].round(1)

# Step 6: Print the updated DataFrame
print("\nDataFrame with Calculated Values:")
print(df)
```

Terminal Output:

    Original Data:
      Sample  Mass_g  Volume_cm3
    0      A     5.4           2
    1      B     9.0           2
    2      C    23.5           3
    3      D    25.8           3
    4      E    44.8           5
    5      F    62.4           8

    DataFrame with Calculated Values:
      Sample  Mass_g  Volume_cm3  Density_g/cm3
    0      A     5.4           2            2.7
    1      B     9.0           2            4.5
    2      C    23.5           3            7.8
    3      D    25.8           3            8.6
    4      E    44.8           5            9.0
    5      F    62.4           8            7.8