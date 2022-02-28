import time

import pytest

from pages.main_page import MainPage
from pages.web_element import WebElement
from settings import valid_email, valid_password, project_url


# test1 Проверка авторизация на сайте с помощью учетки Яндекс
@pytest.mark.positive
def test_login_with_yandex(driver):
    page = MainPage(driver)
    page.main_cabinet.wait_to_be_clickable()
    page.main_cabinet.click()

    page.login_option.wait_to_be_clickable()
    page.login_option.click()

    page.yandex_login_button.wait_to_be_clickable()
    page.yandex_login_button.click()

    page.yandex_login_input.wait_to_be_clickable()
    page.yandex_login_input.send_keys(valid_email)

    page.yandex_next_button0.wait_to_be_clickable()
    page.yandex_next_button0.click()

    page.yandex_password_input.wait_to_be_clickable()
    page.yandex_password_input.send_keys(valid_password)

    page.yandex_next_button1.wait_to_be_clickable()
    page.yandex_next_button1.click()

    page.user_name.wait_to_be_clickable()

    assert page.user_name.get_text() == 'Test'


# test2 Проверка ошибки валидации логина при вводе некорректного символа
@pytest.mark.negative
@pytest.mark.parametrize("invalid_symbol", [' ', '!', '#', '$'], ids=['space', '!', '#', '$'])
def test_login_with_invalid_symbol(driver, invalid_symbol):
    page = MainPage(driver)
    page.main_cabinet.wait_to_be_clickable()
    page.main_cabinet.click()

    page.find_login.wait_to_be_clickable()
    page.find_login.send_keys(invalid_symbol)

    time.sleep(2)
    assert page.login_error_message.get_text() == f"Нельзя использовать символ «{invalid_symbol}»"


# test3 Проверка валидации логина при вводе некорректного кода
@pytest.mark.negative
def test_login_with_invalid_value():
    page = MainPage(pytest.driver)
    page.main_cabinet.wait_to_be_clickable()
    page.main_cabinet.click()

    page.find_login.wait_to_be_clickable()
    page.find_login.send_keys('fffffffffffff')

    page.input_button.wait_to_be_clickable()
    page.input_button.click()

    time.sleep(2)
    assert page.login_error_message.get_text() == "Введенного кода не существует"


# test4 Проверка валидации логина при вводе некорректного номера телефона
@pytest.mark.negative
def test_login_with_invalid_value():
    page = MainPage(pytest.driver)
    page.main_cabinet.wait_to_be_clickable()
    page.main_cabinet.click()

    page.find_login.wait_to_be_clickable()
    page.find_login.send_keys('9999999999')

    page.input_button.wait_to_be_clickable()
    page.input_button.click()

    time.sleep(2)
    assert page.login_error_message.get_text() == "Неверный формат телефона"


# test5 Проверка поиска по автору
@pytest.mark.positive
def test_search_by_author(driver):
    search_query = "Александр Сергеевич Пушкин"
    page = MainPage(driver)
    page.sear_field.wait_to_be_clickable()
    page.sear_field.send_keys(search_query)

    page.sear_button.wait_to_be_clickable()
    page.sear_button.click()

    page.authors_link.wait_to_be_clickable()
    page.authors_link.click()

    page.search_result.wait_to_be_clickable()
    page.search_result.click()

    page.search_author.wait_to_be_clickable()

    assert page.search_author.get_text() == search_query


# test6 Проверка поиска по книге
@pytest.mark.positive
def test_search_by_book(driver):
    search_query = "Капитанская дочка"
    page = MainPage(driver)
    page.sear_field.wait_to_be_clickable()
    page.sear_field.send_keys(search_query)

    page.sear_button.wait_to_be_clickable()
    page.sear_button.click()

    page.book.wait_to_be_clickable()

    assert search_query in page.book.get_text()


# test7 Проверка поиска по невалидному запросу
@pytest.mark.negative
def test_search_by_book(driver):
    search_query = "йййййййййййй"
    page = MainPage(driver)
    page.sear_field.wait_to_be_clickable()
    page.sear_field.send_keys(search_query)

    page.sear_button.wait_to_be_clickable()
    page.sear_button.click()

    page.not_found_issue.wait_to_be_clickable()

    assert page.not_found_issue.get_text() == 'Мы ничего не нашли по вашему запросу! Что делать?'


# test8 Добавление в отложенное
    search_query = "Капитанская дочка"
    page = MainPage(driver)
    page.sear_field.wait_to_be_clickable()
    page.sear_field.send_keys(search_query)

    page.sear_button.wait_to_be_clickable()
    page.sear_button.click()

    #assert

# test9 Удаление из отложенного
# test10 Добавление в корзину
# test11 Удаление из корзины
# test12
# test13
# test14