"""
Course Number: ENGR 13100
Semester: Fall 2026

Description:
    Replace this line with a description of your program.

Assignment Information:
    Assignment:     5.1.1 Py1 PCA 5A
    Team ID:        LC0 - 00
    Author:         Holly Fortener, hforten@purdue.edu
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
    # 1–3. Generate random numbers and cast to float
    a = float(input("Enter a number between 1 and 10: "))
    b = float(input("Enter a number between 3 and 8: "))

    # 4. Calculate values
    sum_val = a + b
    diff_val = a - b
    prod_val = a * b
    quot_val = a / b
    power_val = a**b

    # 5. Square root of absolute values
    sqrt_a = math.sqrt(abs(a))
    sqrt_b = math.sqrt(abs(b))

    # 6–7. Display formatted, labeled output
    print("\n--- Math Report ---")
    print(f"Number 1: {a:.2f}")
    print(f"Number 2: {b:.2f}")
    print(f"Sum: {sum_val:.2f}")
    print(f"Difference: {diff_val:.2f}")
    print(f"Product: {prod_val:.2f}")
    print(f"Quotient: {quot_val:.2f}")
    print(f"Power: {power_val:.2f}")
    print(f"Sqrt(|Number 1|): {sqrt_a:.2f}")
    print(f"Sqrt(|Number 2|): {sqrt_b:.2f}")


if __name__ == "__main__":
    main()
