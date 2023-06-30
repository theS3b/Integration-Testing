from flask import Flask, render_template
import random
import queue


class QueueFlaskApp(Flask):
    """ Flask app with a queue. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_queue = queue.Queue()
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
    # Generate random data for the subplots
    app.x[0] += range(app.x[0][-1], app.x[0][-1] + 10)
    app.y[0] += [random.randint(1, 10) for _ in range(10)]
    app.y[1] += [random.randint(1, 10) for _ in range(10)]
    # Add more y_data lists for additional subplots

    # Return the data as a JSON response
    return {
        'data': [
            {'x': app.x[0], 'y': app.y[0], 'type': 'scatter'},
            {'x': app.x[0], 'y': app.y[1], 'type': 'scatter'}
            # Add more dictionaries for additional subplots
        ]
    }


if __name__ == '__main__':
    app.run(debug=True)
