
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

    # шапка страницы
    main_cabinet = WebElement(WebPage, css_selector='.top-link-main_cabinet') # кнопка "Мой Лаб"
    user_name = WebElement(WebPage, css_selector='span.js-b-autofade-text')  # имя пользователя в шапке страницы
    sear_field = WebElement(WebPage, id='search-field')  # поле поиска
    sear_button = WebElement(WebPage, css_selector='button.b-header-b-search-e-btn')  # кнопка Искать

    # модальная страница для авторизации
    find_login = WebElement(WebPage, css_selector='.full-input__input.formvalidate-error')  # поле для ввода логина (тел, емэйл, код скидки)
    login_error_message = WebElement(WebPage, css_selector='form#auth-by-code small.full-input__msg-small.js-msg-small')  # сообщение под полем ввода логина
    input_button = WebElement(WebPage, id='g-recap-0-btn')  # кнопка "Войти"
    login_option = WebElement(WebPage, link_text='Другие способы входа') # кнопка 'Другие способы входа'
    yandex_login_button = WebElement(WebPage, css_selector='a[title="Яндекс"]') # кнопка "Я"

    # элементы страницы passport.yandex.ru для авторизации
    yandex_login_input = WebElement(WebPage, css_selector='input#passp-field-login') # поле для ввода логина
    yandex_next_button0 = WebElement(WebPage, id='passp:sign-in') # кнопка "Войти"
    yandex_password_input = WebElement(WebPage, id='passp-field-passwd') # поле для ввода пароля
    yandex_next_button1 = WebElement(WebPage, id='passp:sign-in') # кнопка "Войти"


    # страница с результатами поиска (по умолчанию вкладка "Товары")
    authors_link = WebElement(WebPage, css_selector='a[data-id_tab="1"]') # вкладка "Авторы"
    search_result = WebElement(WebPage, css_selector='a.rubric-list-item') # первый автор в списке результатов

    # страница просмотра информации об авторе
    search_author = WebElement(WebPage, css_selector='div.content-default.read-area h1') # ФИО автора в заголовке

    # страница с результатами поиска (по умолчанию вкладка "Товары")
    book_name = WebElement(WebPage, css_selector='span.product-title') # имя первого найденного товара (название книги)
    book_author = WebElement(WebPage, css_selector='div.product-author > a > span') # имя автора первого найденного товара (автор книги)
    add_to_favorite = WebElement(WebPage, css_selector='.icon-fave.track-tooltip.js-open-deferred-block')  # кнопка "Отложить" у первого товара

    # страница с ненайденным результатом поиска
    not_found_issue = WebElement(WebPage, css_selector = 'div.search-error h1') # строка с сообщениемм 'Мы ничего не нашли по вашему запросу! Что делать?'

"""
    def get_first_book_by_name(self, book_name): #
        self.sear_field.wait_to_be_clickable()
        self.sear_field.send_keys(book_name)

        self.sear_button.wait_to_be_clickable()
        self.sear_button.click()

        self.book_name.wait_to_be_clickable()
        first_book_name = self.book_name
        first_book_author = self.book_author

        return first_book_name, first_book_author, self.add_to_favorite

"""


