"""
DATA TYPES IN PYTHON You can use the type() function to get the data type of a
variable or a literal.

Basic Data Types in Python
    - Integer (int)     - whole numbers
    - Float (float)     - numbers with decimal points
    - String (str)      - sequence of characters
    - Boolean (bool)    - True or False
    - None (NoneType)   - represents the absence of a value

Sequence Data Types in Python
    - List - comma separated values enclosed in square brackets, [1, 2, 3], list()
    - Tuple - comma separated values enclosed in parentheses, (1, 2, 3), tuple()
    - Set - comma separated values enclosed in curly braces, {1, 2, 3}, set()
    - Dictionary - key-value pairs enclosed in curly braces, {"name": "John", "age": 20}, dict()
    - Range - range() returns a sequence of numbers
      Syntax: range(start, stop, step)
            - start - optional, an integer number specifying at which position to start. Default is 0
            - stop - required, an integer number specifying at which position to stop (not included)
            - step - optional, an integer number specifying the incrementation. Default is 1

Basic indexing and slicing
    - Indexing - accessing a single element of a sequence
    - Slicing - accessing multiple elements of a sequence
    - Indexing starts from 0
    - Negative indexing starts from -1 (last element)
    - Slicing syntax: [start:stop:step]
        - start - starting index
        - stop - stopping index
        - step - incrementation
        - Default values: start=0, stop=len(sequence), step=1

    Sequence   : Mutability |   Order  |  Unique Elements  | Editablity
    List       :   Mutable  |  Ordered | allows duplicates | replaced or changed or added or removed
    Tuple      : Immutable  |  Ordered | allows duplicates | cannot be replaced or changed or added or removed
    Set        :   Mutable  | Unordered|   no duplicates   | cannot be replaced or changed, only added or removed
    Dictionary :   Mutable  | Unordered| no duplicate keys | only values can be replaced or changed or added or removed

Mixed Type Operations
    - Adding two integers results in an integer
    - Adding an integer and a float results in a float
    - Adding a string and a number results in an error
    - Adding two strings concatenates them and results in a string
    - Multiplying a string by an integer repeats the string and results in a
      string
    - Division (/) always results in a float
    - Floor division (//) always results in an integer
    - Modulus (%) always results in an integer

Data Type Conversion
    - int() - converts a value to an integer
    - float() - converts a value to a float
    - str() - converts a value to a string
    - bool() - converts a value to a boolean
    - list() - converts a value to a list
    - tuple() - converts a value to a tuple
    - dict() - converts a value to a dictionary
    - set() - converts a value to a set

Strings
    Single quotes ('), double quotes ("), or triple quotes (''' or \""") can be used to define strings
    You can add backward-slash (\) before the quote to escape it.
"""
