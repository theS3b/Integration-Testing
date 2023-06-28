# This file provides a class that can be used to plot data in real time.
# Author: Sébastien Delsad
# Date: 2023-06-26

import matplotlib.pyplot as plt
import numpy as np
import time
import pyformulas as pf


class RealTimePlot:
    """Class that can be used to plot data in real time."""

    def __init__(self, title, x_label, y_labels, configuration):
        """
        :param title: Title of the plot
        :param x_label: Label of the x axis
        :param y_labels: List of labels of the y axis
        :param configuration: Configuration of the plot: [nb_lines1, nb_lines2, ...]
        """
        assert isinstance(y_labels, list), "Y labels must be a list"
        assert isinstance(x_label, str), "X label must be a string"
        assert isinstance(title, str), "Title must be a string"
        assert len(y_labels) == len(
            configuration), "Y labels and configuration must have the same length"

        # Create an empty plot
        self.fig, self.axes = plt.subplots(
            len(configuration), 1)  # Create x subplots
        self.lines = []  # Store the lines for each subplot

        # Set up the subplots
        for i, ax in enumerate(self.axes):
            for _ in range(configuration[i]):
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

        self.screen = pf.screen(np.zeros((720, 720)), title=title)

        self.configuration = configuration
        self.title = title

    def update_line(self, new_data):
        """
        Updates the specified subplot with new data.

        :param new_data: New data to add to the subplot (y values)
        """
        assert len(new_data) == len(
            self.lines), "New data must have the same length as the number of lines"

        for i, line in enumerate(self.lines):
            line.set_xdata(
                np.append(line.get_xdata(), len(line.get_xdata())+1))
            line.set_ydata(np.append(line.get_ydata(), new_data[i]))

        # Adjust the subplot limits
        for ax in self.axes:
            ax.relim()
            ax.autoscale_view()

        self.fig.canvas.draw()
        image = np.frombuffer(self.fig.canvas.tostring_rgb(), dtype=np.uint8)
        image = image.reshape(self.fig.canvas.get_width_height()[::-1] + (3,))
        self.screen.update(image)

    def save(self, plt_name="rtp.pdf"):
        """Shows the plot."""
        # Add title
        self.fig.suptitle(self.title, fontsize=16)
        plt.savefig(plt_name, bbox_inches="tight")
        self.close()

    def close(self):
        """Closes the plot."""
        plt.close()


# Test
if __name__ == "__main__":
    # Test the RealTimePlot class
    rtp = RealTimePlot("Test", "X", ["Y1", "Y2"], [2, 1])

    for i in range(50):
        rtp.update_line((i, i**2, i**3))
        time.sleep(0.01)

    rtp.close()
