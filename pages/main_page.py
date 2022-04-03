
import os, pickle
import time

import pytest
from selenium.webdriver.chrome import webdriver

from pages.web_page import WebPage
from pages.web_element import WebElement
from pages.web_element import ManyWebElements
from settings import project_url
from pages.search_result_page import SearchResultPage


class MainPage(WebPage):
    def __init__(self, driver, url=''):
        if not url:
            url = os.getenv("MAIN_URL") or project_url
        super().__init__(driver, url)

    # шапка страницы
    logo = WebElement(WebPage, css_selector='a.b-header-b-logo-e-logo-wrap') # логотип со ссылкой на главную страницу
    main_cabinet = WebElement(WebPage, css_selector='.top-link-main_cabinet') # кнопка "Мой Лаб"
    user_name = WebElement(WebPage, css_selector='span.js-b-autofade-text')  # имя пользователя в шапке страницы
    sear_field = WebElement(WebPage, id='search-field')  # поле поиска
    sear_button = WebElement(WebPage, css_selector='button.b-header-b-search-e-btn')  # кнопка Искать
    favorite = WebElement(WebPage, link_text = 'Отложено') # кнопка Отложено
    favorites_counter = WebElement(WebPage, css_selector = 'div.top-header span.b-header-b-personal-e-icon-count-m-putorder.basket-in-dreambox-a') # количесвто отложенных товаров
    cart = WebElement(WebPage, css_selector='.top-header a[href="/cart/"]') # кнопка Корзина
    cart_counter = WebElement(WebPage, css_selector = 'div.top-header span.b-header-b-personal-e-icon-count-m-cart.basket-in-cart-a') # количесвто товаров в корзине

    # модальная страница для авторизации
    find_login = WebElement(WebPage, css_selector='.full-input__input.formvalidate-error')  # поле для ввода логина (тел, емэйл, код скидки)
    login_error_message = WebElement(WebPage, css_selector='form#auth-by-code small.full-input__msg-small.js-msg-small')  # сообщение под полем ввода логина
    input_button = WebElement(WebPage, id='g-recap-0-btn')  # кнопка "Войти"
    login_option = WebElement(WebPage, link_text='Другие способы входа') # кнопка 'Другие способы входа'
    yandex_login_button = WebElement(WebPage, css_selector='a[title="Яндекс"]') # кнопка "Я"

    # модальная страница успешной авторизации
    success_login = WebElement(WebPage, css_selector = 'form#auth-success-login div.js-auth__title.new-auth__title')

    # элементы страницы passport.yandex.ru для авторизации
    yandex_login_input = WebElement(WebPage, css_selector='input#passp-field-login') # поле для ввода логина
    yandex_next_button0 = WebElement(WebPage, id='passp:sign-in') # кнопка "Войти"
    yandex_password_input = WebElement(WebPage, id='passp-field-passwd') # поле для ввода пароля
    yandex_next_button1 = WebElement(WebPage, id='passp:sign-in') # кнопка "Войти"


    # модальное окно при добавлении книги в Отложено
    add_to_favorite_popup = WebElement(WebPage, css_selector = 'div.b-basket-popinfo-e-text.b-basket-popinfo-e-text-m-add.b-basket-popinfo-e-text-m-gray')

    # модальное окно при добавлении книги в Корзину
    add_to_cart_popup = WebElement(WebPage, css_selector = 'div.b-basket-popinfo-e-text.b-basket-popinfo-e-text-m-add.b-basket-popinfo-e-text-m-gray')

    # модальное окно с кнопкой "Принять"
    accept_cookie = WebElement(WebPage, css_selector = 'button.cookie-policy__button.js-cookie-policy-agree')

    def get_first_book_by_name(self, book_name): # первая найденная книга по названию
        self.sear_field.wait_to_be_clickable()
        self.sear_field.send_keys(book_name)

        self.sear_button.wait_to_be_clickable()
        self.sear_button.click()
        self.wait_page_loaded()
        search_url = self.get_current_url()
        search_result_page = SearchResultPage(self._web_driver, search_url)
        search_result_page.book_name.wait_to_be_clickable()
        first_book_name = search_result_page.book_name
        first_book_author = search_result_page.book_author

        return first_book_name, first_book_author, search_result_page.add_to_favorite, search_result_page.add_to_cart
