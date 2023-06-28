from typing import Union, List, Tuple, Iterable
import requests
from itertools import chain


class AppOutcome:
    """Class that contains the outcome of a request."""

    def __init__(self, times: List[float], body: str, status_code: int, url_accessed: str, success: bool = None, response_reason: str = None):
        self.times = times
        self.success = success if success is not None else status_code == 200
        self.body = body
        self.url_accessed = url_accessed
        self.status_code = status_code
        self.response_reason = response_reason

    def __str__(self):
        return f"AppOutcome(success={self.success}, times={self.times}, body={self.body}, status_code={self.status_code}), response_reason={self.response_reason}), url_accessed={self.url_accessed})"

    def __repr__(self):
        return str(self)

    def merge(self, other):
        """ Merges two AppOutcome objects. """
        return AppOutcome(times=self.times + other.times,
                          body=other.body,
                          url_accessed=other.url_accessed,
                          status_code=other.status_code,
                          success=self.success and other.success)


def get_stats(outcomes: List[float]) -> (float, float):
    """ Returns the average time of the given outcomes. """
    sum_times = 0
    size = 0
    max_resp_time = 0

    times_gen = chain.from_iterable(outcome.times for outcome in outcomes)

    for time_elem in times_gen:
        sum_times += time_elem
        max_resp_time = max_resp_time if max_resp_time > time_elem else time_elem
        size += 1

    success_rate = (sum(outcome.success for outcome in outcomes) /
                    len(outcomes) if len(outcomes) > 0 else 0)
    avg_resp_time = sum_times / size if size > 0 else 0

    return avg_resp_time, max_resp_time, success_rate


def main():
    """ Tests that the class works as expected. """
    x1 = AppOutcome(times=[1, 2, 3], success=True,
                    body="test", status_code=200, url_accessed="test")
    x2 = AppOutcome(times=[1, 2, 3], success=False,
                    body="test", status_code=400, url_accessed="test")
    x3 = AppOutcome(times=[1, 2, 3], body="test",
                    status_code=400, url_accessed="test")
    x4 = AppOutcome(times=[1, 2, 3], body="test",
                    status_code=200, url_accessed="test")

    assert x1.success
    assert not x2.success
    assert not x3.success
    assert x4.success
    print("Success!")


if __name__ == "__main__":
    main()
