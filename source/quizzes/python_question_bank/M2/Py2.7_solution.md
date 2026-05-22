## Py2.7

Use the Python code to fill in the blanks in the flowchart.

[See flowchart with solution in Python M2 quiz files - Py2.7_flowchart_solution.jpg]

# Editor - bernoulli_principle.py

```python
# Calculate pressure change in a pipe with two sections of different diameter
def calc_pressure(P1, rho, v1, v2, h1, h2):
    g = 9.81  # Acceleration due to gravity in m/s^2
    if h1 == h2:
        P2 = P1 + (0.5 * rho * (v1**2 - v2**2))
    else:
        P2 = P1 + (0.5 * rho * (v1**2 - v2**2)) + (rho * g * abs(h1 - h2))
    return P2

P1 = float(input("Enter the pressure at point 1 (P1) in Pascals: "))
rho = float(input("Enter the density of the fluid (rho) in kg/m^3: "))
v1 = float(input("Enter the velocity at point 1 (v1) in m/s: "))
v2 = float(input("Enter the velocity at point 2 (v2) in m/s: "))
h1 = float(input("Enter the height at point 1 (h1) in m: "))
h2 = float(input("Enter the height at point 2 (h2) in m: "))

P2 = calc_pressure(P1, rho, v1, v2, h1, h2)
print(f"The pressure at point 2 in the pipe (P2) is: {P2:.2f} Pascals")
```
