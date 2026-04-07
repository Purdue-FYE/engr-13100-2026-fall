"""
MATPLOTLIB - is a plotting library for the Python programming language and its numerical mathematics extension NumPy.

Documentation: https://matplotlib.org/stable/contents.html

Installing matplotlib - Enter the following command in the terminal: python3 -m pip install matplotlib

Basic Plotting:
    - The most basic plot is the line plot.
    - A line plot is created by specifying the x and y values of the data points you want to plot and then calling the plot() function.
    - The plot() function takes the x and y values as arguments and creates a line plot.
    - The show() function is used to display the plot.
    - The title(), xlabel(), and ylabel() functions are used to set the title, x-axis label, and y-axis label of the plot, respectively.
    - The savefig() function is used to save the plot as an image file.

Types of Plots:
    - Matplotlib provides a variety of plots that can be used to visualize data.
    - Some of the commonly used plots are: Line Plot, Scatter Plot, Bar Plot, Histogram, Pie Chart, Box Plot, Heatmap, etc.

Customizing Plots:
    - Matplotlib allows you to customize the appearance of the plots by setting various properties such as the color, line style, marker style, etc.
    - You can also add labels, titles, legends, and annotations to the plots.

Multiple Plots:
    - You can create multiple plots in the same figure by using the subplot() function.
    - The subplot() function takes three arguments: the number of rows, the number of columns, and the index of the subplot.
    - Example:
        plt.subplot(2, 1, 1) # Create the first subplot
        plt.plot(x, y1)

        plt.subplot(2, 1, 2) # Create the second subplot
        plt.plot(x, y2)
    - You can create multiple plots in the same figure by calling the subplot() function multiple times.
    - The tight_layout() function is used to adjust the spacing between the plots.
"""
"""
# Example: Basic Plotting - Line Plot
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [1, 4, 9, 16, 25]

plt.plot(x, y)
plt.title("Simple Plot")
plt.xlabel("x-axis")
plt.ylabel("y-axis")
plt.savefig("1_simple_plot.png")
plt.show()

# Example: Customizing Plots
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [1, 4, 9, 16, 25]

plt.plot(x, y, color="red", linestyle="--", marker="o", label="Data Points")
plt.title("Customized Plot")
plt.xlabel("x-axis")
plt.ylabel("y-axis")
plt.legend()
plt.savefig("2_custom_plot.png")
plt.show()

# Example: Scatter Plot
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [1, 4, 9, 16, 25]

plt.scatter(x, y, color="blue", marker="x", label="Data Points")
plt.title("Scatter Plot")
plt.xlabel("x-axis")
plt.ylabel("y-axis")
plt.legend()
plt.savefig("3_scatter_plot.png")
plt.show()

# Example: Bar Plot
import matplotlib.pyplot as plt

x = ["A", "B", "C", "D", "E"]
y = [10, 20, 15, 25, 30]

plt.bar(x, y, color="green", label="Data Points")
plt.title("Bar Plot")
plt.xlabel("Categories")
plt.ylabel("Values")
plt.legend()
plt.savefig("4_bar_plot.png")
plt.show()

# Example: Histogram
import matplotlib.pyplot as plt
import numpy as np

data = np.random.randn(1000)

plt.hist(data, bins=30, color="orange", edgecolor="black")
plt.title("Histogram")
plt.xlabel("Values")
plt.ylabel("Frequency")
plt.savefig("5_histogram.png")
plt.show()

# Example: Pie Chart
import matplotlib.pyplot as plt

sizes = [20, 30, 25, 25]
labels = ["A", "B", "C", "D"]

plt.pie(
    sizes,
    labels=labels,
    autopct="%1.1f%%",
    startangle=90,
    colors=["red", "blue", "green", "yellow"],
)
plt.title("Pie Chart")
plt.savefig("6_pie_chart.png")
plt.show()

# Example: Box Plot
import matplotlib.pyplot as plt
import numpy as np

data = np.random.randn(100, 5)

plt.boxplot(data, patch_artist=True, notch=True, vert=0)
plt.title("Box Plot")
plt.xlabel("Values")
plt.savefig("7_box_plot.png")
plt.show()

# Example: Heatmap
import matplotlib.pyplot as plt
import numpy as np

data = np.random.rand(10, 10)

plt.imshow(data, cmap="hot", interpolation="nearest")
plt.title("Heatmap")
plt.colorbar()
plt.savefig("8_heatmap.png")
plt.show()

# Example: Multiple Plots
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y1 = [1, 4, 9, 16, 25]
y2 = [1, 2, 3, 4, 5]

plt.subplot(2, 1, 1)
plt.plot(x, y1, color="red", marker="o")
plt.title("Subplot 1")
plt.xlabel("x-axis")
plt.ylabel("y-axis")

plt.subplot(2, 1, 2)
plt.plot(x, y2, color="blue", marker="x")
plt.title("Subplot 2")
plt.xlabel("x-axis")
plt.ylabel("y-axis")

plt.tight_layout()
plt.savefig("9_multi_plot.png")
plt.show()

"""
