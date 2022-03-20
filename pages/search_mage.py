
import os, pickle

import pytest
from selenium.webdriver.chrome import webdriver

from pages.web_page import WebPage
from pages.web_element import WebElement
from pages.web_element import ManyWebElements
from settings import project_url


class SearchPage(WebPage):
    def __init__(self, driver, url=''):
        if not url:
            url = os.getenv("MAIN_URL") or project_url
        super().__init__(driver, url)


    def get_logo(self):
        logo = WebElement(WebPage, css_selector='a.b-header-b-logo-e-logo-wrap')
        logo.wait_to_be_clickable()
        return logo