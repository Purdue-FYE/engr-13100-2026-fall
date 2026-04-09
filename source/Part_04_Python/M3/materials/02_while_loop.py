"""
While loop: A while loop is used to repeatedly execute a block of statements
   as long as the condition is true.
Syntax:
    while condition:
        statement(s)]

    Definte while loop:
    - initialize a control variable before enterting the loop
    - check the control variable and enter the loop if the condition is true
    - update the control variable inside the loop such that the condition will
      eventually become false
"""
# Write a program that prints the numbers from 1 to 5 using a while loop.
# count = 1
# while count <= 5:
#     print(count) # Output: 1 2 3 4 5
#     count += 1
"""
    Infinite while loop - a loop that never ends
    - occurs when the condition is always true or the condition is not updated
    - to stop an infinite loop, press Ctrl + C
"""
# Write a program that prints the numbers from 1 to 5 using a while loop.
# count = 1
# while count <= 5:
#     print(count)

"""
    Indefinite while loop - a loop that does not have a fixed number of iterations
    - the number of iterations is determined by the user input
    - the loop continues until a specific condition is met
"""
# Write a program that asks the user to enter yes or no to the question "would
# you like to run the program again?"
# The program should continue to run until the user enters no.
# response = input("Would you like to start the program? (yes/no): ")
# while response == 'yes':
#     # code block
#     print("The program is running.")
#     response = input("Would you like to run the program again? (yes/no): ")
"""
    Sentinel-controlled loop - a distinct value that signals the end of the loop
    - the sentinel value is used to stop the loop
    - the sentinel value should be distinct from other values in the sequence
    - example:
                0 or -1 to signal the end of the loop
                'q' or 'Q' or 'quit' to quit the program
                'done' to stop entering values
                EOF (end of file) to signal the end of the file
"""
# Write a program that asks the user to enter a number. The program should keep
# asking the user to enter a number until the user enters -1.
# number = int(input("Enter a number (-1 to stop): "))
# while number != -1:
#     # code block
#     number = int(input("Enter a number (-1 to stop): "))
# print("You entered -1. The program has stopped.")
