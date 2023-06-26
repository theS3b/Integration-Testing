# This file provides a class that can be used to plot data in real time.
# Author: Sébastien Delsad
# Date: 2023-06-26

import matplotlib.pyplot as plt
import numpy as np
import time


class RealTimePlot:
    """Class that can be used to plot data in real time."""

    def __init__(self, x_label, y_label, title, x_range, y_range):
        """
        :param x_label: Label of the x axis
        :param y_label: Label of the y axis
        :param title: Title of the plot
        :param x_range: Range of the x axis
        :param y_range: Range of the y axis
        """
        self.x_label = x_label
        self.y_label = y_label
        self.title = title
        self.x_range = x_range
        self.y_range = y_range

        # Initialize empty lists to store x and y values
        self.x_values = []
        self.y_values = []

        # Create an empty plot
        plt.ion()  # Turn on interactive mode
        self.fig, self.ax = plt.subplots()
        (self.line,) = self.ax.plot(self.x_values, self.y_values)

        # Set up the plot
        self.ax.set_xlabel(self.x_label)
        self.ax.set_ylabel(self.y_label)
        self.ax.set_title(self.title)

        plt.pause(0.1)

    def update_line(self, new_data):
        """
        Updates the plot with new data.

        :param new_data: New data to add to the plot (y value)
        """

        self.line.set_xdata(np.append(
            self.line.get_xdata(), len(self.line.get_xdata())+1))
        self.line.set_ydata(np.append(self.line.get_ydata(), new_data))

        # Adjust the plot limits
        self.ax.relim()
        self.ax.autoscale_view()

        plt.draw()

        plt.pause(0.1)

    def show(self):
        """Shows the plot."""

        plt.show()

    def close(self):
        """Closes the plot."""

        plt.close()


# Test
if __name__ == "__main__":
    # Create a plot
    plot = RealTimePlot("X", "Y", "Dynamic Line Graph", [0, 100], [0, 100])

    # Add data to the plot
    for i in range(100):
        plot.update_line(i)
        time.sleep(0.1)

    # Show the plot
    plot.show()

    # Close the plot
    plot.close()
