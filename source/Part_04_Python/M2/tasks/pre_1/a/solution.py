"""
Course Number: ENGR 13100
Semester: Fall 2026

Description:
    Replace this line with a description of your program.

Assignment Information:
    Assignment:     6.1.1 PY2 PCA 6A
    Team ID:        LC0 - 00
    Author:         Holly Fortener, hforten@purdue.edu
    Date:           02/18/2026

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

def main():
    A = int(input("Enter an integer value for A: "))

    if A < -22 or A > 324:
        A = A - 16
        print(f"A = {A}")
    elif A > 102 and A < 157:
        A = A * (-5)
        print(f"A = {A}")
    elif A >= 241:
        A = A - 98
        print(f"A = {A}")
    elif A >= 51 and A <= 87:
        A = A - 37
        print(f"A = {A}")
    else:
        print("A is invalid")

if __name__ == "__main__":
    main()