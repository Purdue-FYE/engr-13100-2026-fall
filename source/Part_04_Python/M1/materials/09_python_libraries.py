"""
PYTHON LIBRARIES AND MODULES

Python libraries are collections of functions and methods that allow you to perform many actions without writing your code.

Python modules are files that contain Python code. They can define functions, classes, and variables.

Python has a vast collection of libraries and modules that can be used to
perform various tasks. Some of the commonly used libraries are:
    - math - provides mathematical functions
    - numpy - provides support for large, multi-dimensional arrays and matrices
    - matplotlib - provides plotting functions
    - pandas - provides data structures and data analysis tools
    - cv2 - provides computer vision functions
    - scipy - provides scientific computing functions

Installing a library:
    - To install a library, you can use the pip command (Python package manager)
    - For example, to install the numpy library, you can use the following command in the terminal:
        python3 -m pip install numpy
    - To install pip, you can use the following command in the terminal:
        python3 -m pip --version # Check if pip is installed
        python3 -m ensurepip --user # Install pip
        python3 -m pip install --upgrade pip # Upgrade pip


# import the math module
import math

print(math.sqrt(16))  # Output: 4.0

# import the numpy module
import numpy as np

# Create a simple array
arr = np.array([1, 2, 3, 4, 5])

# Multiply each element by 2
result = arr * 2

# Print the result
print(result)  # Output: [ 2  4  6  8 10]

# import the matplotlib module
import matplotlib.pyplot as plt

# Create a simple plot
x = [1, 2, 3, 4, 5]
y = [1, 4, 9, 16, 25]

plt.plot(x, y)
plt.title("Simple Plot")
plt.xlabel("x-axis")
plt.ylabel("y-axis")
plt.show()

# import the pandas module
import pandas as pd

# Create a simple DataFrame
data = {
    "Name": ["John", "Anna", "Peter", "Linda"],
    "Age": [25, 36, 29, 42],
    "City": ["New York", "Paris", "Berlin", "London"],
}

df = pd.DataFrame(data)

# Display the DataFrame
print(
    df
)  # Output:     Name  Age  City 0  John  25  New York 1  Anna  36  Paris 2  Peter  29  Berlin 3  Linda  42  London

# Accessing a specific column
ages = df["Age"]  # Access the 'Age' column
print(ages)  # Output: 0    25, 1    36, 2    29, 3    42, Name: Age, dtype: int64

"""
