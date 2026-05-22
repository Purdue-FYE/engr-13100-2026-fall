"""
Course Number: ENGR 13100
Semester: Fall 2026

Description:
    Replace this line with a description of your program.

Assignment Information:
    Assignment:     6.2.1 ind_1
    Team ID:        LC0 - 00
    Author:         Holly Fortener, hforten@purdue.edu
    Date:           02/18/2026

Contributors:
    Name, login@purdue [repeat for each]

    My contributor(s) helped me:
    [ ] understand the assignment expectations without
        telling me how they will approach it.
    [ ] understand different ways to think about a solution
        without helping me plan my solution.
    [ ] think through the meaning of a specific error or
        bug present in my code without looking at my code.
    Note that if you helped somebody else with their code, you
    have to list that person as a contributor here as well.

Academic Integrity Statement:
    I have not used source code obtained from any unauthorized
    source, either modified or unmodified; nor have I provided
    another student access to my code.  The project I am
    submitting is my own original work.
"""

def main():
    print("Irrigation Advisor")

    # --- Validate soil input ---
    soil = input("Soil moisture (%) [0–60]: ")
    if soil.strip() >= "0" and soil.strip() <= "60":
        soil = float(soil)
    else:
        print("Warning: Soil moisture seems out of expected range.")
        return

    # --- Validate rain input ---
    rain = input("Rain forecast (mm) [0–50]: ")
    if rain.strip() >= "0" and rain.strip() <= "50":
        rain = float(rain)
    else:
        print("Warning: Rain forecast seems out of expected range.")
        return

    # --- Validate maintenance input ---
    maintenance_needed = input("Maintenance required? (yes/no): ")
    maintenance_needed = str(maintenance_needed).strip().lower()
    if maintenance_needed == "yes":
        maintenance_needed = "yes"
    elif maintenance_needed == "no":
        maintenance_needed = "no"
    else:
        print("Warning: expected 'yes' or 'no'. Using 'no'.")
        maintenance_needed = "no"

    # --- Validate low_pressure input ---
    low_pressure = input("Low pressure detected? (yes/no): ")
    low_pressure = str(low_pressure).strip().lower()
    if low_pressure == "yes":
        low_pressure = "yes"
    elif low_pressure == "no":
        low_pressure = "no"
    else:
        print("Warning: expected 'yes' or 'no'. Using 'no'.")
        low_pressure = "no"

    # --- Decision Logic (single if-elif-else chain) ---
    # Order matters: maintenance → pressure → rain → soil bands
    if maintenance_needed == "yes":
        action = "DO NOT IRRIGATE"
        reason = "Maintenance required."
    elif low_pressure == "yes":
        action = "DO NOT IRRIGATE"
        reason = "Low pressure condition."
    elif rain >= 10:
        action = "DELAY"
        reason = f"Significant rain expected ({rain} mm)."
    elif soil < 20:
        action = "RUN FULL"
        reason = f"Dry soil ({soil}%) and low rain forecast."
    elif 20 <= soil < 25:
        action = "RUN REDUCED"
        reason = "Borderline moisture."
    else:
        action = "SKIP"
        reason = f"Soil moisture is adequate ({soil}%)."

    # --- Output ---
    print("\n--- Recommendation ---")
    print(f"Action: {action}")
    print(f"Reason: {reason}")
    print("----------------------")


if __name__ == "__main__":
    main()
