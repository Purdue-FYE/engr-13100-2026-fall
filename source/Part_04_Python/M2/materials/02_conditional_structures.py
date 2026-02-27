"""
CONDITIONAL STRUCTURES (also known as selection structures or decision structures)

keywords : if, elif, else

1. Single alternative example:
Syntax:
    if condition:
        statement(s)
"""
# Write a program that prints a warning message if the temperature is greater
# than 30 degrees Celsius.
temperature = int(input("Enter the temperature: "))
if temperature > 30:
    print("It's hot outside")
print("End of program")

"""
2. Dual alternative example:
Syntax:
    if condition:
        statement(s)
    else:
        statement(s)
"""
# Write a program that prints a warning message if the temperature is greater
# than 30 degrees Celsius, otherwise print a message that it's a nice day.
temperature = int(input("Enter the temperature: "))
if temperature > 30:
    print("It's hot outside")
else:
    print("It's a nice day")
print("End of program")

"""
3. Multiple alternative example:
Syntax:
    if condition:
        statement(s)
    elif condition:
        statement(s)
    else:
        statement(s)
"""
# Write a program that prints a warning message if the temperature is greater
# than 30 degrees Celsius,  a message that it's a nice day if the temperature is
# between 20 and 30 degrees Celsius, and a message that it's cold outside if the
# temperature is less than 20 degrees Celsius.
temperature = int(input("Enter the temperature: "))
if temperature > 30:
    print("It's hot outside")
elif temperature >= 20 and temperature <= 30:
    print("It's a nice day")
else:
    print("It's cold outside")
print("End of program")

"""
4. Nested example:
Syntax:
    if condition:
        statement(s)
        if condition:
            statement(s)
        else:
            statement(s)
    else:
        statement(s)
"""
# Write a program that prints a warning message if the temperature is greater
# than 30 degrees Celsius and the humidity is greater than 50%, otherwise print
# a message that it's a nice day.
temperature = int(input("Enter the temperature: "))
humidity = int(input("Enter the humidity: "))
if temperature > 30:
    if humidity > 50:
        print("It's hot and humid")
    else:
        print("It's hot but not humid")
else:
    print("It's a nice day")
print("End of program")
