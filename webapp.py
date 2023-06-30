from flask import Flask, render_template
import random
from collections import deque
import time
import multiprocessing as mp


class QueueFlaskApp(Flask):
    """ Flask app with a queue. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_queue = mp.Queue()
        self.x = [[0]]
        self.y = [[0], [0]]

    def get_data_queue(self):
        return self.data_queue

    def set_config(self, title, x_label, y_labels, configuration):
        self.title = title
        self.x_label = x_label
        self.y_labels = y_labels
        self.configuration = configuration


app = QueueFlaskApp(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/config')
def config():

    # Compute trace configuration
    traces = []

    i = 0
    for rowi, nb_lines in enumerate(app.configuration):
        xaxis_name = 'x' + str(rowi + 1)
        yaxis_name = 'y' + str(rowi + 1)

        for _ in range(nb_lines):

            traces.append(
                {'y': [0], 'type': 'scatter', 'xaxis': xaxis_name, 'yaxis': yaxis_name, 'name': app.y_labels[rowi]})

            i += 1

    last_axis_name = 'xaxis' + str(len(app.configuration))

    # Compute layout configuration
    layout = {
        'grid': {'rows': len(app.configuration), 'columns': 1, 'pattern': 'independent', 'roworder': 'top to bottom'},
        'responsive': True,
        'title': {
            'text': app.title,
            'xref': 'paper',
            'x': 0.5,
            'xanchor': 'center',
            'yref': 'container',
            'y': 0.95,
            'yanchor': 'top',
            'font': {
                'size': 24
            }
        },
        last_axis_name: {
            'title': {
                'text': app.x_label,
                'font': {
                    'size': 18,
                    'color': '#7f7f7f'
                }
            }
        }
    }

    for i, y_label in enumerate(app.y_labels):
        layout['yaxis' + str(i + 1)] = {
            'title': {
                'text': y_label,
                'font': {
                    'size': 18,
                    'color': '#7f7f7f'
                }
            }
        }

    return {'traces': traces, 'layout': layout}


@app.route('/data')
def get_data():
    # Get data from the queue
    if not app.data_queue.empty():
        new_data = app.data_queue.get()

        print(new_data)
        # Return the data as a JSON response
        return {
            'data': [
                {'y': new_data[0], 'type': 'scatter'},
                {'y': new_data[1], 'type': 'scatter'},
                {'y': new_data[2], 'type': 'scatter'},
                # Add more dictionaries for additional subplots
            ]
        }
    else:
        return {'data': []}


def generate_data(queue):
    while True:
        # Generate random data
        data = [[random.randint(0, 10) for _ in range(5)],
                [random.randint(0, 10) for _ in range(5)],
                [random.randint(0, 10) for _ in range(5)]]

        # Put the data in the queue
        queue.put(data)

        # Sleep for 1 second
        time.sleep(1)


if __name__ == '__main__':
    data_process = mp.Process(target=generate_data,
                              args=(app.get_data_queue(),))
    data_process.start()

    # Start the Flask app
    app.set_config('My plot', 'Time', ['Y1', 'Y2'], [2, 1])
    app.run(debug=True)

    # Terminate the data generation process when the Flask app exits
    data_process.terminate()
