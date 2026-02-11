### Q1.5 Program Design and Evaluation

Imagine you are designing a program that:
- Takes user input
- Uses random numbers
- Performs calculations
- Outputs formatted results

(a) Identify three potential errors that beginner programmers might make.

1. Forgetting to convert user input into a number before doing calculations
2. Using variables before they are defined or misspelling variable names
3. Writing incorrect formulas or using the wrong operators in calculations

(b) For each error:
- Name the error type
- Explain how it could be prevented by using good programming practices.

#### 1. TypeError or ValueError

        Explanation:
        
        The input() function always returns a string. If a student tries to perform math with that string (for example, adding a number to it), Python will raise a TypeError. If they try to convert text that isn’t numeric into an integer or float, Python will raise a ValueError.

        Prevention:

        Always cast input using int() or float() before calculations

        Use try/except blocks to handle invalid input gracefully

        Prompt users clearly to enter numeric values

#### 2. NameError

        Explanation:
        
        This happens when a variable is used before it is created, or when the variable name is typed differently than it was originally defined.

        Prevention:

        Use consistent variable naming conventions

        Define variables before using them

        Run code in small sections and test frequently

#### 3. LogicError (not a built-in Python error, but a programming mistake)

        Explanation:
        
        The program runs without crashing, but produces incorrect results due to a wrong formula, incorrect operator (such as using / instead of //), or an off-by-one error when using random numbers or indexing.

        Prevention:

        Write out the formula in plain language before coding

        Test the program with known values to verify correct output

        Add print statements or use a debugger to trace intermediate values