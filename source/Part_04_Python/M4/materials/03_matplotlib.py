"""
MATPLOTLIB - is a plotting library for the Python programming language and its
numerical mathematics extension NumPy.

Documentation: https://matplotlib.org/stable/contents.html

Installing matplotlib - Enter the following command in the terminal:

python3 -m pip install matplotlib

Basic Plotting:

    - The most basic plot is the line plot.
    - A line plot is created by specifying the x and y values of the data points you
      want to plot and then calling the plot() function.
    - The plot() function takes the x and y values as arguments and creates a line plot.
    - The show() function is used to display the plot.
    - The set_title(), set_xlabel(), and set_ylabel() functions are used to set the
      title, x-axis label, and y-axis label of the plot, respectively.
    - The savefig() function is used to save the plot as an image file.

Types of Plots:

    - Matplotlib provides a variety of plots that can be used to visualize data.
    - Some of the commonly used plots are: Line Plot, Scatter Plot, Bar Plot, Histogram,
      Pie Chart, Box Plot, Heatmap, etc.

Customizing Plots:

    - Matplotlib allows you to customize the appearance of the plots by setting various
      properties such as the color, line style, marker style, etc.
    - You can also add labels, titles, legends, and annotations to the plots.

Multiple Plots:

    - You can create multiple plots in the same figure by using the subplots() function.
    - The first two arguments to the subplots() function are the number of rows and the
      number of columns.
    - Example:
        fig, ax = plt.subplots(2, 1)

        ax[0].plot(x, y1)

        ax[1].plot(x, y2)

    - The tight_layout() function is used to prevent overlap of titles and labels.
"""

"""
# Example: Basic Plotting - Line Plot
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [1, 4, 9, 16, 25]

fig, ax = plt.subplots()

ax.plot(x, y)
ax.set_title("Simple Plot")
ax.set_xlabel("x-axis")
ax.set_ylabel("y-axis")

fig.savefig("1_simple_plot.png")
plt.show()

# Example: Customizing Plots
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [1, 4, 9, 16, 25]

fig, ax = plt.subplots()

ax.plot(x, y, color="red", linestyle="--", marker="o", label="Data Points")
ax.set_title("Customized Plot")
ax.set_xlabel("x-axis")
ax.set_ylabel("y-axis")
ax.legend()

fig.savefig("2_custom_plot.png")
plt.show()

# Example: Scatter Plot
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [1, 4, 9, 16, 25]

fig, ax = plt.subplots()

ax.scatter(x, y, color="blue", marker="x", label="Data Points")
ax.set_title("Scatter Plot")
ax.set_xlabel("x-axis")
ax.set_ylabel("y-axis")
ax.legend()

fig.savefig("3_scatter_plot.png")
plt.show()

# Example: Bar Plot
import matplotlib.pyplot as plt

x = ["A", "B", "C", "D", "E"]
y = [10, 20, 15, 25, 30]

fig, ax = plt.subplots()

ax.bar(x, y, color="green", label="Data Points")
ax.set_title("Bar Plot")
ax.set_xlabel("Categories")
ax.set_ylabel("Values")
ax.legend()

fig.savefig("4_bar_plot.png")
plt.show()

# Example: Histogram
import matplotlib.pyplot as plt
import numpy as np

data = np.random.randn(1000)
fig, ax = plt.subplots()
ax.hist(data, bins=30, color="orange", edgecolor="black")
ax.set_title("Histogram")
ax.set_xlabel("Values")
ax.set_ylabel("Frequency")

fig.savefig("5_histogram.png")
plt.show()

# Example: Pie Chart
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

sizes = [20, 30, 25, 25]
labels = ["A", "B", "C", "D"]

ax.pie(
    sizes,
    labels=labels,
    autopct="%1.1f%%",
    startangle=90,
    colors=["red", "blue", "green", "yellow"],
)
ax.set_title("Pie Chart")

fig.savefig("6_pie_chart.png")
plt.show()

# Example: Box Plot
import matplotlib.pyplot as plt
import numpy as np

data = np.random.randn(100, 5)
fig, ax = plt.subplots()
ax.boxplot(data, patch_artist=True, notch=True, vert=False)
ax.set_title("Box Plot")
ax.set_xlabel("Values")  # works since boxes are horizontal

fig.savefig("7_box_plot.png")
plt.show()

# Example: Heatmap
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()
data = np.random.rand(10, 10)

im = ax.imshow(data, cmap="hot", interpolation="nearest")
ax.set_title("Heatmap")
fig.colorbar(im, ax=ax)   # fixed
fig.savefig("8_heatmap.png")
plt.show()

# Example: Multiple Plots
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y1 = [1, 4, 9, 16, 25]
y2 = [1, 2, 3, 4, 5]

fig, ax = plt.subplots(2, 1)

ax[0].plot(x, y1, color="red", marker="o")
ax[0].set_title("Subplot 1")
ax[0].set_xlabel("x-axis")
ax[0].set_ylabel("y-axis")

ax[1].plot(x, y2, color="blue", marker="x")
ax[1].set_title("Subplot 2")
ax[1].set_xlabel("x-axis")
ax[1].set_ylabel("y-axis")

fig.tight_layout()
fig.savefig("9_multi_plot.png")
plt.show()
"""
