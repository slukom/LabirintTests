
import os, pickle

import pytest
from selenium.webdriver.chrome import webdriver

from pages.web_page import WebPage
from pages.web_element import WebElement
from pages.web_element import ManyWebElements
from settings import project_url


class MainPage(WebPage):
    def __init__(self, driver, url=''):
        if not url:
            url = os.getenv("MAIN_URL") or project_url
        super().__init__(driver, url)


    def get_logo(self):
        logo = WebElement(WebPage, css_selector='a.b-header-b-logo-e-logo-wrap')
        logo.wait_to_be_clickable()
        return logo

    main_cabinet = WebElement(WebPage, css_selector='.top-link-main_cabinet')
    login_option = WebElement(WebPage, link_text='Другие способы входа')
    yandex_login_button = WebElement(WebPage, css_selector='a[title="Яндекс"]')
    yandex_login_input = WebElement(WebPage, css_selector='input#passp-field-login')
    yandex_next_button0 = WebElement(WebPage, id='passp:sign-in')
    yandex_password_input = WebElement(WebPage, id='passp-field-passwd')
    yandex_next_button1 = WebElement(WebPage, id='passp:sign-in')
    user_name = WebElement(WebPage, css_selector='span.js-b-autofade-text')

    find_login = WebElement(WebPage, css_selector='.full-input__input.formvalidate-error')
    login_error_message = WebElement(WebPage, css_selector='form#auth-by-code small.full-input__msg-small.js-msg-small')
    input_button = WebElement(WebPage, id='g-recap-0-btn')

    sear_field = WebElement(WebPage, id='search-field')
    sear_button = WebElement(WebPage, css_selector='button.b-header-b-search-e-btn')

    authors_link = WebElement(WebPage, css_selector='a[data-id_tab="1"]')
    search_result = WebElement(WebPage, css_selector='a.rubric-list-item')

    search_author = WebElement(WebPage, css_selector='div.content-default.read-area h1')

    book = WebElement(WebPage, css_selector='span.product-title')

    not_found_issue = WebElement(WebPage, css_selector = 'div.search-error h1')






