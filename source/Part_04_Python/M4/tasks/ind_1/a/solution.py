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

Academic Integrity Statement:
    I have not used source code obtained from any unauthorized
    source, either modified or unmodified; nor have I provided
    another student access to my code.  The project I am
    submitting is my own original work.
"""


def main():

    # =========================
    # Part 1: Import and Load Data
    # =========================

    import numpy as np
    import pandas as pd
    import os
    # print("Working directory:", os.getcwd())
    # print("Script location:", os.path.abspath(__file__))


    # print("get base directory ...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # print("reading CSV ...")
    df = pd.read_csv(os.path.join(base_dir, "traffic_data.csv"))


    # Load CSV file
    # df = pd.read_csv("source/Part_04_Python/M4/tasks/ind_1/a/traffic_data.csv")

    # Display required information
    print("First 5 rows:\n", df.head())
    print("\nColumn names:\n", df.columns)
    print("\nShape (rows, columns):", df.shape)


    # =========================
    # Part 2: NumPy Calculations
    # =========================

    # Convert columns to NumPy arrays
    vehicle_count = df["Vehicle_Count"].to_numpy()
    avg_speed = df["Avg_Speed_mph"].to_numpy()

    # Calculate Traffic Index
    traffic_index = vehicle_count / avg_speed

    # Increase by 15% (construction effect)
    traffic_index = traffic_index * 1.15

    # Display first 10 values
    print("\nFirst 10 Traffic Index values:")
    print(traffic_index[:10])


    # =========================
    # Part 3: DataFrame Operations
    # =========================

    # Add Traffic_Index to DataFrame
    df["Traffic_Index"] = traffic_index

    # Filter datasets
    high_volume_df = df[df["Vehicle_Count"] > 400]
    low_speed_df = df[df["Avg_Speed_mph"] < 45]

    # Display results
    print("\nHigh Vehicle Count (>400) - first 5 rows:")
    print(high_volume_df.head())
    print("Number of rows:", len(high_volume_df))

    print("\nLow Speed (<45 mph) - first 5 rows:")
    print(low_speed_df.head())
    print("Number of rows:", len(low_speed_df))


    # =========================
    # Part 4: Summary Statistics
    # =========================

    columns = ["Vehicle_Count", "Avg_Speed_mph", "Traffic_Index"]

    print("\nSummary Statistics:")
    for col in columns:
        print(f"\n{col}:")
        print(f"Mean: {df[col].mean():.2f}")
        print(f"Max: {df[col].max():.2f}")
        print(f"Min: {df[col].min():.2f}")
        print(f"Std Dev: {df[col].std():.2f}")


    # =========================
    # Part 5: Visualization
    # =========================

    import matplotlib.pyplot as plt

    # 1. Scatter Plot
    plt.figure(figsize=(10, 5))
    plt.scatter(df["Vehicle_Count"],df["Avg_Speed_mph"], color="black")
    plt.ylabel("Average Speed (mph)", fontsize=12)
    plt.xlabel("Vehicle Count", fontsize=12)
    plt.title("Vehicle Count vs. Average Speed", fontsize=14)
    plt.tick_params(axis="both", labelsize=12)
    plt.grid(True)
    # plt.show()


    # 2. Line Plot

    # Prepare date data
    df["Date"] = pd.to_datetime(df["Date"])

    # Filter for June
    june_df = df[df["Date"].dt.month == 6]
    #print("\nJune Data - first 5 rows:")
    #print(june_df.head())

    plt.figure(figsize=(10, 5))
    plt.plot(june_df["Date"], june_df["Vehicle_Count"], color="blue", marker="o")
    plt.xlim(june_df["Date"].min(), june_df["Date"].max())
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Vehicle Count", fontsize=12)
    plt.title("Daily Vehicle Count (June 2026)", fontsize=14)
    plt.tick_params(axis="both", labelsize=12)
    plt.grid(True)
    # plt.show()


    # 3. Combined Plot

    # Create figure and first axis
    fig, ax1 = plt.subplots(figsize=(11, 6))

    ax1.plot(june_df["Date"], june_df["Vehicle_Count"], color="blue",
            marker="o", label="Vehicle Count")
    ax1.set_xlabel("Date", fontsize=12)
    ax1.set_ylabel("Vehicle Count", fontsize=12)
    ax1.tick_params(axis="both", labelsize=12)

    ax2 = ax1.twinx()
    ax2.scatter(june_df["Date"], june_df["Avg_Speed_mph"], color="black",
                label="Avg Speed (mph)")
    ax2.set_ylabel("Average Speed (mph)", fontsize=12)
    ax2.tick_params(axis="both", labelsize=12)

    ax1.set_xlim(june_df["Date"].min(), june_df["Date"].max())

    plt.title("Vehicle Count and Average Speed Over Time (June)", fontsize=14)
    fig.legend(loc="upper left")
    # plt.show()

if __name__ == "__main__":
    main()