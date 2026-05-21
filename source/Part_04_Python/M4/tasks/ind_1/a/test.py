import matplotlib.pyplot as plt

# Example data
time = [0, 5, 10, 15, 20, 25]

temperature = [68, 72, 78, 85, 88, 90]
power = [120, 135, 150, 165, 180, 190]

# Create figure and first axis
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot temperature data as a red line plot with circle data markers
ax1.plot(time, temperature, marker='o', color='red')

# Label first y-axis
ax1.set_xlabel("Time (minutes)", fontsize=12)
ax1.set_ylabel("Temperature (C)", fontsize=12)

# Increase size of axis tick labels
ax1.tick_params(axis="both", labelsize=12)

# Create second y-axis
ax2 = ax1.twinx()

# Plot power data as a blue line plot with data markers
ax2.plot(time, power, marker='s', color='blue')

# Label second y-axis
ax2.set_ylabel("Power Consumption (W)", fontsize=12)

# Increase size of axis tick labels
ax2.tick_params(axis="both", labelsize=12)

# Add title
plt.title("Machine Temperature and Power Consumption", fontsize=14)

plt.tight_layout()
plt.show()