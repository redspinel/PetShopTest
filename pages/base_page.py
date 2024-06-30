# pages/base_page.py

import requests
from config.config import BASE_URL

class BasePage:
    def __init__(self):
        self.base_url = BASE_URL

    def get(self, endpoint, headers=None, params=None):
        response = requests.get(f"{self.base_url}{endpoint}", headers=headers, params=params)
        return response

    def post(self, endpoint, headers=None, data=None):
        response = requests.post(f"{self.base_url}{endpoint}", headers=headers, json=data)
        return response

    def put(self, endpoint, headers=None, data=None):
        response = requests.put(f"{self.base_url}{endpoint}", headers=headers, json=data)
        return response

    def delete(self, endpoint, headers=None):
        response = requests.delete(f"{self.base_url}{endpoint}", headers=headers)
        return response