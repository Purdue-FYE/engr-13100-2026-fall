"""
Course Number: ENGR 13100
Semester: Fall 2026

Description:
    Replace this line with a description of your program.

Assignment Information:
    Assignment:     7.2.1 ind_1
    Team ID:        LC0 - 00
    Author:         Holly Fortener, hforten@purdue.edu
    Date:           04/08/2026

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

    user_input = input("Enter items separated by commas (no spaces): ")
    items = user_input.split(",")

    error_count = 0
    for item in items:
        if item == "normal":
            print("Moving item to standard bin")
        elif item == "fragile":
            print("Handling fragile item with care")
        elif item == "heavy":
            print("Activating lift assist for heavy item")
        elif item == "error":
            print("ALERT: Item error detected – robot needs help!")
            error_count += 1
            if error_count == 3:
                print("ALERT: Too many errors – sending robot to inspection")
                break
        else:
            print("Sending item to inspection")

if __name__ == "__main__":
    main()