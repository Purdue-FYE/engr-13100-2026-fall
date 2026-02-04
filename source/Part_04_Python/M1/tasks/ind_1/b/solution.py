"""
Course Number: ENGR XXXXX
Semester: Fall 2026

Description:
    This program simulates testing a new medical device prototype

Assignment Information:
    Assignment:     4.3.1 Py1 Ind 1
    Team ID:        LC0 - 00
    Author:         Holly Fortener, hforten@purdue.edu
    Date:           01/23/2026

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


# ----------------------------------------
# PY01 – Medical Device Prototype Testing
# Instructor Reference Solution
# ----------------------------------------

# Imports
import random
import math
from datetime import datetime

def main():

    # ----------------------------------------
    # Part 1 – User Input
    # ----------------------------------------

    device_name = input("Enter medical device name: ").strip()
    prototype_id = int(input("Enter prototype ID number: "))

    researcher_last = input("Enter researcher's last name: ").strip().title()
    researcher_title = input("Enter researcher's title: ").strip().title()

    # Demonstrate split (sequence data type)
    title_parts = researcher_title.split()

    # ----------------------------------------
    # Part 2 – Professional Header
    # ----------------------------------------

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\n" + "=" * 50)
    print("MEDICAL DEVICE PROTOTYPE TEST REPORT")
    print("=" * 50)
    print(f"Device Name     : {device_name}")
    print(f"Prototype ID    : {prototype_id}")
    print(f"Researcher     : {researcher_title} {researcher_last}")
    print(f"Test Timestamp : {timestamp}")
    print("=" * 50)

    # ----------------------------------------
    # Part 3 – Simulated Test Data
    # ----------------------------------------

    # Generate random test values (no loops allowed)
    test_values = [
        random.randint(50, 100),
        random.randint(50, 100),
        random.randint(50, 100),
        random.randint(50, 100),
        random.randint(50, 100)
    ]

    print("\nTest Values:", test_values)
    print("First Test Value:", test_values[0])
    print("Test Value Slice (3 values):", test_values[1:4])

    # ----------------------------------------
    # Part 4 – Mathematical Analysis
    # ----------------------------------------

    average = sum(test_values) / len(test_values)
    sqrt_average = math.sqrt(average)

    print(f"\nAverage Test Value: {average:.2f}")
    print(f"Square Root of Average: {sqrt_average:.2f}")

    # ----------------------------------------
    # Part 5 – Pass/Fail Logic (No if, No loops)
    # ----------------------------------------

    passing_threshold = 75
    status_options = ["FAIL", "PASS"]

    passed = average >= passing_threshold
    result = status_options[passed]

    print(f"Passing Threshold: {passing_threshold}")
    print("Final Device Status:", result)

    # ----------------------------------------
    # Part 6 – String Processing
    # ----------------------------------------

    print("\nFormatted Researcher Tag:", (researcher_last + "_") * 2)
    print("Split Researcher Title Sequence:", title_parts)


if __name__ == "__main__":
    main()