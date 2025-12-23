"""
IMPORT METHODS -

There are several ways to import a module or a function from a module
    - You can import a module
    - You can import a module using an alias
    - You can import specific functions from a module
    - You can import specific functions from a module using an alias
    - You can import all functions from a module using the * operator


# import a module
import math

print(math.sqrt(25))  # Output: 5.0

# import a module using an alias
import math as m

print(20 * m.cos(m.pi))  # Output: -20.0 , (cos(pi) = -1)

# import specific functions from a module
from math import cos, pi

print(20 * cos(pi))  # Output: -20.0

# import specific functions from a module using an alias
from math import sqrt as s

print(s(25))  # Output: 5.0

# import all functions from a module using the * operator
from math import *

print(sqrt(25))  # Output: 5.0

"""
