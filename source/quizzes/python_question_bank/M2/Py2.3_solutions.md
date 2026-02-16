## Py2.3 Solutions

Use the Python code to fill in 3 blanks in the sample input/output:

### Editor - calculate_fare.py
```python
# Calculate train fare based on travel time
hours = float(input("Enter your travel time in hours: "))
if hours >= 6:
    fare = 12
    print(f"Total fare: ${fare:.2f}")
elif hours < 6:
    fare = 12 - (hours / 2)
    print(f"Total fare: ${fare:.2f}")
else:
    print("Did not recognize input.")
```

### Program Description

Prompt the user to enter the number of hours they plan to travel, then calculate their fare based on hours: to ride for 6 or more hours, train sfare is $12; to ride for 6 hours or less, train fare is $12 minus half the number of hours. For these two conditions, also display the total fare in dollars, formatting to match the examples below. Otherwise, display: "Did not recognize input."

### Terminal

    (a) $ python calculate_fare.py
        Enter distance: 4
        Total fare: $10.00

    (b) $ python calculate_fare.py
        Enter distance: 10
        Total fare: $12.00

    (c) $ python calculate_fare.py
        Enter distance: ten
        Did not recognize input.
