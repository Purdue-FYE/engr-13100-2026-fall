### Q1.3 Debugging and Reasoning

A student writes the following code:

    import random

    numbers = [1, 2, 3, 4, 5]
    choice = random.randint(0, len(numbers))
    print(numbers[choice])

(a)	What error might occur when this code runs?

    Answer:
    An IndexError: list index out of range may occur.

(b)	Explain why the error happens.

    Answer:
    The function random.randint(a, b) returns a random integer including both endpoints a and b.

    len(numbers) is 5

    Valid list indices are 0 through 4

    If random.randint(0, len(numbers)) returns 5, the program will try to access numbers[5], which does not exist, causing an IndexError.

(c)	Provide two different ways to fix the code.

#### Fix 1: Adjust the upper bound of randint

Make sure the maximum value is the last valid index:

    choice = random.randint(0, len(numbers) - 1)

#### Fix 2: Use random.choice() instead of indexing

This avoids working with indices entirely:

    choice = random.choice(numbers)
    print(choice)