"""
Course Number: ENGR 13300
Semester: Spring 2025

Description:
    Taking in an input, generating random number, and performing number operations on
    them.

Assignment Information:
    Assignment:     7.2.2 Py1 Team 2
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

import random
from fractions import Fraction as frac


def main():
    # Asks user for a random seed
    random.seed(int(input("Enter the seed: ")))

    # Generates four random numbers based on instructions and round them to 3 decimal places
    precision = {{" precision "}}
    num1 = round(random.uniform(0, 100), precision)
    num2 = round(random.uniform(10, 50), precision)
    num3 = round(random.uniform(20, 40), precision)
    num4 = round(random.uniform(100, 200), precision)

    # Prints the four random numbers
    print(f"First Random Number : {num1}")
    print(f"Second Random Number : {num2}")
    print(f"Third Random Number : {num3}")
    print(f"Fourth Random Number : {num4}")

    # Calculates the sum of the random numbers, rounds it, and prints sum to console
    sumdec = round(num1 + num2 + num3 + num4, precision)
    print(f"Sum from decimals: {num1} + {num2} + {num3} + {num4} = {sumdec}")

    # Converts decimal to fraction, limits denominator so denominator is small
    max_denominator = {{" max_denominator "}}
    frac1 = frac(num1).limit_denominator(max_denominator)
    frac2 = frac(num2).limit_denominator(max_denominator)
    frac3 = frac(num3).limit_denominator(max_denominator)
    frac4 = frac(num4).limit_denominator(max_denominator)
    sumfrac = (frac1 + frac2 + frac3 + frac4).limit_denominator(max_denominator)
    print(f"Sum from fractions: {frac1} + {frac2} + {frac3} + {frac4} = {sumfrac}")


if __name__ == "__main__":
    main()
