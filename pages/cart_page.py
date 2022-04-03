
import os, pickle

import pytest
from selenium.webdriver.chrome import webdriver

from pages.web_page import WebPage
from pages.web_element import WebElement
from pages.web_element import ManyWebElements
from settings import cart_url

# страница "Корзина"
class CartPage(WebPage):
    def __init__(self, driver, url = ''):
        if not url:
            url = cart_url
        super().__init__(driver, url)

    # страница Корзина
    empty_cart = WebElement(WebPage, css_selector='form#basket-step1-default span.g-alttext-small.g-alttext-grey.g-alttext-head')  # сообщение "Ваша корзина пуста"