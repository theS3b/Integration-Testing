# Description: Contains methods usefull to test a web app.
# Author: Sébastien Delsad
# Date: 2023-06-26

# Ignore too general except clause
# pylint: disable=W0703
# pylint: disable=C0103

import json
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup


# Create class from functions below
class AppInterface:
    """ Class that contains methods usefull to test a web app. """
    def __init__(self, base_url, timeout = 5):
        """ Initializes the class. """
        self.s = requests.Session()
        
        self.timeout = timeout
        self.BASE_URL = base_url
        self.OK_CODE = 200

    def simple_get(self, endpoint):
        ''' Makes a GET request to the specified URL.
        :param endpoint: Endpoint to make the request to (e.g. / or /account)
        :return: A tuple (success, body) where success is True if the request was successful, False otherwise, and body is the body of the response
        '''
        try:
            response = self.s.get(self.BASE_URL + endpoint, timeout=self.timeout, verify=False)
            return response.status_code == self.OK_CODE, response
        except Exception as e:
            # Return false and info about exception
            return False, str(e)

    def simple_post(self, endpoint, data):
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

        try:
            response = self.s.post(self.BASE_URL + endpoint, data = data, timeout=self.timeout, verify=False, headers = headers)
            if response.status_code != self.OK_CODE:
                return False, response.text + "\n" + response.reason + "\n" + response.url + "\n" + str(response.status_code)
            
            return True, response

        except Exception as e:
            return False, str(e)

    def get_token_and_post(self, token_endpoint, post_endpoint, data):
        ''' Makes a POST request to the specified URL.
        :param token_endpoint: Endpoint to make the request to to get the token (e.g. / or /account)
        :param post_endpoint: Endpoint to make the request to (e.g. / or /account)
        :param data: Data to send in the POST request (e.g. {"username": "test", "password": "test"})
        :return: A tuple (success, body) where success is True if the request was successful, False otherwise, and body is the body of the response
        '''
        assert isinstance(data, dict), "Data must be a dictionary"

        # Get page with token
        success, response = self.simple_get(token_endpoint)
        if not success:
            return False, response

        # Get token
        soup = BeautifulSoup(response.text, "html.parser")
        try:
            token = soup.find("input", {"name": "__RequestVerificationToken"})["value"]
        except Exception as e:
            return False, str(e)

        # Post
        return self.simple_post(post_endpoint, {"__RequestVerificationToken": token, **data})

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
    success, body = o.get_token_and_post(
        "/compte/connexion",
        "/compte/connexion", 
        {"Input.Email": config["credentials"]["username"], "Input.Password": config["credentials"]["password"], "submit": ""})
    print (success)
    print (body)


    
# Launch main
if __name__ == "__main__":
    main()