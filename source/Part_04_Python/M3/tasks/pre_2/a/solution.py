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

    v = float(input("Enter initial velocity in m/s: "))
    a = -9.8              # acceleration due to gravity (m/s^2)
    time_steps = 5        # seconds

    for t in range(1, time_steps + 1):
        x = v * t + 0.5 * a * t**2
        if x <= 0:
            print(f"At t = {t} s, the ball has hit the ground.")
            break
        elif x > 25:
            print(f"At t = {t} s, projectile height is: {x:.2f} m")
            print("I've lost the ball in the sun!")
            break
        else:
            print(f"At t = {t} s, projectile height is: {x:.2f} m")

if __name__ == "__main__":
    main()
