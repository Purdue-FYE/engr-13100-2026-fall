"""
IMPORT MATH
    - Python has a built-in module called math that contains a collection of
      mathematical functions
    - To use the math module, you must import it using the import keyword
    - The math module provides functions for performing mathematical operations
    - To access functions in the math module, you must use the module name
      followed by a period and then the function name
    - For example,
        - to find the square root of a number, you can use the math.sqrt()
          function
        - to find the ceiling of a number, you can use the math.ceil() function
        - to find the floor of a number, you can use the math.floor() function
        - to find the factorial of a number, you can use the math.factorial()
          function
"""

# import the math module
import math

# math module functions - sqrt(), ceil(), floor(), factorial()
print(math.sqrt(16))  # Output: 4.0
print(math.ceil(4.2))  # Output: 5
print(math.floor(4.8))  # Output: 4
print(math.factorial(5))  # Output: 120

# Trignometric functions - sin, cos, tan
print(math.sin(math.pi / 2))  # Output: 1.0
print(math.cos(0))  # Output: 1.0
print(math.tan(math.pi / 4))  # Output: 0.9999999999999999

# Inverse Trignometric functions - asin, acos, atan
print(math.asin(1))  # Output: 1.5707963267948966 which is pi/2
print(math.acos(1))  # Output: 0.0
print(math.atan(0.5))  # Output: 0.4636476090008061 which is pi/6

# Exponential function
print(math.exp(1))  # Output: 2.718281828459045 (which is e^1)

# Logarithmic function
print(math.log(10))  # Output: 2.302585092994046 (which is ln(10)) - Natural logarithm
print(math.log10(100))  # Output: 2.0 (which is log base 10 of 100) - Base 10 logarithm
print(math.log2(8))  # Output: 3.0 (which is log base 2 of 8) - Base 2 logarith

# Power function - math.pow() and **
print(math.pow(2, 3))  # Output: 8.0 (which is 2^3)
