"""
STRINGS -

Documentation: https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str

1. Strings as sequences of characters
A string is a sequence of characters. In Python, strings are immutable sequences of Unicode code points.

2. String literals
A string literal is a sequence of characters enclosed in single quotes ('...') or double quotes ("...").

3. String manipulation as an immutable sequence
For strings x and y with indices i, j and k, the following operations are supported:
    - Indexing        - x[i], x[-i]
    - Slicing         - x[i:j], x[i:j:k] # start, stop, step
    - Concatenation   - x + y
    - Repetition      - n * x, where n is an integer
    - Membership test - x in y, x not in y
    - Length          - len(x), min(x), max(x)
    - Iteration       - for i in x
    - Comparison      - x == y, x != y, x < y, x <= y, x > y, x >= y
    - Searching       - x.find(y), x.rfind(y), x.index(y), x.rindex(y)
    - Counting        - x.count(y)
    - Ordering        - sorted(x), reversed(x)

4. String methods
For strings x and y, the following methods are supported:
    - x.lower()      - lowers the case of all characters
    - x.upper()      - uppercases all characters
    - x.title()      - capitalizes the first character of each word
    - x.capitalize() - capitalizes the first character of the string
    - x.split()      - splits a string into a list of substrings
    - x.strip()      - removes leading and trailing whitespace (lstrip, rstrip)
    - x.replace()    - replaces a substring with another substring (old, new)
    - x.join()       - joins a list of substrings into a single string
    - x.startswith() - checks if a string starts with a specified prefix (prefix, start, end)
    - x.endswith()   - checks if a string ends with a specified suffix
    - x.isalpha()    - checks if all characters are alphabetic, returns Boolean
    - x.isdigit()    - checks if all characters are digits, returns Boolean
    - x.isalnum()    - checks if all characters are alphanumeric, returns Boolean
    - x.islower()    - checks if all characters are lowercase, returns Boolean
    - x.isupper()    - checks if all characters are uppercase, returns Boolean
    - x.isspace()    - checks if all characters are whitespace, returns Boolean

"""
"""
# Strings as sequences of characters
s = "Purdue"
for i in s:
    print(i)  # Output: P u r d u e

# ord() function - returns the Unicode code point of a character
o = []
for j in s:
    o = ord(j)
    print(o)  # Output: 80 117 114 100 117 101

# chr() function - returns the character that corresponds to a Unicode code point
for k in s:
    c = chr(ord(k))
    print(c)  # Output: P u r d u e

# String manipulation as an immutable sequence
s = "Hail Purdue!"
# Indexing
print(s[0])  # Output: H

# Slicing
print(s[0:4])  # Output: Hail
print(s[5:12])  # Output: Purdue

# Concatenation
s1 = "Hail"
s2 = "Purdue!"
print(s1 + " " + s2)  # Output: Hail Purdue!

# Repetition
print(s1 * 3)  # Output: HailHailHail

# Membership test
print("Hail" in s)  # Output: True
print("Hail" not in s)  # Output: False

# Length
print(len(s))  # Output: 12
print(min(s1))  # Output: H (Unicode code point 72)
print(max(s2))  # Output: u (Unicode code point 117)

# Iteration
for i in s:
    print(i)  # Output: H a i l   P u r d u e !

# Comparison
print(s1 == s2)  # Output: False
print(s1 != s2)  # Output: True

# Searching
print(s.find("Purdue"))  # Output: 5

# Counting
print(s.count("a"))  # Output: 1

# Ordering
print(sorted(s))  # Output: [' ', '!', 'H', 'P', 'a', 'd', 'e', 'i', 'l', 'r', 'u']

# String methods
s3 = "2024"
s4 = "    ENGR 133    "
print(s.lower())  # Output: hail purdue!
print(s.upper())  # Output: HAIL PURDUE!
print(s.title())  # Output: Hail Purdue!
print(s.capitalize())  # Output: Hail purdue!
print(s.split())  # Output: ['Hail', 'Purdue!']
print(s4.strip())  # Output: ENGR 133
print(s4.lstrip())  # Output: ENGR 133
print(s4.rstrip())  # Output:     ENGR 133
print(s.replace("Purdue", "Boilermakers"))  # Output: Hail Boilermakers!
print(" ".join(["Hail", "Purdue!"]))  # Output: Hail Purdue!
print(s.startswith("Hail"))  # Output: True
print(s.endswith("!"))  # Output: True
print(s1.isalpha())  # Output: True
print(s3.isdigit())  # Output: True
print(s2.isalnum())  # Output: True
print(s.islower())  # Output: False
print(s.isupper())  # Output: False
print(s.isspace())  # Output: False
"""
