from locust import HttpUser, task
import requests
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

class HelloWorldUser(HttpUser):
    def on_start(self):
        # Ignore self-signed certificate errors
        self.client.verify = False
        

    @task
    def hello_world(self):
        self.client.get("/")
        self.client.get("/compte/connexion")