### Q1.1 Understanding Python Errors

For each error type listed below:

(a) Define the error in your own words.

(b) Write a short Python code example (based on your program from Question 1) that would cause this error.

(c) Briefly explain why the error occurs in your example.

#### TypeError

    A TypeError happens when you try to perform an operation on a value of the wrong data type, such as adding a number to a string.

    user_input = "5"
    result = user_input + 2
    print(result)
    
    The variable user_input is a string, and 2 is an integer. Python does not know how to add a string and a number together, so it raises a TypeError.

#### IndexError

    An IndexError occurs when you try to access a position in a list or string that does not exist.

    numbers = [10, 20, 30]
    print(numbers[3])

    This list has valid indices 0, 1, and 2. Index 3 is out of range, so Python raises an IndexError.

#### ValueError

    A ValueError happens when a function receives a value of the correct type but an invalid value.

    user_input = "hello"
    number = int(user_input)
    print(number)

    The string "hello" cannot be converted into an integer. Even though int() expects a string, the value is not a valid number, so Python raises a ValueError.

#### NameError

    A NameError occurs when you try to use a variable or function name that has not been defined.

    total = 10
    print(totall)

    The variable totall is misspelled and was never defined. Python cannot find a variable with that name, so it raises a NameError.

