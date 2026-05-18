## Py2.8

Use the Python code to fill in the blanks in the:

(a) Terminal (sample input/output)
(b) Flowchart

### Editor - number_score.py

```python
# Calculate number score
num1 = int(input("Enter the first number (1-50): "))
num2 = int(input("Enter the second number (1-50): "))
num3 = int(input("Enter the third number (1-50): "))
num4 = int(input("Enter the fourth number (1-50): "))

print(f"You entered: {num1}, {num2}, {num3}, {num4}")

lucky_nums = {3, 6, 7, 8, 9}
unlucky_nums = {4, 13, 17}

if num1 in lucky_nums or num3 in lucky_nums:
    print("You entered a lucky number!")
    bonus = 15
    score = num1 + num3 + bonus
elif num2 in unlucky_nums or num4 in unlucky_nums:
    print("You entered an unlucky number!")
    penalty = -5
    if num2 == 13 or num4 == 13:
        print("You entered the unluckiest number!")
        penalty = -10
    score = num2 + num4 + penalty
else:
    print("Your numbers are mid. Low score.")
    score = 5

print(f"Your score is: {score}")
```

### Terminal (a)

    # Sample input/ouput 1
    $ python checkout.py
    Enter the first number (1-50): 7
    Enter the second number (1-50): ___
    Enter the third number (1-50): 12
    Enter the fourth number (1-50): 40
    You entered: 7, 22, 12, 40
    _________________________________
    Your score is: 34

    # Sample input/ouput 2
    $ python checkout.py
    Enter the first number (1-50): 2
    Enter the second number (1-50): 4
    Enter the third number (1-50): 11
    Enter the fourth number (1-50): 20
    _________________________________
    You entered an ___________ number!
    Your score is: -1

    # Sample input/ouput 3
    $ python checkout.py
    Enter the first number (1-50): 1
    Enter the second number (1-50): 13
    Enter the third number (1-50): 9
    Enter the fourth number (1-50): ___
    You entered: 1, 13, 9, ___
    You entered an unlucky number!
    _________________________________
    Your score is: 11

    # Sample input/ouput 4
    $ python checkout.py
    Enter the first number (1-50): 1
    Enter the second number (1-50): 2
    Enter the third number (1-50): 10
    Enter the fourth number (1-50): 11
    You entered: 1, 2, 10, 11
    _________________________________
    Your score is: ___

### Flowchart (b)

[See flowchart with blanks in Python M2 quiz files - Py2.8_flowchart.jpg]
