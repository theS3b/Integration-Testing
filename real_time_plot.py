# This file provides a class that can be used to plot data in real time.
# Author: Sébastien Delsad
# Date: 2023-06-26

import matplotlib.pyplot as plt
import numpy as np
import time
import code


class RealTimePlot:
    """Class that can be used to plot data in real time."""

    def __init__(self, title, x_label, y_labels):
        """
        :param title: Title of the plot
        :param x_label: Label of the x axis
        :param y_labels: List of labels of the y axis
        """
        assert isinstance(y_labels, list), "Y labels must be a list"
        assert isinstance(x_label, str), "X label must be a string"
        assert isinstance(title, str), "Title must be a string"

        # Create an empty plot
        plt.ion()  # Turn on interactive mode
        self.fig, self.axes = plt.subplots(
            len(y_labels), 1)  # Create x subplots
        self.lines = []  # Store the lines for each subplot

        self.fig.suptitle(title)

        # Set up the subplots
        for i, ax in enumerate(self.axes):
            line, = ax.plot([], [])
            self.lines.append(line)

            ax.set_ylabel(y_labels[i])

        self.axes[-1].set_xlabel(x_label)

        # Add space between subplots
        plt.subplots_adjust(hspace=0.5)

        # Make it bigger
        self.fig.set_size_inches(10, 8)

        # Make title less far from the plot
        self.fig.tight_layout(rect=[0, 0.03, 1, 0.95])

        plt.pause(0.1)

    def update_line(self, new_data):
        """
        Updates the specified subplot with new data.

        :param new_data: New data to add to the subplot (y values)
        """

        for i, line in enumerate(self.lines):
            line.set_xdata(
                np.append(line.get_xdata(), len(line.get_xdata())+1))
            line.set_ydata(np.append(line.get_ydata(), new_data[i]))

        # Adjust the subplot limits
        for ax in self.axes:
            ax.relim()
            ax.autoscale_view()

        plt.draw()
        plt.pause(0.1)

    def show(self):
        """Shows the plot."""
        plt.show()
        code.interact(local=locals())

    def close(self):
        """Closes the plot."""
        plt.ioff()
        plt.close()


# Test
if __name__ == "__main__":
    # Test the RealTimePlot class
    rtp = RealTimePlot("Test", "X", ["Y1", "Y2", "Y3"])

    for i in range(50):
        rtp.update_line((i, i**2, i**3))
        time.sleep(0.01)
