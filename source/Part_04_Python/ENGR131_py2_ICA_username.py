## PY2 ICA: UDFs & Code Efficiency (06B)

"""
The following Python code estimates the mass of a few simple parts—rectangular blocks
and solid cylinders—made from basic materials (aluminum, steel, wood). It uses the idea
that mass = density * volume, where block volume = length * width * height and
cylinder volume = pi * radius^2 * height.

"""

# Calculate masses of simple parts (blocks and cylinders)

# Part 1: Aluminum block (0.20 m × 0.10 m × 0.02 m)

pi_local = 3.1415926535
g = 9.80665

material1 = "aluminum"
# Density lookup
if material1 == "aluminum":
    rho1 = 2700.0
elif material1 == "steel":
    rho1 = 7850.0
elif material1 == "wood":
    rho1 = 600.0
else:
    rho1 = 1000.0  # default

L1 = 0.20
W1 = 0.10
H1 = 0.02

# Calculate Volume of block
V1 = L1 * W1 * H1
m1 = rho1 * V1

# Mass classification
if m1 < 1:
    note1 = "Very light."
elif m1 < 10:
    note1 = "Moderate mass."
else:
    note1 = "Heavy—handle with care."

print(f"Part 1 mass: {m1:.3f} kg — {note1}")

# Part 2: Steel block (0.15 m × 0.08 m × 0.03 m)


pi_local = 3.141592653
g = 9.80665

material2 = "steel"
# Density lookup
if material2 == "aluminum":
    rho2 = 2700.0
elif material2 == "steel":
    rho2 = 7850.0
elif material2 == "wood":
    rho2 = 600.0
else:
    rho2 = 1000.0

L2 = 0.15
W2 = 0.08
H2 = 0.03

# Calculate Volume of block
V2 = L2 * W2 * H2
m2 = rho2 * V2

# Mass classification
if m2 < 1:
    note2 = "Very light."
elif m2 < 10:
    note2 = "Moderate mass."
else:
    note2 = "Heavy—handle with care."

print(f"Part 2 mass: {m2:.3f} kg — {note2}")

# Part 3: Wooden cylinder (diameter 0.10 m, height 0.30 m)


pi_local = 3.1415926535
g = 9.80665

material3 = "wood"
# Density lookup
if material3 == "aluminum":
    rho3 = 2700.0
elif material3 == "steel":
    rho3 = 7850.0
elif material3 == "wood":
    rho3 = 600.0
else:
    rho3 = 1000.0

D3 = 0.10
H3 = 0.30
r3 = D3 / 2.0

# Calculate volume of cylinder
V3 = pi_local * (r3**2) * H3
m3 = rho3 * V3

# Mass classification
if m3 < 1:
    note3 = "Very light."
elif m3 < 10:
    note3 = "Moderate mass."
else:
    note3 = "Heavy—handle with care."

print(f"Part 3 mass: {m3:.3f} kg — {note3}")

# Part 4: Aluminum cylinder (diameter 0.05 m, height 0.25 m)


pi_local = 3.1415926535
g = 9.80665

material4 = "aluminum"
# Density lookup
if material4 == "aluminum":
    rho4 = 2700.0
elif material4 == "steel":
    rho4 = 7850.0
elif material4 == "wood":
    rho4 = 600.0
else:
    rho4 = 1000.0

D4 = 0.05
H4 = 0.25
r4 = D4 / 2.0

# Calculate Volume of Cylinder
V4 = pi_local * (r4**2) * H4
m4 = rho4 * V4

# Mass Classification
if m4 < 1:
    note4 = "Very light."
elif m4 < 10:
    note4 = "Moderate mass."
else:
    note4 = "Heavy—handle with care."

print(f"Part 4 mass: {m4:.3f} kg — {note4}")

total_mass = m1 + m2 + m3 + m4
print(f"\nTotal mass: {total_mass:.3f} kg")
