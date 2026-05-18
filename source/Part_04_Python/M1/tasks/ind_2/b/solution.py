"""
Course Number: ENGR 13300
Semester: Fall 2024

Description:
    This program calculates the series and parallel total resistance.

Assignment Information:
    Assignment:     7.3.2 Py1 Ind 2
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

    unit = '{{" unit "}}'  # unit string

    # Get a measurment value from the user.
    E1 = float(input(f'Input the {{" measurement "}} of the first {{" element "}} [{unit}]: '))
    E2 = {{" fixed_value_py "}}

    # Calculate the total measurement for series configuration.
    E_srs = {{" func_srs_py "}}

    # Calculate the total measurement for parallel configuration.
    E_prl = {{" func_prl_py "}}

    # Display the results in a table.
    print("Type           First      Second      Total")
    print(f"Series   {E1:8.1f} {unit} {E2:8.1f} {unit} {E_srs:8.1f} {unit}")
    print(f"Parallel {E1:8.1f} {unit} {E2:8.1f} {unit} {E_prl:8.1f} {unit}")


if __name__ == "__main__":
    main()
