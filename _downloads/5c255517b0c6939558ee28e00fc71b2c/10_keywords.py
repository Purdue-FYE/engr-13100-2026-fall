"""
KEYWORDS IN PYTHON
    - Keywords are reserved words in Python that have special meaning and cannot be used as variable names.
    - Keywords are case-sensitive.
    - Python has 35 keywords.
    - You can get a list of keywords using the keyword module.
    - You can check if a word is a keyword using the iskeyword() function.
    - You can get a list of built-in functions and variables using the builtins
      module.
    - You can check if a word is a built-in function or variable using the dir()
      function.
    - You can check if a word is a built-in function or variable using the is
      identity operator.


# import the keyword module
import keyword

print(keyword.kwlist)  # List of reserved words
print(keyword.iskeyword("break"))  # Output: True

# import the builtins module
import builtins

print(dir(builtins))  # List of built-in functions and variables

print(ArithmeticError is builtins.ArithmeticError)  # Output: True

"""
