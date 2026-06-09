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

Academic Integrity Statement:
    I have not used source code obtained from any unauthorized
    source, either modified or unmodified; nor have I provided
    another student access to my code.  The project I am
    submitting is my own original work.
"""

def main():
    
# =============================================================================
#  SECTION 1 — LOAD THE DATASET
# =============================================================================
#
#  Below is a real-world-style dataset of 20 water quality samples collected
#  at three sites along a river during June–August.
#
#  Columns:
#    sample_id   : unique sample identifier
#    site        : monitoring site (A = upstream, B = midstream, C = downstream)
#    temp_c      : water temperature in degrees Celsius
#    do_mg_l     : dissolved oxygen concentration in mg/L
#    ph          : pH of the water sample (provided for context, not used here)

    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import r2_score, mean_squared_error

    import os
    # print("get base directory ...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # print("reading CSV ...")
    df = pd.read_csv(os.path.join(base_dir, "river_data.csv"))

    # Load CSV file
    # df = pd.read_csv("source/Part_04_Python/M5/tasks/ind_1/a/river_data.csv")

    # =============================================================================
    #  SECTION 2 — DATA EXPLORATION
    # =============================================================================
    
    print("=" * 50)
    print("  WABASH RIVER AUTHORITY — Water Quality Dataset")
    print("=" * 50)
    # print(df.to_string(index=False))
    print()
    print(df)
    print()
    print("--- Summary Statistics ---")
    print(df[["temp_c", "do_mg_l", "ph"]].describe())
    print()

    # =============================================================================
    #  SECTION 3 — PLOT 1: EXPLORATORY SCATTER PLOT
    # =============================================================================

    fig1, ax1 = plt.subplots(figsize=(8, 5))
    
    site_colors = {"A": "#2196F3", "B": "#FF9800", "C": "#4CAF50"}
    site_markers = {"A": "o", "B": "s", "C": "^"}
    site_labels = {"A": "Site A (Upstream)", "B": "Site B (Midstream)", "C": "Site C (Downstream)"}
    
    for site, group in df.groupby("site"):
        ax1.scatter(
            group["temp_c"],
            group["do_mg_l"],
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
        "DO–Temperature Relationship at Wabash River Sites", 
        fontsize=14, pad=15)
    
    # Label the x-axis with correct units
    ax1.set_xlabel("Water Temperature (°C)", fontsize=12, labelpad=10)
    
    # Label the y-axis with correct units
    ax1.set_ylabel("Dissolved Oxygen (mg/L)", fontsize=12, labelpad=10)

    # Increase axis tick label size for better readability
    ax1.tick_params(axis="both", labelsize=11)
    ax1.set_xlim(ax1.get_xlim()[0] - 1, ax1.get_xlim()[1] + 1)
    ax1.set_ylim(ax1.get_ylim()[0] - 1, ax1.get_ylim()[1] + 1)

    ax1.legend(framealpha=0.9, fontsize=11)
    ax1.grid(True, linestyle="--", alpha=0.4)
    ax1.set_facecolor("#f9f9f9")
    
    plt.tight_layout()
    # plt.savefig("DO_temp_plot.png", dpi=150)
    # plt.show()
    # print("✔  Saved DO_temp_plot.png")

    # =============================================================================
    #  SECTION 4 — LINEAR REGRESSION WITH SCIKIT-LEARN
    # =============================================================================

    # scikit-learn expects a 2D feature array (n_samples, n_features)
    x = df["temp_c"].values.reshape(-1, 1)   # independent variable: temperature
    y = df["do_mg_l"].values                 # dependent variable: dissolved oxygen

    # Create a LinearRegression model object and fit it to x and y
    model = LinearRegression()
    model.fit(x, y)
    
    # Extract the slope and intercept from your fitted model
    slope = model.coef_[0]
    intercept = model.intercept_
    
    
    # Generate predictions for every temperature value in x
    y_pred = model.predict(x)

    # Calculate Sum of Squared Errors (SSE) to measure how 
    # well a model matches the actual data.
    sse = np.sum((y - y_pred)**2)

    # Calculate Sum of Squares Total (SST) to measure the total 
    # variability in the observed data.
    sst = np.sum((y - np.mean(y))**2)
    
    # Calculate R² (coefficient of determination) to quantify the 
    # proportion of variance in y explained by x.
    r2 = 1 - (sse / sst)
    
    # Note: alternatively, you can use r2_score() to compute R² 
    # using the actual and predicted y-values:
    # r2   = r2_score(y, y_pred)
    
    
    # Print the regression results in a clear and organized format
    print("=" * 50)
    print("  LINEAR REGRESSION RESULTS")
    print("=" * 50)
    print(f"  Equation  :  DO = {slope:.3f} × Temp + {intercept:.3f}")
    print(f"  Slope     :  {slope:.3f}  mg/L per °C")
    print(f"  Intercept :  {intercept:.3f}  mg/L")
    print(f"  R²        :  {r2:.3f}")
    print(f"  SSE       :  {sse:.3f}  (mg/L)²")
    print(f"  SST       :  {sst:.3f}  (mg/L)²")
    print()


    # =============================================================================
    #  SECTION 5 — PLOT 2: REGRESSION LINE OVERLAY
    # =============================================================================
    
    # Create a smooth temperature range for plotting the regression line
    # Hint: Use np.linspace(start, stop, num_points) to create 100 evenly-spaced
    #       temperature values between the min and max observed temperatures.
    #       Reshape to (-1, 1) so scikit-learn accepts it.
    
    temp_range = np.linspace(df["temp_c"].min(), df["temp_c"].max(), 100).reshape(-1, 1)
    
    
    # Generate predicted DO values for that temperature range using 
    # your fitted model.
    
    do_predicted = model.predict(temp_range)
    
    
    # Create a new scatter plot of the original data points (same as before)
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    
    for site, group in df.groupby("site"):
        ax2.scatter(
            group["temp_c"], 
            group["do_mg_l"],
            color=site_colors[site],
            marker=site_markers[site], 
            label=site_labels[site],
            s=100, 
            edgecolors="white", 
            linewidths=0.8, 
            zorder=3,
        )

    ax2.plot(
        temp_range, do_predicted,
        color="#E53935", 
        linewidth=2.5,
        label=f"Regression: DO = {slope:.3f}·T + {intercept:.3f}  (R²={r2:.3f})",
        zorder=2,
    )

    ax2.set_title(
        "Regression Fit: DO–Temperature Relationship at Wabash River Sites", 
        fontsize=14, pad=15)
    ax2.set_xlabel("Water Temperature (°C)", fontsize=12, labelpad=10)
    ax2.set_ylabel("Dissolved Oxygen (mg/L)", fontsize=12, labelpad=10)
    ax2.tick_params(axis="both", labelsize=11)
    ax2.set_xlim(ax2.get_xlim()[0] - 1, ax2.get_xlim()[1] + 1)
    ax2.set_ylim(ax2.get_ylim()[0] - 1, ax2.get_ylim()[1] + 1)

    ax2.legend(framealpha=0.9, fontsize=11)
    ax2.grid(True, linestyle="--", alpha=0.4)
    ax2.set_facecolor("#f9f9f9")
    
    plt.tight_layout()
    # plt.savefig("DO_temp_regression_plot.png", dpi=150)
    # plt.show()
    # print("✔  Saved DO_temp_regression_plot.png")

    # =============================================================================
    #  SECTION 8 — REFLECTION QUESTIONS  (answer as comments below each question)
    # =============================================================================
    #
    #  Q1. What does the SIGN of the slope tell you physically about the
    #      relationship between temperature and dissolved oxygen?
    #
    #  A1. 
    #
    #
    #  Q2. Your R² value should be close to 1.0. What does this tell you about
    #      how well temperature alone explains variation in DO?
    #      Name ONE other environmental variable that might also affect DO.
    #
    #  A2. 
    #
    #
    #  Q3. Look at your residual plot (plot_3.png). Do the residuals appear
    #      randomly scattered, or do you notice a pattern? What would a curved
    #      pattern in a residual plot suggest about your model choice?
    #
    #  A3. 
    #
    #
    #  Q4. Linear regression assumes the relationship continues indefinitely.
    #      Why is it physically unreasonable to use this model to predict DO
    #      at 0 °C or at 50 °C? What is this limitation called?
    #
    #  A4. 
    #
    #
    #  Q5. Site C is the most downstream location. Its data points tend to have
    #      lower DO than Sites A and B at similar temperatures. Suggest one
    #      real-world engineering reason why downstream DO might be lower even
    #      at the same temperature.
    #
    #  A5. 


if __name__ == "__main__":
    main()