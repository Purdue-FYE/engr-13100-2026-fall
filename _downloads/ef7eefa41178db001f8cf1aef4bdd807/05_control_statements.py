"""
Loop control statements: These statements change the execution from its
   normal sequence.
    - break: Terminates the loop statement and transfers execution to the
      statement immediately following the loop.
    - continue: Causes the loop to skip the remainder of its body and
      immediately retest its condition prior to reiterating.
    - pass: Does nothing.
"""
# break statement
# Write a program that prints the numbers from 1 to 5 using a while loop.
# count = 1
# while count <= 5:
#     print(count)
#     if count == 3:
#         break
#     count += 1

# continue statement
# Write a program that prints the numbers from 1 to 5 using a while loop.
# count = 0
# while count < 5:
#     count += 1
#     if count == 3:
#         continue
#     print(count)

# Input validation using break statement
# Write a program that asks the user to enter a number between 1 and 5 using a break statement.
# while True:
#     number = int(input("Enter a number between 1 and 5: "))
#     if number >= 1 and number <= 5:
#         break
# print(f"You entered {number}")

# pass statement
# Write a program that prints the numbers from 1 to 5 using a while loop.
# count = 1
# while count <= 5:
#     pass
#     print(count)
#     count += 1
