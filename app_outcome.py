from typing import Union, List, Tuple, Iterable
import requests


class AppOutcome:
    """Class that contains the outcome of a request."""

    def __init__(self, req_time: float, body: str, status_code: int, url_requested: str, url_returned: str, success: bool = None, response_reason: str = None):
        self.req_time = req_time
        self.success = success if success is not None else status_code == 200
        self.body = body
        self.url_requested = url_requested
        self.status_code = status_code
        self.response_reason = response_reason
        self.url_returned = url_returned

    @staticmethod
    def from_response(req_time: float, url_req, response: requests.Response, success: bool = None) -> 'AppOutcome':
        """Creates an AppOutcome from a requests.Response object."""
        assert isinstance(
            response, requests.Response), "Response must be a requests.Response object"

        out_success = success if success is not None else response.status_code == 200
        return AppOutcome(req_time, response.text, response.status_code,
                          url_req, response.url, out_success, response.reason)

    @staticmethod
    def from_exception(req_time: float, url_req: str, exception: Exception) -> 'AppOutcome':
        """Creates an AppOutcome from an exception."""
        assert isinstance(
            exception, Exception), "Exception must be an Exception object"

        return AppOutcome(req_time, str(exception), 999, url_req, "EXCEPTION", False, "EXCEPTION")

    def light_copy(self) -> 'AppOutcome':
        """Returns a light copy of the object."""
        return AppOutcome(self.req_time, "", self.status_code, self.url_requested, self.url_returned, self.success, self.response_reason)

    def __str__(self):
        return f"AppOutcome(req_time={self.req_time}, success={self.success}, url_req={self.url_requested}, status_code={self.status_code}, response_reason={self.response_reason}, url_returned={self.url_returned})"

    def __repr__(self):
        return str(self)


def get_stats(outcomes: List[AppOutcome]) -> (float, float):
    """ Returns the average req_time of the given outcomes. """

    avg_resp_req_time = (sum(outcome.req_time for outcome in outcomes) /
                         len(outcomes) if len(outcomes) > 0 else 0)

    max_resp_req_time = max(outcome.req_time for outcome in outcomes) if len(
        outcomes) > 0 else 0

    min_resp_req_time = min(outcome.req_time for outcome in outcomes) if len(
        outcomes) > 0 else 0

    success_rate = (sum(outcome.success for outcome in outcomes) /
                    len(outcomes) if len(outcomes) > 0 else 0)

    return avg_resp_req_time, max_resp_req_time, min_resp_req_time, success_rate


def main():
    """ Tests that the class works as expected. """
    x1 = AppOutcome(req_time=1, success=True,
                    body="test", status_code=200, url_requested="test", url_returned="test")
    x2 = AppOutcome(req_time=2, success=False,
                    body="test", status_code=400, url_requested="test", url_returned="test")
    x3 = AppOutcome(req_time=3, body="test",
                    status_code=400, url_requested="test", url_returned="test")
    x4 = AppOutcome(req_time=4, body="test",
                    status_code=200, url_requested="test", url_returned="test")

    assert x1.success
    assert not x2.success
    assert not x3.success
    assert x4.success
    print("Success!")


if __name__ == "__main__":
    main()
