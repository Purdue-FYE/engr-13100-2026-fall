"""
Course Number: ENGR 13100
Semester: Fall 2026

Description:
    Replace this line with a description of your program.

Assignment Information:
    Assignment:     6.2.1 ind_1
    Team ID:        LC0 - 00
    Author:         Holly Fortener, hforten@purdue.edu
    Date:           05/29/2026

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

    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import os
    from sklearn.linear_model import LinearRegression
    import textwrap

    # ========================================
    # Part 2: Load and Inspect Data
    # ========================================

    base_dir = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(base_dir, "thermal_expansion_data.csv"))

    # --- STUDENT CODE: Load CSV file --- #
    # df = pd.read_csv(".../thermal_expansion_data.csv")

    # Display required information
    print("--- Thermal Expansion Dataset ---")
    print()
    print(df.head(12))
    print()

    # ========================================
    # Part 3: Display Data on a Scatter Plot
    # ========================================

    fig1, ax1 = plt.subplots(figsize=(10, 6))
    
    site_colors = {"A": "#2196F3", "B": "#FF9800", "C": "#4CAF50"}
    site_markers = {"A": "o", "B": "s", "C": "^"}
    site_labels = {"A": "Site A (Near fixed support)", "B": "Site B (Mid-span)", "C": "Site C (Near free end)"}
    
    for site, group in df.groupby("Site"):
        ax1.scatter(
            group["Temp_C"],
            group["Expansion_mm"],
            color=site_colors[site],
            marker=site_markers[site],
            label=site_labels[site],
            s=100,
            edgecolors="white",
            linewidths=0.8,
            zorder=3
        )

    # Add a descriptive title to the plot
    ax1.set_title(
        "Thermal Expansion at Different Sites on an Aluminum Beam", 
        fontsize=14, pad=15)
    ax1.set_xlabel("Temperature (°C)", fontsize=12, labelpad=10)
    ax1.set_ylabel("Thermal Expansion (mm)", fontsize=12, labelpad=10)

    # Increase axis tick label size for better readability
    ax1.tick_params(axis="both", labelsize=12)
    ax1.set_xlim(-5, 105)
    ax1.set_ylim(0, 3)
    ax1.legend(framealpha=0.9, fontsize=12)
    ax1.grid(True, linestyle="--", alpha=0.4)
    
    plt.minorticks_on()
    plt.tight_layout()
    # plt.savefig("exp_temp_plot.png")
    # plt.show()
    # plt.close()

    # ========================================
    # Part 4: Compute Linear Regression
    # ========================================

    # scikit-learn expects a 2D feature array (n_samples, n_features)
    x = df["Temp_C"].values.reshape(-1, 1)   # independent variable: temperature in Celsius
    y = df["Expansion_mm"].values            # dependent variable: thermal expansion

    model = LinearRegression()
    model.fit(x, y)

    slope = model.coef_[0]
    intercept = model.intercept_

    y_pred = model.predict(x)

    sse = np.sum((y - y_pred)**2)
    sst = np.sum((y - np.mean(y))**2)
    r2 = 1 - (sse / sst)

    # Print the regression results in a clear and organized format
    print("--- LINEAR REGRESSION RESULTS ---")
    print()
    print(f"  Equation  :  Expansion = {slope:.3f} × Temp + {intercept:.3f}")
    print(f"  Slope     :  {slope:.3f}  mm per °C")
    print(f"  Intercept :  {intercept:.3f}  mm")
    print(f"  R²        :  {r2:.3f}")
    print(f"  SSE       :  {sse:.3f}  (mm)²")
    print(f"  SST       :  {sst:.3f}  (mm)²")


    # ========================================
    # Part 5: Plot Regression Line on Same Plot
    # ========================================

    y_predicted = model.predict(x)
    
    
    # Create a new scatter plot of the original data points (same as before)
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    
    for site, group in df.groupby("Site"):
        ax2.scatter(
            group["Temp_C"], 
            group["Expansion_mm"],
            color=site_colors[site],
            marker=site_markers[site], 
            label=site_labels[site],
            s=100, 
            edgecolors="white", 
            linewidths=0.8, 
            zorder=3,
        )

    ax2.plot(
        x, y_predicted,
        color="#E53935", 
        linewidth=2.5,
        label=f"Regression: Expansion = {slope:.3f}·Temp + {intercept:.3f}  (R²={r2:.3f})",
        zorder=2,
    )

    plot_title = "Regression Fit: Thermal Expansion–Temperature Relationship at Three Aluminum Beam Sites"
    wrapped_title = "\n".join(textwrap.wrap(plot_title, width=65))

    ax2.set_title(
        wrapped_title, 
        fontsize=14, pad=15)
    ax2.set_xlabel("Temperature (°C)", fontsize=12, labelpad=10)
    ax2.set_ylabel("Thermal Expansion (mm)", fontsize=12, labelpad=10)
    ax2.tick_params(axis="both", labelsize=12)
    ax2.set_xlim(-5, 105)
    ax2.set_ylim(0, 3)

    ax2.legend(framealpha=0.9, fontsize=12, loc="best")
    ax2.grid(True, linestyle="--", alpha=0.4)
    
    plt.minorticks_on()
    plt.tight_layout()
    # plt.savefig("exp_temp__regression_plot.png")
    # plt.show()
    # plt.close()



if __name__ == "__main__":
    main()