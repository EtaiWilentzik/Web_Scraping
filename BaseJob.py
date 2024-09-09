import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import certifi


class BaseJob(ABC):
    def __init__(self, url=""):
        self.url = url

    def next_page(self, page_number):
        header = self.get_headers()
        url = self.url.format(page_number=page_number)

        # print("URL: ", url)
        response = requests.get(url, headers=header, verify=certifi.where())
        soup = BeautifulSoup(response.text, "html.parser")
        # print("+====================++====================++====================+")
        # print("Page number: ", page_number)
        return soup

    @abstractmethod
    def read_page(self, soup, job_list, optional_names):
        pass

    @staticmethod
    def get_headers():
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        }
