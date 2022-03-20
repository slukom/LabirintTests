import time

import pytest
from selenium.webdriver.common.alert import Alert

from pages.main_page import MainPage
from settings import valid_email, valid_password
from selenium.webdriver.common.alert import Alert


# test1 Проверка авторизация на сайте с помощью учетки Яндекс
@pytest.mark.positive
def test_login_with_yandex(driver):
    page = MainPage(driver)
    page.main_cabinet.click()
    page.login_option.click()

    page.yandex_login_button.click()
    page.yandex_login_input.send_keys(valid_email)
    page.yandex_next_button0.click()
    page.yandex_password_input.send_keys(valid_password)
    page.yandex_next_button1.click()

    page.user_name.wait_to_be_clickable()

    assert page.user_name.get_text() == 'Test'


# test2 Проверка ошибки валидации логина при вводе некорректного символа
@pytest.mark.negative
@pytest.mark.parametrize("invalid_symbol", [' ', '!', '#', '$'], ids=['space', '!', '#', '$'])
def test_login_with_invalid_symbol(driver, invalid_symbol):
    page = MainPage(driver)

    page.main_cabinet.click()

    page.find_login.send_keys(invalid_symbol)

    time.sleep(2)
    assert page.login_error_message.get_text() == f"Нельзя использовать символ «{invalid_symbol}»"


# test3 Проверка валидации логина при вводе некорректного кода
@pytest.mark.negative
def test_login_with_invalid_code(driver):
    page = MainPage(driver)

    page.main_cabinet.click()

    page.find_login.send_keys('fffffffffffff')

    page.input_button.click()

    time.sleep(2)
    assert page.login_error_message.get_text() == "Введенного кода не существует"


# test4 Проверка валидации логина при вводе некорректного номера телефона
@pytest.mark.negative
def test_login_with_invalid_tel_number(driver):
    page = MainPage(driver)

    page.main_cabinet.click()

    page.find_login.send_keys('9999999999')

    page.input_button.click()

    time.sleep(2)
    assert page.login_error_message.get_text() == "Неверный формат телефона"


# test5 Проверка поиска по автору
@pytest.mark.positive
def test_search_by_author(driver):
    search_query = "Александр Сергеевич Пушкин"
    page = MainPage(driver)

    page.sear_field.send_keys(search_query)

    page.sear_button.click()
    page.authors_link.click()
    page.search_result.click()
    page.search_author.wait_to_be_clickable()
    assert page.search_author.get_text() == search_query


# test6 Проверка поиска по названию книги
@pytest.mark.positive
def test_search_by_book(driver):
    search_query = "Капитанская дочка"
    page = MainPage(driver)
    book_name, _, _, _ = page.get_first_book_by_name(search_query)
    assert search_query in book_name.get_text()


# test7 Проверка поиска по невалидному запросу
@pytest.mark.negative
def test_invalid_search(driver):
    search_query = "йййййййййййй"
    page = MainPage(driver)

    page.sear_field.send_keys(search_query)
    page.sear_button.click()

    page.not_found_issue.wait_to_be_clickable()
    assert page.not_found_issue.get_text() == 'Мы ничего не нашли по вашему запросу! Что делать?'


# test8 Заходим на страницу Отложенные и проверяем, что отложенных товаров нет
@pytest.mark.positive
def test_no_favorite(driver):
    page = MainPage(driver)
    page.favorite.click()
    page.no_favorite_goods.wait_to_be_clickable()
    assert 'Отложите интересные вам товары' in page.no_favorite_goods.get_text()


# test9 Добавление в отложенное со страницы поиска
@pytest.mark.positive
def test_add_to_favorite(driver):
    search_query = "Капитанская дочка"
    page = MainPage(driver)

    _, _, add_to_favorite, _ = page.get_first_book_by_name(search_query) # находим кнопку-сердечко
    add_to_favorite.click() # нажимаем на кнопку-сердечко, чтобы добавить в избранное

    page.favorites_counter.wait_to_be_clickable()
    favorites_counter = int(page.favorites_counter.get_text())
    assert favorites_counter > 0 # проверяем что счетчик не нулевой

    page.add_to_favorite_popup.wait_to_be_clickable()
    assert 'Вы добавили в отложенные книгу' in page.add_to_favorite_popup.get_text()


# test10 Удаление из отложенного со страницы поиска
@pytest.mark.positive
def test_delete_from_favorite(driver):
    search_query = "Капитанская дочка"
    page = MainPage(driver)

    _, _, add_to_favorite, _ = page.get_first_book_by_name(search_query) # находим кнопку-сердечко
    add_to_favorite.click() # нажимаем на кнопку-сердечко, чтобы добавить в избранное
    add_to_favorite.click() # нажимаем повторно для вызова контекстного меню
    page.delete_from_favorite.wait_to_be_clickable()
    page.delete_from_favorite.click() # нажимаем на вторую кнопку в меню

    page.favorites_counter.wait_to_be_clickable()
    favorites_counter = int(page.favorites_counter.get_text())
    assert favorites_counter == 0


# test11 Удаление из отложенного со страницы "Отложенные товары" по нажатию на кнопку "Очистить"
@pytest.mark.positive
def test_clear_favorite(driver):
    search_query = "Капитанская дочка"
    page = MainPage(driver)

    _, _, add_to_favorite, _ = page.get_first_book_by_name(search_query)  # находим кнопку-сердечко
    add_to_favorite.click()  # нажимаем на кнопку-сердечко, чтобы добавить в избранное
    page.favorites_counter.click()
    page.clear_favorite.click()
    alert = Alert(driver) # создаем объект оповещения
    alert.accept() # нажимаем на кнпоку "Ок" на окне оповещения

    # проверяем, что после очистки отложенных товаров отображается сообщение 'Выбранные товары удалены!'
    page.message.wait_to_be_clickable()
    assert page.message.get_text() == 'Выбранные товары удалены!'


# test12 Заходим в Корзину и проверяем, что нет товаров в корзине
@pytest.mark.positive
def test_empty_cart(driver):
    page = MainPage(driver)
    page.cart.wait_to_be_clickable()
    page.cart.click()
    page.empty_cart.wait_to_be_clickable()

    assert 'ВАША КОРЗИНА ПУСТА. ПОЧЕМУ?' in page.empty_cart.get_text()


# test13 Добавление в корзину
@pytest.mark.positive
def test_add_to_cart(driver):
    search_query = "Капитанская дочка"
    page = MainPage(driver)

    _, _, _, add_to_cart = page.get_first_book_by_name(search_query)
    add_to_cart.click()

    page.cart_counter.wait_to_be_clickable()
    cart_counter = int(page.cart_counter.get_text())

    assert cart_counter > 0

    page.add_to_cart_popup.wait_to_be_clickable()
    assert 'Вы добавили в корзину книгу' in page.add_to_cart_popup.get_text()

# test14 Удаление из корзины
# test15 Добавить в сравнение
# test16 Удалить из сравнения
# test17
