"""
Course Number: ENGR 13100
Semester: Fall 2026

Description:
    Replace this line with a description of your program.

Assignment Information:
    Assignment:     6.1.2 PY2 PCA 6B
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

def calc_power(V, R):
    P = V**2 / R
    return P

def main():
    V = float(input("Enter voltage (V): "))
    R = float(input("Enter resistance (Ω): "))

    P = calc_power(V, R)
    print(f"Calculated power: {P:.2f} W")

if __name__ == "__main__":
    main()