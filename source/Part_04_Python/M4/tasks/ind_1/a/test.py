import matplotlib.pyplot as plt

# Example data
time = [0, 5, 10, 15, 20, 25]

temperature = [68, 72, 78, 85, 88, 90]
power = [120, 135, 150, 165, 180, 190]

# Create figure and first axis
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot temperature data as a red line plot with circle data markers
ax1.plot(time, temperature, marker='o', color='red')

# Label first data series axes and add color to match the data series
ax1.set_ylabel("Temperature (C)", fontsize=14, color='red')
ax1.set_xlabel("Time (minutes)", fontsize=14)

# Y-axis ticks red, X-axis ticks black — must set separately
ax1.tick_params(axis="y", labelsize=13, colors='red')
ax1.tick_params(axis="x", labelsize=13, colors='black')

# Set y-axis limits ('Temperature (C)')
ax1.set_ylim(60, 100)

# Create second y-axis
ax2 = ax1.twinx()

# Plot power data as a blue line plot with data markers
ax2.plot(time, power, marker='s', color='blue')

# Label second y-axis and add color to match the data series
ax2.set_ylabel("Power Consumption (W)", fontsize=14, color='blue')

# Y-axis ticks blue — no need to touch x-axis on ax2 (it's shared with ax1)
ax2.tick_params(axis="y", labelsize=13, colors='blue')

# Add title
plt.title("Machine Temperature and Power Consumption", fontsize=16)

# Insert legend for both data series in the upper left corner of the plot
plt.legend([ax1.lines[0], ax2.lines[0]], ["Temperature", "Power Consumption"], loc="upper left", fontsize=13)

plt.tight_layout()
plt.show()