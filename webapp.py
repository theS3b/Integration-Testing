from flask import Flask, render_template
import random
import queue


class QueueFlaskApp(Flask):
    """ Flask app with a queue. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_queue = queue.Queue()

    def get_data_queue(self):
        return self.data_queue


app = QueueFlaskApp(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data')
def get_data():
    # Generate random data for the plot
    x_data = list(range(10))
    y_data = [random.randint(1, 10) for _ in range(10)]

    # Return the data as a JSON response
    return {'data': {'x': x_data, 'y': y_data, 'type': 'scatter'}}


if __name__ == '__main__':
    app.run(debug=True)
