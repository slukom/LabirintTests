
import os, pickle

import pytest
from selenium.webdriver.chrome import webdriver

from pages.web_page import WebPage
from pages.web_element import WebElement
from pages.web_element import ManyWebElements
from settings import project_url


class SearchPage(WebPage):
    def __init__(self, driver, url='', search_query = ''):
        if not url:
            url = os.getenv("SEARCH_URL") or project_url + 'search/' + search_query + '/?stype=0'
        super().__init__(driver, url)
