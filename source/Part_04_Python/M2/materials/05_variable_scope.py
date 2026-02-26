"""
VARIABLE SCOPE - scope of a variable is the region of the program where the variable is recognized
1. Local Scope - variables declared inside a function are local variables and can only be accessed inside that function
2. Global Scope - variables declared outside a function are global variables and can be accessed throughout the program

- Avoid using global variables as they can be modified from anywhere in the program and can lead to bugs
- Use local variables instead to avoid conflicts and bugs in the program
- Use the global keyword to modify a global variable inside a function
- Known constants are acceptable to use as global variables such as gravity (g = 9.81) in physics calculations.
"""
# # Example of a local variable
# def my_func():
#     x = 10
#     print(x)


# my_func()  # 10
# print(f"The value of x is {x}")  # NameError: name 'x' is not defined

# # Example of a global variable
# y = 20


# def my_func():
#     print(f"This is the value of y inside the function: {y}")


# my_func()  # 20
# print(f"This is the value of y outside the function: {y}")  # 20


# # Example of a global variable being modified inside a function
# z = 30


# def my_func():
#     global z  # global keyword is used to refer to the global variable
#     z = 40
#     print(f"This is the value of z inside the function: {z}")


# my_func()  # 40
# print(f"This is the value of z outside the function: {z}")  # 40

# # Example of a global variable being modified inside a function without using the global keyword
# w = 50


# def my_func():
#     w = 60
#     print(f"This is the value of w inside the function: {w}")


# my_func()  # 60
# print(f"This is the value of w outside the function: {w}")  # 50
# # The global variable w is not modified because the local variable w is a different variable
