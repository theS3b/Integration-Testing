import matplotlib
import numpy as np
import time
import pyformulas as pf
from collections import deque
import matplotlib.pyplot as plt
matplotlib.use('agg')  # Use Agg backend to avoid crashing on headless servers

STOP_RTP = (False, None)  # Value to put in the queue to stop the plotting
# Value to put in the queue to save the plot
SAVE_STOP_RTP = (False, "rtp.pdf")


def async_real_time_plot(title, x_label, y_labels, configuration, data: deque = None):
    '''
    This function can be used to plot data in real time.
    To use it, simply call it in a thread and put data in the deque.
    The data must be a tuple (continue, data) where continue is a boolean indicating if the plotting should continue and data is a list containing the new y values for each plot.
    To stop the plotting, put (False, None) in the deque.

    :param title: Title of the plot
    :param x_label: Label of the x axis
    :param y_labels: List of labels of the y axis
    :param configuration: Configuration of the plot: [nb_lines1, nb_lines2, ...]
    :param data: Deque containing if the plotting should continue and the data to plot (continue, data)
    '''
    times = []

    # Create an empty plot
    fig, axes = plt.subplots(len(configuration), 1)  # Create x subplots
    lines = []  # Store the lines for each subplot

    # Set up the subplots
    for i, ax in enumerate(axes):
        for _ in range(configuration[i]):
            line, = ax.plot([], [])
            lines.append(line)

        ax.set_ylabel(y_labels[i])

    axes[-1].set_xlabel(x_label)

    # Add space between subplots
    plt.subplots_adjust(hspace=0.5)

    # Make it bigger
    fig.set_size_inches(10, 8)

    # Make title less far from the plot
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])

    screen = pf.screen(np.zeros((720, 720)), title=title)

    data_queue = data

    # Main loop
    while True:

        # Check for new data
        if data_queue:
            continue_run, new_data = data_queue.popleft()
        else:
            time.sleep(0.05)
            continue

        if not continue_run:
            break

        # Update the lines
        for i, line in enumerate(lines):
            line.set_xdata(np.append(line.get_xdata(),
                           len(line.get_xdata()) + 1))
            line.set_ydata(np.append(line.get_ydata(), new_data[i]))

        # Adjust the subplot limits
        for ax in axes:
            ax.relim()
            ax.autoscale_view()

        # Draw the plot
        t = time.time()
        fig.canvas.draw()
        times.append(time.time() - t)

        image = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))

        screen.update(image)

    # Save the plot if needed
    if isinstance(new_data, str):
        fig.suptitle(title, fontsize=16)
        plt.savefig(new_data, bbox_inches="tight")

    print("Max times rtp: ", max(times))

    plt.close()


if __name__ == "__main__":
    # Test the RealTimePlot as a thread
    q = deque()

    import threading
    t = threading.Thread(target=async_real_time_plot, args=(
        "Test", "X", ["Y1", "Y2"], [2, 1], q), daemon=True)
    t.start()

    for i in range(50):
        q.append((True, (i, i ** 2, i ** 3)))
        time.sleep(0.01)

    q.append((False, None))
    t.join()
