# Description: Contains methods usefull to test a web app.
# Author: Sébastien Delsad
# Date: 2023-06-26

# Ignore too general except clause
# pylint: disable=W0703
# pylint: disable=C0103

from typing import Union, List, Tuple, Iterable
import time
import json
import requests
import urllib3
try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

from app_outcome import AppOutcome

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Create class from functions below
class AppInterface:
    """ Class that contains methods usefull to test a web app. """

    def __init__(self, base_url: str, timeout: int = 10):
        """ Initializes the class. """
        self.s = requests.Session()

        self.timeout = timeout
        self.BASE_URL = base_url

    def simple_get(self, endpoint: str) -> List[AppOutcome]:
        ''' Makes a GET request to the specified URL.
        :param endpoint: Endpoint to make the request to (e.g. / or /account)
        :return: A tuple (success, body) where success is True if the request was successful, False otherwise, and body is the body of the response
        '''
        st = time.time()
        try:
            response = self.s.get(self.BASE_URL + endpoint,
                                  timeout=self.timeout, verify=False)

            return [AppOutcome.from_response(time.time() - st, endpoint, response)]

        except Exception as e:
            # Return false and info about exception
            return [AppOutcome.from_exception(time.time() - st, endpoint, e)]

    def simple_post(self, endpoint, data) -> List[AppOutcome]:
        ''' Makes a POST request to the specified URL.
        :param endpoint: Endpoint to make the request to (e.g. / or /account)
        :param data: Data to send in the POST request (e.g. {"username": "test", "password": "test"})
        :return: A tuple (success, body) where success is True if the request was successful, False otherwise, and body is the body of the response
        '''
        assert isinstance(data, dict), "Data must be a dictionary"

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        }

        st = time.time()
        try:
            response = self.s.post(self.BASE_URL + endpoint, data=data,
                                   timeout=self.timeout, verify=False, headers=headers)

            return [AppOutcome.from_response(time.time() - st, endpoint, response)]

        except Exception as e:
            return [AppOutcome.from_exception(time.time() - st, endpoint, e)]

    def get_token_and_post(self, token_endpoint, post_endpoint, data) -> List[AppOutcome]:
        ''' Makes a POST request to the specified URL.
        :param token_endpoint: Endpoint to make the request to to get the token (e.g. / or /account)
        :param post_endpoint: Endpoint to make the request to (e.g. / or /account)
        :param data: Data to send in the POST request (e.g. {"username": "test", "password": "test"})
        :return: A tuple (success, body) where success is True if the request was successful, False otherwise, and body is the body of the response
        '''
        assert isinstance(data, dict), "Data must be a dictionary"

        # Get page with token
        outcome_get = self.simple_get(token_endpoint)
        if not all(outcome.success for outcome in outcome_get):
            return [outcome_get]

        # Get token
        soup = BeautifulSoup(outcome_get[-1].body, "html.parser")
        try:
            token = soup.find("input", {"name": "__RequestVerificationToken"})[
                "value"]
        except Exception as e:
            return [AppOutcome.from_exception(sum(o.time for o in outcome_get), token_endpoint, e)]

        # Post
        outcome_post = self.simple_post(
            post_endpoint, {"__RequestVerificationToken": token, **data})

        return outcome_get + outcome_post

    def __del__(self):
        ''' Destructor. '''
        self.s.close()


def main():
    ''' Main function. '''
    # Get credentials
    with open("config.json", "r", encoding='utf-8') as f:
        config = json.load(f)

    # Test
    o = AppInterface(config["base_url"])
    outcome = o.get_token_and_post(
        "/compte/connexion",
        "/compte/connexion",
        {"Input.Email": config["credentials"]["username"], "Input.Password": config["credentials"]["password"], "submit": ""})

    print(outcome)


# Launch main
if __name__ == "__main__":
    main()
