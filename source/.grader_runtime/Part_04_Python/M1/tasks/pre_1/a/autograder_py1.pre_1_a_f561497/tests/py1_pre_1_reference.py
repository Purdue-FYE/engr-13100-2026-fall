"""
Course Number: ENGR 13100
Semester: Fall 2026

Description:
    Replace this line with a description of your program.

Assignment Information:
    Assignment:     7.1.2 Py1 Pre 0
    Team ID:        LC0 - 00
    Author:         Name, login@purdue.edu
    Date:           08/29/2024

Contributors:
    Name, login@purdue [repeat for each]

    My contributor(s) helped me:
    [ ] understand the assignment expectations without
        telling me how they will approach it.
    [ ] understand different ways to think about a solution
        without helping me plan my solution.
    [ ] think through the meaning of a specific error or
        bug present in my code without looking at my code.
    Note that if you helped somebody else with their code, you
    have to list that person as a contributor here as well.

Academic Integrity Statement:
    I have not used source code obtained from any unauthorized
    source, either modified or unmodified; nor have I provided
    another student access to my code.  The project I am
    submitting is my own original work.
"""

import math


def main():
    a = 101
    b = 7
    c = 12.34

    x1 = c**2 - math.sin(b)**2
    print(f'equation 1: {x1:.3f}')

    x2 = math.factorial(b) * (math.cos(math.pi / c) - a)
    print(f'equation 2: {x2:.3f}')

    x3 = math.pow(c, math.pi * math.e) * math.asin(math.sqrt(3) / 2) / (a**math.e * b)
    print(f'equation 3: {x3:.3f}')


if __name__ == "__main__":
    main()