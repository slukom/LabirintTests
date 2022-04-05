import time

import pytest
from selenium.webdriver.common.alert import Alert

from pages.main_page import MainPage
from pages.about_book_page import AboutBookPage
from pages.about_author_page import AboutAuthorPage
from pages.search_result_page import SearchResultPage
from pages.favorites_page import FavoritesPage
from pages.cart_page import CartPage
from pages.compare_page import ComparetPage
from settings import valid_email, valid_password
from selenium.webdriver.common.alert import Alert
from settings import project_url, discount_code, login


# test1 Проверка авторизация на сайте с помощью учетки Яндекс (!)
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

    assert page.user_name.get_text() == login


# test2 Авторизация по корректному коду скидки
@pytest.mark.positive
def test_login_with_code(driver):
    page = MainPage(driver)
    page.main_cabinet.click()
    page.login_option.click()

    page.find_login.send_keys(discount_code)
    page.input_button.click()

    #page.success_login.wait_to_be_clickable()
    #print('\nlogin = ',page.success_login.get_text())
    # проверяем, что на модальной форме об успешной авторизации есть приветственный текст
    #assert f'Здравствуйте, {login}' in page.success_login.get_text()
    page.wait_page_loaded()
    page.user_name.wait_to_be_clickable()
    #time.sleep(6) # таймер ожидания закрытия модальной формы, после которой появляется имя пользователя в шапке сайта
    # проверяем, что в шапке сайта появилось имя авторизаванного пользователя
    assert page.user_name.get_text() == login


# test3 Проверка ошибки валидации логина при вводе некорректного символа
@pytest.mark.negative
@pytest.mark.parametrize("invalid_symbol", [' ', '!', '#', '$'], ids=['space', '!', '#', '$'])
def test_login_with_invalid_symbol(driver, invalid_symbol):
    page = MainPage(driver)

    page.main_cabinet.click()

    page.find_login.send_keys(invalid_symbol)

    time.sleep(2)
    assert page.login_error_message.get_text() == f"Нельзя использовать символ «{invalid_symbol}»"


# test4 Проверка валидации логина при вводе некорректного кода
@pytest.mark.negative
def test_login_with_invalid_code(driver):
    page = MainPage(driver)

    page.main_cabinet.click()

    page.find_login.send_keys('fffffffffffff')

    page.input_button.click()

    time.sleep(2)
    assert page.login_error_message.get_text() == "Введенного кода не существует"


# test5 Проверка валидации логина при вводе некорректного номера телефона
@pytest.mark.negative
def test_login_with_invalid_tel_number(driver):
    page = MainPage(driver)

    page.main_cabinet.click()

    page.find_login.send_keys('9999999999')

    page.input_button.click()

    time.sleep(2)
    assert page.login_error_message.get_text() == "Неверный формат телефона"


# test6 Проверка поиска по автору
@pytest.mark.positive
def test_search_by_author(driver):
    search_query = "Александр Сергеевич Пушкин"
    page = MainPage(driver)

    page.sear_field.send_keys(search_query)

    page.sear_button.click()
    page.wait_page_loaded()
    search_result_page = SearchResultPage(driver, page.get_current_url())
    search_result_page.wait_page_loaded()
    search_result_page.authors_link.click()

    search_result_page.found_author.click()
    about_author_page = AboutAuthorPage(driver, page.get_current_url())
    about_author_page.author_name.wait_to_be_clickable()
    assert about_author_page.author_name.get_text() == search_query


# test7 переход на главную страницу со страницы просмотра информации об авторе
@pytest.mark.positive
def test_go_to_main_page_from_author_page(driver):
    search_query = "Александр Сергеевич Пушкин"
    page = MainPage(driver)
    page.sear_field.send_keys(search_query)
    page.sear_button.click()
    page.wait_page_loaded()
    search_result_page = SearchResultPage(driver, page.get_current_url())
    search_result_page.authors_link.wait_to_be_clickable()
    search_result_page.authors_link.click()
    search_result_page.search_result.click()

    page.logo.wait_to_be_clickable()
    page.logo.click()

    assert page.get_current_url() == project_url


# test8 Проверка поиска по названию книги
@pytest.mark.positive
def test_search_by_book(driver):
    search_query = "Капитанская дочка"
    page = MainPage(driver)
    book_name, _, _, _ = page.get_first_book_by_name(search_query)
    assert search_query in book_name.get_text()


# test9 переход на главную страницу со страницы поиска
@pytest.mark.positive
def test_go_to_main_page_from_search_page(driver):
    search_query = "Капитанская дочка"
    page = MainPage(driver)
    page.get_first_book_by_name(search_query)

    page.logo.wait_to_be_clickable()
    page.logo.click()

    assert page.get_current_url() == project_url


# test10 Поиск книги по ISBN
@pytest.mark.positive
def test_search_by_ISBN(driver):
    search_query = "978-5-9287-3324-7"
    page = MainPage(driver)
    book_name, _, _, _ = page.get_first_book_by_name(search_query)
    assert "Капитанская дочка" in book_name.get_text()

    book_name.click()
    page.wait_page_loaded()
    about_book = AboutBookPage(driver, page.get_current_url())
    about_book.isbn.wait_to_be_clickable()
    assert search_query in about_book.isbn.get_text()


# test11 Проверка поиска по невалидному запросу
@pytest.mark.negative
def test_invalid_search(driver):
    search_query = "йййййййййййй"
    page = MainPage(driver)

    page.sear_field.send_keys(search_query)
    page.sear_button.click()
    page.wait_page_loaded()
    search_result_page = SearchResultPage(driver, page.get_current_url())
    search_result_page.not_found_issue.wait_to_be_clickable()
    assert search_result_page.not_found_issue.get_text() == 'Мы ничего не нашли по вашему запросу! Что делать?'


# test12 Заходим на страницу Отложенные и проверяем, что отложенных товаров нет
@pytest.mark.positive
def test_no_favorite(driver):
    page = MainPage(driver)
    page.favorite.click()
    page.wait_page_loaded()
    favorites_page = FavoritesPage(driver)
    favorites_page.no_favorite_goods.wait_to_be_clickable()
    assert 'Отложите интересные вам товары' in favorites_page.no_favorite_goods.get_text()


# test13 переход на главную страницу со страницы "Отложенные товары"
@pytest.mark.positive
def test_go_to_main_page_from_favorite(driver):
    search_query = "Капитанская дочка"
    page = MainPage(driver)
    page.favorite.click()

    page.logo.wait_to_be_clickable()
    page.logo.click()

    assert page.get_current_url() == project_url


# test14 Добавление в отложенное со страницы поиска
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


# test15 Удаление из отложенного со страницы поиска
@pytest.mark.positive
def test_delete_from_favorite(driver):
    search_query = "Капитанская дочка"
    page = MainPage(driver)

    _, _, add_to_favorite, _ = page.get_first_book_by_name(search_query) # находим кнопку-сердечко
    page.wait_page_loaded()
    search_result_page = SearchResultPage(driver, page.get_current_url())
    add_to_favorite.wait_to_be_clickable()
    add_to_favorite.click()  # нажимаем на кнопку-сердечко, чтобы добавить в избранное
    add_to_favorite.click()  # нажимаем повторно для вызова контекстного меню
    search_result_page.delete_from_favorite.wait_to_be_clickable()
    search_result_page.delete_from_favorite.click() # нажимаем на вторую кнопку в меню

    page.favorites_counter.wait_to_be_clickable()
    favorites_counter = int(page.favorites_counter.get_text())

    assert favorites_counter == 0


# test16 Удаление из отложенного со страницы "Отложенные товары" по нажатию на кнопку "Очистить"
@pytest.mark.positive
def test_clear_favorite(driver):
    search_query = "Капитанская дочка"
    page = MainPage(driver)

    _, _, add_to_favorite, _ = page.get_first_book_by_name(search_query)  # находим кнопку-сердечко
    add_to_favorite.click()  # нажимаем на кнопку-сердечко, чтобы добавить в избранное
    page.favorites_counter.click()
    page.wait_page_loaded()
    favorite_page = FavoritesPage(driver, page.get_current_url())
    favorite_page.clear_favorite.wait_to_be_clickable()
    favorite_page.clear_favorite.click()
    alert = Alert(driver) # создаем объект оповещения
    alert.accept() # нажимаем на кнпоку "Ок" на окне оповещения

    # проверяем, что после очистки отложенных товаров отображается сообщение 'Выбранные товары удалены!'
    favorite_page.message.wait_to_be_clickable()
    assert favorite_page.message.get_text() == 'Выбранные товары удалены!'


# test17 Заходим в Корзину и проверяем, что нет товаров в корзине
@pytest.mark.positive
def test_empty_cart(driver):
    page = MainPage(driver)
    page.cart.wait_to_be_clickable()
    page.cart.click()
    page.wait_page_loaded()
    cart_page = CartPage(driver, page.get_current_url())
    cart_page.empty_cart.wait_to_be_clickable()

    assert 'ВАША КОРЗИНА ПУСТА. ПОЧЕМУ?' in cart_page.empty_cart.get_text()


# test18 переход на главную страницу со страницы "Корзина"
@pytest.mark.positive
def test_go_to_main_page_from_cart(driver):
    search_query = "Капитанская дочка"
    page = MainPage(driver)
    page.cart.click()
    page.logo.wait_to_be_clickable()
    page.logo.click()

    assert page.get_current_url() == project_url


# test19 Добавление в корзину первую найденную книгу
@pytest.mark.positive
def test_add_to_cart(driver):
    search_query = "Капитанская дочка"
    page = MainPage(driver)

    _, _, _, add_to_cart = page.get_first_book_by_name(search_query)
    add_to_cart.click()
    page.add_to_cart_popup.wait_to_be_clickable()
    # проверяем, что появилось сообщение об успешном добавлении в корзину
    assert 'Вы добавили в корзину книгу' in page.add_to_cart_popup.get_text()

    page.cart_counter.wait_to_be_clickable()
    # time.sleep(2)
    cart_counter = int(page.cart_counter.get_text())
    # проверяем, что счетчик товаров в корзине увеличился
    assert cart_counter > 0


# test20 Добавление в корзину со страницы просмотра книги
@pytest.mark.positive
def test_add_to_cart_from_book_page(driver):
    search_query = "Капитанская дочка"
    page = MainPage(driver)
    page.accept_cookie.click()
    name_found_book, _, _, add_to_cart = page.get_first_book_by_name(search_query)
    name_found_book.click()
    page.wait_page_loaded()
    about_book_page = AboutBookPage(driver, page.get_current_url())
    about_book_page.add_to_cart.wait_to_be_clickable()
    about_book_page.add_to_cart.click()
    # проверяем, что название кнопки изменилось
    assert about_book_page.add_to_cart.get_text() == 'Оформить заказ'

    page.cart_counter.wait_to_be_clickable()
    time.sleep(3)
    cart_counter = int(page.cart_counter.get_text())
    # проверяем, что счетчик увеличился
    assert cart_counter > 0
    time.sleep(3)
    page.add_to_cart_popup.wait_to_be_clickable()
    assert 'Вы добавили в корзину книгу' in page.add_to_cart_popup.get_text()


# test21 Добавить в сравнение
def test_add_to_compare(driver):
    page = MainPage(driver)
    page.accept_cookie.click()
    page.open_actions_block.click()
    page.add_to_compare.wait_to_be_clickable()
    page.add_to_compare.click()
    page.wait_page_loaded()
    # проверяем, название пункта меню меняется на текст 'Перейти к сравнению'
    assert 'Перейти к сравнению' in page.add_to_compare.get_text()


# test22 Удалить из сравнения
def test_delete_from_compare(driver):
    page = MainPage(driver)
    page.accept_cookie.click()
    page.open_actions_block.click()
    page.add_to_compare.wait_to_be_clickable()
    page.add_to_compare.click()
    page.wait_page_loaded()
    page.add_to_compare.click()
    page.wait_page_loaded()
    compare_page = ComparetPage(driver, page.get_current_url())
    compare_page.wait_page_loaded()
    compare_page.delete_compare_list_button.click()
    alert = Alert(driver)
    alert.accept()
    # проверяем, что после очищения сравнительного списка появляется текст 'Товаров нет. Добавьте хотя бы один товар, например, из раздела'
    assert 'Товаров нет. Добавьте хотя бы один товар, например, из раздела' in compare_page.empty_compare_text.get_text()

# test23 Получить купон по валидному email
# test24 Получить купон по невалидному email
# test25 Задать вопрос в поддержку
# test26 Отправить пустое сообщение в поддержку
# test27 Отправить очень длинное сообщение в поддержку
# test26 Успешный поиск по слову в своих сообщениях с поддержкой
# test28 Безрезультатный поиск по слову в своих сообщениях с поддержкой
# test29 Успешный поиск по слову в публичных сообщениях с поддержкой
# test30 Безрезультатный поиск по слову в публичных сообщениях с поддержкой
# test31 Переход на главную страницу со страницы поддержки
# test32 Переход в соц.сети
# test33 Переход на страницу Помощи
# test34 Переход на главную страницу со страницы Помощи
# test35 Успешный поиск по слову на странице Помощи
# test36 Безрезультатный поиск по слову на странице Помощи
# test21 Оформление покупки

# test22 Удаление из корзины




