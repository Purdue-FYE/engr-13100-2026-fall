"""
===============================================================================
Course Number: ENGR 13300
Semester: # e.g. Fall 2024

Program Description
    Replace this line with a description of your program.

Assignment Information
    Assignment:     e.g. 5.2.1 Task 1 (for Python 1 Team task 1)
    Author:         Name, login@purdue.edu
    Team ID:        LC# - ## (e.g. LC1 - 01; for section LC1, team 01)

Contributor:    Name, login@purdue [repeat for each]

    My contributor(s) helped me:
    [ ] understand the assignment expectations without
        telling me how they will approach it.
    [ ] understand different ways to think about a solution
        without helping me plan my solution.
    [ ] think through the meaning of a specific error or
        bug present in my code without looking at my code.
    Note that if you helped somebody else with their code, you
    have to list that person as a contributor here as well.

ACADEMIC INTEGRITY STATEMENT
I have not used source code obtained from any other unauthorized
source, either modified or unmodified. Neither have I provided
access to my code to another. The project I am submitting
is my own original work.
===============================================================================
"""
"""
# The "strip()" function removes indicated
# characters from either side of a string
# If no characters are indicated, it simply
# strips any white spaces from either side
# of a string.

string = " haha laughing haha   "

# Leading and trailing whitespace are removed
print(string.strip())

# Indicated characters removed from both sides of string
print(string.strip(" ha"))

# Note that order doesn't matter
print(string.strip("ah "))

# Space in middle
print(string.strip("a h"))

# Without the 'a'
print(string.strip("h "))

# Note that characters blocked by other characters
# which are closer to the edges, but which aren't
# marked for stripping, are not successfully stripped
print(string.strip(" hl"))

# Argument doesn't contain space
# No characters are removed.
print(string.strip("ha"))

string = "Go Purdue!"
print(string.strip("Go"))


# Feel free to comment out the lines above before moving on


# The "split()" function breaks strings up
# based on the indicator provided within the
# parentheses

string = "Purdue University was established in 1869."

# If left empty, the string is split at white spaces
print(string.split())

string = "Five pairs of perfect parallel lines"

# Note how the indicator is removed from the
# resulting split string elements
print(string.split("p"))

string = "Hail, hail to old Purdue! All hail to our old gold and black! Hail, hail to old Purdue!"

# You can also use punctuation to split strings
print(string.split("!"))

# You can use combinations of characters
# But note that it is case sensitive
print(string.split("hail"))
"""
