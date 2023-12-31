# Load Testing Simulator

This file contains a simple load testing simulator that can be used to test the performance of a server.

## Author
Sébastien Delsad

## Date
2023-06-26

## Description
The load testing simulator is designed to simulate the behavior of multiple users interacting with a server. It allows you to define a set of actions that each user can perform and simulate different load scenarios by specifying the number of users, ramp-up time, peak load time, ramp-down time, and timeout.

The simulator uses threads to simulate concurrent user requests and provides real-time plots to monitor the progress of the load test. It also includes a queue to collect the outputs from the simulated clients.

## Dependencies
The following dependencies are required to run the load testing simulator:

To install:

- `pyformulas`: A custom module for real-time plotting.

Already installed with Python:

- `time`: Provides functions for working with time-related tasks.
- `threading`: Allows the use of threads for concurrent execution.
- `random`: Provides functions for generating random numbers.
- `queue`: Implements thread-safe queues for communication between threads.
- `math`: Provides mathematical functions for rounding and calculations.
- `enum`: Supports the definition of enumerated types.
- `real_time_plot`: A custom module for real-time plotting.

The `real_time_plot` module is used to create real-time plots to visualize the number of users, response time, and success rate during the load test. Make sure the `real_time_plot.py` file is present in the same directory as this script.

## Usage
To use the load testing simulator, follow these steps:

1. Define the actions that each user can perform by creating a list of tuples in the format `[(action, probability), ...]`. The `action` should be a function that takes a `user_id` and returns `True` if successful, and `probability` is the probability of that action being performed.
2. Create a `queue.Queue` object to collect the results from the server. If no result queue is provided (None), a new queue will be created internally.
3. Create an instance of the `Simulator` class with the following parameters:
   - `actions`: The list of actions defined in step 1.
   - `peak_users`: The number of users to simulate at peak load.
   - `result_queue`: The result queue created in step 2.
   - `ramp_up_time`: The time to ramp up to peak users.
   - `load_time`: The time to hold peak users.
   - `ramp_down_time`: The time to ramp down to 0 users.
   - `timeout`: The maximum time to wait for a response from the server before considering the request failed.
4. Call the `simulate()` method of the `Simulator` instance to start the load test.
5. Monitor the console output and the real time plot to see the progress of the load test.
6. After the load test finishes, the plot will be saved to a file named `rtp.pdf` in the current directory.

## Example
Here's an example usage of the load testing simulator:

```python
import os
import time
import random
import real_time_plot

# Define the action function
def fun(x):
    """Function to simulate a request to the server."""
    a = random.random()
    time.sleep(a)
    return a > 0.5

def main():
    """Main function."""
    sim = Simulator([(fun, 1)], 5, None, 5, 5, 5, 10)
    sim.simulate()

    os.system("rtp.pdf")

if __name__ == "__main__":
    main()
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.