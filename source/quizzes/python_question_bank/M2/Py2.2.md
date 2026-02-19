## Py2.2

Draw a flowchart for the following Python code. Remember to use the flowchart shapes recommend for this course.

```python
import random
import math

def classify_average(avg):
    # >= 90: Excellent, >= 75: Good, >= 60: Pass, else Fail
    if avg >= 90:
        return "Excellent"
    elif avg >= 75:
        return "Good"
    elif avg >= 60:
        return "Pass"
    else:
        return "Fail"

print("Enter integer scores 0–100. Type 'done' to finish.")

total = 0
count = 0
low_score_found = False

raw = input("Score (or 'done'): ").strip()
while raw != "done":
    # Simple integer check (digits only; no +/-)
    if raw.isdigit():
        val = int(raw)
        if 0 <= val <= 100:
            total = total + val
            count = count + 1
            if val < 50:
                low_score_found = True
        else:
            print("Out of range (0–100).")
    else:
        print("Invalid input. Enter digits or 'done'.")
    raw = input("Score (or 'done'): ").strip()

if count == 0:
    print("No scores entered.")
else:
    avg = total / count

    # Random curve: small swing and extra credit
    curve = random.randint(-2, 2)           # -2..2
    extra = random.choice([0, 2, 5])        # bonus points
    curved = avg + curve + extra

    # Clamp to [0, 100] using simple decisions
    if curved < 0:
        curved = 0
    if curved > 100:
        curved = 100

    final_score = math.ceil(curved)         # round up
    category = classify_average(final_score)

    print("Count:", count)
    print("Raw average:", round(avg, 2))
    print("Final (after curve, ceil):", final_score)
    print("Category:", category)

    if low_score_found and category != "Excellent":
        print("Flag: Review recommended (low score present).")