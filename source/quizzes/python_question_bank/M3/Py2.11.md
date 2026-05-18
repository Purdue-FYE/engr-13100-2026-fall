## Py2.11 Loop Outputs

You are simulating a tank cooling system. The code block adjusts the system temperature and flow rate until a safe condition is met. What are the final values of each variable after the code runs?

```python
temp = 60
flow = 10
limit = 50

while temp > limit or flow < 12:
    if temp > limit:
        temp = temp - 5
    else:
        flow = flow + 1

efficiency = temp / flow
```

    temp = __________________
    flow = __________________
    limit = ___________________
    efficiency = ___________________

Note: If efficiency is not an integer, you may leave your answer as a fraction.
