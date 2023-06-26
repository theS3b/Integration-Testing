import matplotlib.pyplot as plt
import random
import time
import numpy

# Initialize empty lists to store x and y values
x_values = []
y_values = []

# Create an empty plot
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()
line, = ax.plot(x_values, y_values)

# Set up the plot
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Dynamic Line Graph')

def update_line(hl, new_data):
    hl.set_xdata(numpy.append(hl.get_xdata(), len(hl.get_xdata())+1))
    hl.set_ydata(numpy.append(hl.get_ydata(), new_data))

    # Adjust the plot limits
    ax.relim()
    ax.autoscale_view()

    plt.draw()

for i in range(5):
    update_line(line, random.random())
    plt.pause(1)


import threading
import queue
def dosomething(param):
    return param * 2
que = queue.Queue()
thr = threading.Thread(target = lambda q, arg : q.put(dosomething(arg)), args = (que, 2))
thr.start()
print('Started')