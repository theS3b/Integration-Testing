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


app = QueueFlaskApp(__name__)


@app.route('/')
def index():
    return render_template('index.html')


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
                {'y': new_data[1], 'type': 'scatter'}
                # Add more dictionaries for additional subplots
            ]
        }
    else:
        return {'data': []}


def generate_data(queue):
    while True:
        # Generate random data
        data = [[random.randint(0, 10) for _ in range(5)],
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
    app.run(debug=True)

    # Terminate the data generation process when the Flask app exits
    data_process.terminate()
