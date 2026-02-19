## Py2.1 Solutions

### Inefficiencies in the given code
High-level theme: The code violates DRY (“Don’t Repeat Yourself”) and redoes work/patterns that should be abstracted.

#### See items blow for grading:
1. Repeated imports
    - import math appears in every part.
    - Fix: Import once at the top.

2. Redundant constants
    - pi_local = 3.1415926535 is defined multiple times and is unnecessary because math.pi exists.
    - Fix: Use math.pi once (no local pi_local).

3. Unused variable
    - g = 9.80665 is defined repeatedly but not used (mass does not require gravity).
    - Fix: Remove it entirely.

4. Copy–paste density lookup
    - The if/elif density blocks are repeated for each material (material1, material2, …).
    - Fix: Use a dictionary (e.g., DENSITY = {"aluminum": 2700.0, ...}) and a single lookup with a default.

5. Repetitive structure for each part
    - Each part duplicates: choose density → compute volume → compute mass → classify → print.
    - Fix: Extract functions (volume_block, volume_cylinder, classify_mass) and loop over a list of parts.

6. Magic numbers scattered
    - Dimensions and thresholds appear inline without central definition.
    - Fix: Keep part parameters in data structures; keep classification thresholds in one place or a function.

7. Overly granular, numbered variable names
    - L1, W1, H1, rho1, m1, note1 etc. hamper reuse and maintainability.
    - Fix: Use structured data (dicts/tuples) and loop variables.

8. Local “pi” vs standard library
    - Using a hand‑typed PI risks typos and inconsistency; math.pi is precise and conventional.

9. (If using the literal text) HTML entity &lt; in comparisons
    - In plain Python source, &lt; is invalid—it should be <. If this appears as-is in a Python file, it’s an error (not an “inefficiency,” but a correctness issue). In a rendered environment (e.g., LMS/HTML), it may just be display-escaped.

## Example of Efficient Code

```python
import math

# Centralized density table (kg/m^3) with a safe default
DENSITY = {
    "aluminum": 2700.0,
    "steel": 7850.0,
    "wood": 600.0,
}
DEFAULT_DENSITY = 1000.0  # fallback if material unknown

def density_of(material: str) -> float:
    return DENSITY.get(material.lower(), DEFAULT_DENSITY)

def volume_block(L: float, W: float, H: float) -> float:
    """Volume of a rectangular block [m^3]."""
    return L * W * H

def volume_cylinder(D: float, H: float) -> float:
    """Volume of a right circular cylinder [m^3]."""
    r = D / 2.0
    return math.pi * (r ** 2) * H

def classify_mass(m: float) -> str:
    """Simple mass classification text."""
    if m < 1:
        return "Very light."
    elif m < 10:
        return "Moderate mass."
    else:
        return "Heavy—handle with care."

# Describe all parts in one place
# Each item: (name, shape, material, dimensions...)
# For blocks: ("block", L, W, H)
# For cylinders: ("cylinder", D, H)
parts = [
    ("Part 1", "block",    "aluminum", (0.20, 0.10, 0.02)),
    ("Part 2", "block",    "steel",    (0.15, 0.08, 0.03)),
    ("Part 3", "cylinder", "wood",     (0.10, 0.30)),
    ("Part 4", "cylinder", "aluminum", (0.05, 0.25)),
]

total_mass = 0.0
for label, shape, material, dims in parts:
    rho = density_of(material)
    if shape == "block":
        L, W, H = dims
        V = volume_block(L, W, H)
    elif shape == "cylinder":
        D, H = dims
        V = volume_cylinder(D, H)
    else:
        raise ValueError(f"Unknown shape: {shape}")

    m = rho * V
    total_mass += m
    note = classify_mass(m)
    print(f"{label} mass: {m:.3f} kg — {note}")

print(f"\nTotal mass: {total_mass:.3f} kg")