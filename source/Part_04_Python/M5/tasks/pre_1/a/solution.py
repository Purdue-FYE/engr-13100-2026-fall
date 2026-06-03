"""
Course Number: ENGR 13100
Semester: Fall 2026

Description:
    Replace this line with a description of your program.

Assignment Information:
    Assignment:     6.2.1 ind_1
    Team ID:        LC0 - 00
    Author:         Holly Fortener, hforten@purdue.edu
    Date:           05/20/2026

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
"""

def main():

    # ========================================
    # Part 1: Import Required Libraries
    # ========================================

    import os
    import pandas as pd
    import matplotlib.pyplot as plt
    from sklearn.linear_model import LinearRegression


    # ========================================
    # Part 2: Load and Inspect Data
    # ========================================

    base_dir = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(base_dir, "radioactive_decay.csv"))

    # --- STUDENT CODE: Load CSV file --- #
    # df = pd.read_csv(".../radioactive_decay.csv")

    # Display required information
    print("--- Radioactive Decay Dataset ---")
    print()
    print(df.head(10))
    print()

    # ========================================
    # Part 3: Display Data on a Scatter Plot
    # ========================================

    plt.scatter(df["time_days"],
                df["remaining_fraction"],
                s=50,
                alpha=0.7)
    
    plt.xlabel("Time (days)", fontsize=12, labelpad=10)
    plt.ylabel("Remaining Fraction", fontsize=12, labelpad=10)
    plt.title("Radioactive Decay", fontsize=14, pad=15)
    plt.tick_params(axis='both', which='major', labelsize=11)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    plt.tight_layout()
    # plt.show()
    # plt.savefig(".../radioactive_decay_plot.png")
    # plt.close()

    # ========================================
    # Part 4: Compute Linear Regression
    # ========================================

    model = LinearRegression()
    model.fit(df[["time_days"]], df["remaining_fraction"])

    # ========================================
    # Part 5: Display Slope, Intercept, and Regression Equation
    # ========================================

    print("--- Linear Regression Coefficients ---")
    print()
    print(f"Slope: {model.coef_[0]:.3f}")
    print(f"Intercept: {model.intercept_:.3f}")
    print()

    # ========================================
    # Part 6: Generate Predicted y-values
    # ========================================

    predicted_y = model.predict(df[["time_days"]])

    # ========================================
    # Part 7: Plot Data and Regression Line on Same Plot
    # ========================================

    plt.scatter(df["time_days"],
                df["remaining_fraction"],
                s=50,
                alpha=0.7,
                label="Radioactive Decay Data")

    plt.plot(df["time_days"],
             predicted_y,
             color="red",
             linewidth=2,
             label="Regression: y = {:.3f}x + {:.3f}".format(model.coef_[0], model.intercept_))

    plt.xlabel("Time (days)", fontsize=12, labelpad=10)
    plt.ylabel("Remaining Fraction", fontsize=12, labelpad=10)
    plt.title("Radioactive Decay", fontsize=14, pad=15)
    plt.tick_params(axis='both', which='major', labelsize=11)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend(fontsize=11)

    plt.tight_layout()
    # plt.show()
    # plt.savefig(".../radioactive_decay_regression_plot.png")
    # plt.close()

if __name__ == "__main__":
    main()