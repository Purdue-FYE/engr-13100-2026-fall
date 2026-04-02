"""
Nested loop: A loop inside another loop.
Syntax:
    for element in sequence:
        statement(s)
        while condition:
            statement(s)
    statement(s)

"""
# # Nested loop
# # Write a program to print the multiplication table of 2 using a nested loop.
# for i in range(2, 3): # also range(2, 3) = [2]
#     for j in range(1, 11):
#         print(f"{i} * {j} = {j * i}")
#     print() # print a new line after each iteration of the outer loop

# # Write a program to print the multiplication table of 2 using a nested loop.
# i = 2
# while i <= 2: # Outer loop equivalent to range(2, 3)
#     j = 1
#     while j <= 10:  # Inner loop equivalent to range(1, 11)
#         print(f"{i} * {j} = {j * i}")
#         j += 1
#     i += 1

# # Write a program to print the multiplication table of 2 using a nested loop.
# i = 2
# while i <= 2: # Outer loop equivalent to range(2, 3)
#     for j in range(1, 11):  # Inner loop equivalent to range(1, 11)
#         print(f"{i} * {j} = {j * i}")
#     i += 1

# # Write a program to print the multiplication table of 2 using a nested loop.
# for i in range(2, 3): # also range(2, 3) = [2]
#     j = 1
#     while j <= 10:
#         print(f"{i} * {j} = {j * i}")
#         j += 1
#     print() # print a new line after each iteration of the outer loop

# # While vs for loop
# # Write a program that prints the numbers from 1 to 5 using a while loop.
# count = 1
# while count <= 5:
#     print(count) # Output: 1 2 3 4 5
#     count += 1.

# for count in range(1, 6): # range(1, 6) = [1, 2, 3, 4, 5]
#     print(count) # Output: 1 2 3 4
