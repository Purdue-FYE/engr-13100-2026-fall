## Py2.6

Use the flowchart to fill in 1 blank in the Python code.

[See flowchart in Python M2 quiz files - Py2.5_flowchart.jpg]

```python
# Calculate current (I) with voltage (V) and resistance (R) using Ohm's Law (V = I*R)
import __main__

def calc_current(voltage, resistance):
    current = voltage / resistance
    return current

def main():
    voltage = float(input("Enter voltage (Volts): "))
    resistance = float(input("Enter resistance (Ohms): "))
    ______________________________________________________
    print(f"The current in the circuit is {current:.2f} Amps.")

if __name__ == "__main__":
    main()
```