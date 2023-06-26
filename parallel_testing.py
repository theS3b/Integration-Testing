# This file contains a simple load testing simulator that can be used to test the performance of a server.
# Author: Sébastien Delsad
# Date: 2023-06-26

import time
import threading
import random
import queue
from math import ceil, floor
from enum import Enum
import real_time_plot


class Simulator:
    """Simulates a load test."""

    class State(Enum):
        """State of the simulator."""

        RAMP_UP = 1
        FULL_LOAD = 2
        RAMP_DOWN = 3
        FINISHED = 4

    def __init__(
        self,
        actions,
        peak_users,
        result_queue,
        ramp_up_time,
        load_time,
        ramp_down_time,
        timeout,
    ):
        """
        :param actions: List of actions to perform. Of the form [(action, probability), ...] where action is a function that takes user_id and returns true if successful, and probability is the probability of that action being performed
        :param peak_users: Number of users to simulate at peak
        :param ramp_up_time: Time to ramp up to peak users
        :param load_time: Time to hold peak users
        :param ramp_down_time: Time to ramp down to 0 users
        :param timeout: Max time to wait for a response from the server before considering the request failed
        """
        assert (
            sum((prob for action, prob in actions)) == 1
        ), "Probabilities must sum to 1"
        assert peak_users > 0, "Peak users must be greater than 0"
        assert ramp_up_time > 0, "Ramp up time must be greater than 0"
        assert ramp_down_time > 0, "Ramp down time must be greater than 0"
        assert timeout > 0, "Timeout must be greater than 0"
        assert result_queue is None or isinstance(
            result_queue, queue.Queue
        ), "Result queue must be a queue.Queue (thread safe)"

        self.peak_users = peak_users
        self.ramp_up_time = ramp_up_time
        self.load_time = load_time
        self.ramp_down_time = ramp_down_time
        self.timeout = timeout
        self.actions = actions
        self.result_queue = result_queue if result_queue is not None else queue.Queue()
        self.inform_time = 2  # Inform the user every 5 seconds via the console
        self.rtp_update_time = 1  # Update the real time plots every 1 second

        self.current_users = 0
        self.thread_pool = set()

        # Initialize real time plots
        self.rtp_nb_users = real_time_plot.RealTimePlot(
            "Time (s)",
            "Number of users",
            "Load testing - Number of Users",
            (0, 10),
            (0, peak_users),
        )

        self.rtp_avg_resp_time = real_time_plot.RealTimePlot(
            "Time (s)", "Average response time (s)", "Load testing - Response Time", (0, 10), (0, 1)
        )

        self.rtp_success_rate = real_time_plot.RealTimePlot(
            "Time (s)", "Success rate", "Load testing - Success Rate", (0, 10), (0, 1)
        )

    def __simulate_user(self, user_id):
        """
        Simulates a single user's behavior and returns a value.

        :param user_id: ID of the user
        :return: Value returned by the user's actions
        """

        # Sample from actions
        action = random.choices(
            [action for action, prob in self.actions],
            [prob for action, prob in self.actions],
        )[0]

        start_time = time.time()

        # Perform action
        ret = action(user_id)

        end_time = time.time()
        execution_time = end_time - start_time

        return execution_time, ret

    def __launch_user(self, thread):
        """Launches a user thread."""
        self.current_users += 1

        thread.start()

        # Register the thread in the thread pool
        self.thread_pool.add(thread)

    def __show_progress(self):
        """Shows the progress of the load test."""
        avg_resp_time = (
            sum((resp_time for resp_time, _ in self.result_queue.queue)) /
            len(self.result_queue.queue)
            if len(self.result_queue.queue) > 0 else 0)

        success_rate = (
            sum((1 if ret else 0 for _, ret in self.result_queue.queue)) /
            len(self.result_queue.queue)
            if len(self.result_queue.queue) > 0 else 0
        )

        # Update real time plots
        self.rtp_nb_users.update_line(self.current_users)
        self.rtp_avg_resp_time.update_line(avg_resp_time)
        self.rtp_success_rate.update_line(success_rate)

    def simulate(self):
        """Simulates the load test."""

        state = self.State.RAMP_UP
        time_last_inform = 0
        time_last_plot = 0
        time_new_state_started = time.time()
        thread_number = 0
        user_thread = None

        while state != self.State.FINISHED:

            if user_thread is None:
                thread_number += 1
                user_thread = threading.Thread(
                    target=lambda: self.result_queue.put(
                        self.__simulate_user(thread_number)
                    ),
                    daemon=True,
                )

            if state == self.State.RAMP_UP:
                # Here we ceil the result e.g. 9.1 users -> we create a new user
                ideal_nb_users = ceil(
                    self.peak_users *
                    (time.time() - time_new_state_started) /
                    self.ramp_up_time
                )

            elif state == self.State.FULL_LOAD:
                ideal_nb_users = self.peak_users

            elif state == self.State.RAMP_DOWN:
                # Here we floor the result e.g. 9.9 users -> we don't create a new user
                ideal_nb_users = floor(
                    self.peak_users *
                    (1 - (time.time() - time_new_state_started) /
                        self.ramp_down_time)
                )

            # Adjust number of users #

            # Remove threads finished from the thread pool
            self.thread_pool = set(
                (thread for thread in self.thread_pool if thread.is_alive())
            )

            threads_were_removed = len(self.thread_pool) != self.current_users
            self.current_users = len(self.thread_pool)

            # Add new threads if necessary
            threads_were_added = False
            if self.current_users < ideal_nb_users:
                self.__launch_user(user_thread)
                user_thread = None
                threads_were_added = True

            # Manage logging
            if (threads_were_added or threads_were_removed) and time.time() - time_last_inform >= self.inform_time:
                print(
                    f"Current number of users: {self.current_users}/{self.peak_users}")
                time_last_inform = time.time()

            # Manage real time plots
            if time.time() - time_last_plot >= self.rtp_update_time:
                self.__show_progress()
                time_last_plot = time.time()

            # Transition logic #
            if state == self.State.RAMP_UP and self.current_users >= self.peak_users:
                state = self.State.FULL_LOAD
                time_new_state_started = time.time()
                print("Ramp up finished. Starting full load.")

            if state == self.State.FULL_LOAD and time.time() - time_new_state_started >= self.load_time:
                state = self.State.RAMP_DOWN
                time_new_state_started = time.time()
                print("Full load finished. Starting ramp down.")

            if state == self.State.RAMP_DOWN and self.current_users <= 0:
                state = self.State.FINISHED
                time_new_state_started = time.time()
                print("Ramp down finished.")

            if state == self.State.FINISHED:
                print("Load testing finished.")

                # Show real time plots
                self.rtp_nb_users.show()
                self.rtp_avg_resp_time.show()
                self.rtp_success_rate.show()


def fun(x):
    print('test', x)
    time.sleep(5)
    return x


def main():
    qu = queue.Queue()
    sim = Simulator([(fun, 1)], 5, qu, 5, 5, 5, 10)
    sim.simulate()

    print("Results:")
    while not qu.empty():
        print(qu.get())


if __name__ == "__main__":
    main()
