
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
    empty_cart_text = WebElement(WebPage, css_selector = 'form#basket-step1-default span.g-alttext-small.g-alttext-grey.g-alttext-head')  # сообщение "Ваша корзина пуста"
    go_to_checkout_button = WebElement(WebPage, css_selector = 'button.btn.btn-primary.btn-large.fright.start-checkout-js') # кнопка "Перейти к оформлению"
    item_reduction_button = WebElement(WebPage, css_selector = 'div.product-operations span.btn.btn-lessen.btn-lessen-cart') # кнопка минус
    item_increase_button = WebElement(WebPage, css_selector = 'div.product-operations span.btn.btn-increase.btn-increase-cart') # кнопка плюс
    goods_quantity_input = WebElement(WebPage, css_selector = 'input.quantity')

    empty_cart_button = WebElement(WebPage, css_selector = 'div.text-regular.empty-basket-link a') # кнопка "Очистить корзину"