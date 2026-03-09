"""
Course Number: ENGR 13100
Semester: Fall 2026

Description:
    Replace this line with a description of your program.

Assignment Information:
    Assignment:     7.1.2 pre_2
    Team ID:        LC0 - 00
    Author:         Holly Fortener, hforten@purdue.edu
    Date:           03/05/2026

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
    x = int(input("Enter an integer value for x: "))

    print(f"Start: x = {x}")
    for i in range(100):
        print(f"Pass {i+1}: x = {x}")

        t = 0
        while t < 2:
            x += 1
            print(f"Incremented x in while loop; Now x = {x}")
            t += 1

        if x < 18:
            x += 1
            print(f"Incremented x; Now x = {x}")
        else:
            break

    print(f"Number of iterations: {i+1}")

if __name__ == "__main__":
    main()