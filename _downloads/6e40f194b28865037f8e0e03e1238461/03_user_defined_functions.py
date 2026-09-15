"""
FUNCTIONS - resuable code blocks that perform a specific task.

Types of functions:
- Built-in functions - functions that are built into Python
- User-defined functions - functions defined by the user

Built-in functions - functions that are built into Python.
Examples: print(), range(), input() etc

User defined functions - functions defined by the user.
Syntax:
    def function_name(parameter1, parameter2, ...):
        statement(s)
        return value1, value2, ...
    function_name(argument1, argument2, ...)

    - def keyword is used to define a function
    - function name should be descriptive and meaningful
      (follows the same rules as variable names)
    - function call is required to execute the function
    - function can be called multiple times
    - function can be defined inside another function

Function Arguments and Parameters:
- Arguments are values passed to a function
- Parameters are variables used to define a function and are optional
- Arguments are assigned to parameters based on their position
- Arguments can be passed as positional arguments or keyword arguments
- Default parameters are used when no argument is passed

    Positional arguments:
    - Arguments passed to a function based on their position
    - Order of arguments is important
    - Number of arguments should match the number of parameters

    Keyword arguments:
    - Arguments passed to a function based on their name
    - Order of arguments is not important
    - Number of arguments should match the number of parameters

    Note:
    - All positional arguments must be placed before keyword arguments
    - The argument variable name and the parameter variable name do
      not have to match, just the positional order matters

    Default parameters:
    - Default parameters are used when no argument is passed
    - Default parameters should be at the end

Return statement:
- return statement is used to return a value from a function
- return statement is optional
- return statement can return multiple values
- return statement can be used to exit a function
- no other statement is executed after the return statement

Benefits of using functions:
- Code reusability
- Modularity
- Easy debugging and maintenance
- Better readability, organization, and efficiency

Scope:
- Scope is the region of the program where a variable is recognized
- Scope determines the visibility of a variable
- Scope can be local or global
    - Local scope - variables declared inside a function are local variables
    - Global scope - variables declared outside a function are global variables

Function recursion: (not covered in this course)
- Recursion is a technique in which a function calls itself
- Base case is required to prevent infinite recursion
- Recursion is used to solve complex problems and simplify code
"""
# Write a function that calculates how long an object will take to fall to the
# ground from a certain height.
# The formula to calculate the time taken for an object to fall is:
# time = sqrt(2 * height / g)
# where:  time - time taken for the object to fall
#       height - height from which the object is dropped
#            g - acceleration due to gravity (9.81 m/s^2)

# import math

# g = 9.81


# def calculate_time(height):  # parameter
#     time = math.sqrt(2 * height / g)
#     return time


# def main():
#     time = calculate_time(10)  # argument
#     print(f"The object will take {time:.2f} seconds to fall to the ground")


# if __name__ == "__main__":
#     main()

# Write a function that calculates how long an object will take to fall to the
# ground from a certain height with a given initial speed.
# The formula to calculate the time taken for an object to fall is:
# time = -speed +- sqrt(speed^2 - 4 * (g/2) * height) / g
# where:
#       time - time taken for the object to fall
#       height - height from which the object is dropped
#       speed - initial speed of the object
#       g - acceleration due to gravity (9.81 m/s^2)


# def calculate_time(height, speed, g):  # multiple parameters
#     if g > 0:
#         g = -g

#     time1 = -speed + math.sqrt(speed**2 - 4 * (g / 2) * height) / g
#     time2 = -speed - math.sqrt(speed**2 - 4 * (g / 2) * height) / g

#     if time1 > 0:
#         time = time1
#     elif time2 > 0:
#         time = time2
#     else:
#         time = time1
#     return time


# def main():
#     time = calculate_time(10, 0, 9.81)  # multiple arguments
#     print(f"The object will take {time:.2f} seconds to fall to the ground")


# if __name__ == "__main__":
#     main()  # call the main function
