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
from pages.support_page import SupportPage
from pages.help_page import HelpPage
from pages.checkout_page import CheckoutPage
from settings import valid_email, valid_password, valid_phone
from settings import project_url, discount_code, login, social_network
from selenium.webdriver.common.action_chains import ActionChains


def generate_string(num):
    return "x" * num

def russian_chars():
    return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

def chinese_chars():
    return '的一是不了人我在有他这为之大来以个中上们'

def special_chars():
    return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'


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

    assert page.user_name.get_text() == login


# test2 Авторизация по корректному коду скидки
@pytest.mark.positive
def test_login_with_code(driver):
    page = MainPage(driver)
    page.main_cabinet.click()
    page.login_option.click()

    page.find_login.send_keys(discount_code)
    page.input_button.click()

    page.wait_page_loaded()
    page.user_name.wait_to_be_clickable()
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

    page.search_field.send_keys(search_query)

    page.search_button.click()
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
    page.search_field.send_keys(search_query)
    page.search_button.click()
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

    page.search_field.send_keys(search_query)
    page.search_button.click()
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
    cart_page.empty_cart_text.wait_to_be_clickable()

    assert 'ВАША КОРЗИНА ПУСТА. ПОЧЕМУ?' in cart_page.empty_cart_text.get_text()


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
    time.sleep(2)
    alert.accept()
    # проверяем, что после очищения сравнительного списка появляется текст 'Товаров нет. Добавьте хотя бы один товар, например, из раздела'
    assert 'Товаров нет. Добавьте хотя бы один товар, например, из раздела' in compare_page.empty_compare_text.get_text()


# test23 переход на главную страницу со страницы "Сравнение товаров"
@pytest.mark.positive
def test_go_to_main_page_from_compare(driver):
    page = MainPage(driver)
    page.accept_cookie.click()
    page.open_actions_block.click()
    page.add_to_compare.wait_to_be_clickable()
    page.add_to_compare.click()
    page.wait_page_loaded()
    page.add_to_compare.click()
    page.wait_page_loaded()
    page.logo.click()
    # проверяем, что вернулись на главную страницу
    assert page.get_current_url() == project_url


# test24 Получить купон по валидному зарегистрированному ранее email
@pytest.mark.positive
def test_get_coupon_by_used_valid_email(driver):
    page = MainPage(driver)
    page.input_email.send_keys(valid_email)
    page.get_coupon_button.wait_to_be_clickable()
    page.get_coupon_button.click()
    # проверяем, что выводится сообщение 'Адрес электронной почты уже используется'
    assert 'Адрес электронной почты уже используется' in page.get_email_is_in_use_text()


# test25 Получить купон по невалидному email
@pytest.mark.negative
def test_get_coupon_by_invalid_email(driver):
    page = MainPage(driver)
    page.input_email.send_keys('q@q.q')
    page.get_coupon_button.wait_to_be_clickable()
    page.get_coupon_button.click()
    # проверяем, что выводится сообщение 'Укажите почту'
    assert 'Укажите почту' in page.get_email_is_in_use_text()


# test26 Получить купон по незарегистрированному валидному email
@pytest.mark.positive
def test_get_coupon_by_new_valid_email(driver):
    page = MainPage(driver)
    page.input_email.send_keys(f'test{time.time()}@test.test')
    page.get_coupon_button.wait_to_be_clickable()
    page.get_coupon_button.click()
    page.received_coupon_popup.wait_to_be_clickable()
    # проверяем, что выводится сообщение о получении купона
    assert 'Купон на 50 р.' in page.received_coupon_popup.get_text()


# test27 Задать вопрос в поддержку
@pytest.mark.positive
def test_ask_support(driver):
    message_for_support = 'test message'
    page = MainPage(driver)
    page.support_link.click()
    page.wait_page_loaded()
    support_page = SupportPage(driver, page.get_current_url())
    support_page.ask_support_button.wait_to_be_clickable()
    support_page.ask_support_button.click()
    support_page.find_login.wait_to_be_clickable()
    support_page.find_login.send_keys(discount_code)
    support_page.input_button.click()

    support_page.textarea_for_question.send_keys(message_for_support)
    support_page.send_question_button.click()
    support_page.wait_page_loaded()
    assert message_for_support in support_page.posted_question.get_text()


# test28 Отправить пустое сообщение в поддержку
@pytest.mark.negative
def test_send_empty_message_to_support(driver):
    message_for_support = ''
    support_page = SupportPage(driver)
    support_page.ask_support_button.wait_to_be_clickable()
    support_page.ask_support_button.click()
    support_page.find_login.wait_to_be_clickable()
    support_page.find_login.send_keys(discount_code)
    support_page.input_button.click()
    support_page.textarea_for_question.send_keys(message_for_support)

    support_page.send_question_button.click()
    support_page.send_question_button.click()

    support_page.wait_page_loaded()
    # проверяем что не удалось отправить сообщение
    assert 'Переписки отсутствуют :(' == support_page.no_correspondence_text.get_text()


# test29 Успешный поиск по слову в своих сообщениях с поддержкой
@pytest.mark.positive
def test_success_search_in_my_messages(driver):
    message_for_support = 'test message'
    search_request = 'test'
    support_page = SupportPage(driver)
    support_page.ask_support_button.wait_to_be_clickable()
    support_page.ask_support_button.click()
    support_page.find_login.wait_to_be_clickable()
    support_page.find_login.send_keys(discount_code)
    support_page.input_button.click()

    support_page.textarea_for_question.send_keys(message_for_support)
    support_page.send_question_button.click()
    support_page.wait_page_loaded()
    support_page.my_question_link.click()

    support_page.search_here_input.send_keys(search_request)
    support_page.submit_request_button.click()
    support_page.wait_page_loaded()
    # проверяем что в найденных сообщениях содержится искомое слово
    assert search_request in support_page.found_message.get_text()


# test30 Безрезультатный поиск по слову в своих сообщениях с поддержкой
@pytest.mark.negative
def test_unsuccessful_search_in_my_messages(driver):
    search_request = 'zzzzzz'
    support_page = SupportPage(driver)
    support_page.my_question_link.click()
    support_page.find_login.wait_to_be_clickable()
    support_page.find_login.send_keys(discount_code)
    support_page.input_button.click()
    support_page.wait_page_loaded()
    support_page.search_here_input.send_keys(search_request)
    support_page.submit_request_button.click()
    support_page.wait_page_loaded()
    # проверяем что по найденному запросу сообщения не найдены
    assert 'Переписки отсутствуют :(' == support_page.no_correspondence_text.get_text()


# test31 Успешный поиск по слову в публичных сообщениях с поддержкой
@pytest.mark.positive
def test_success_search_in_public_messages(driver):
    search_request = 'доставк'
    support_page = SupportPage(driver)
    support_page.ask_support_button.wait_to_be_clickable()
    support_page.search_here_input.send_keys(search_request)
    support_page.submit_request_button.click()
    support_page.wait_page_loaded()
    # проверяем что в найденных сообщениях содержится искомое слово
    assert search_request in support_page.found_message.get_text()


# test32 Безрезультатный поиск по слову в публичных сообщениях с поддержкой
@pytest.mark.negative
def test_unsuccess_search_in_public_messages(driver):
    search_request = 'zzzzz'
    support_page = SupportPage(driver)
    support_page.ask_support_button.wait_to_be_clickable()
    support_page.search_here_input.send_keys(search_request)
    support_page.submit_request_button.click()
    support_page.wait_page_loaded()
    # проверяем что по найденному запросу сообщения не найдены
    assert 'Переписки отсутствуют' in support_page.not_found_messages_text.get_text()


# test33 Переход на главную страницу со страницы поддержки
@pytest.mark.negative
def test_go_to_main_page_form_support_page(driver):
    support_page = SupportPage(driver)
    support_page.logo.wait_to_be_clickable()
    support_page.logo.click()
    # проверяем что по нажатию на логотип происходит возврат на главную страницу
    assert support_page.get_current_url() == project_url


# test34 Оформление покупки
@pytest.mark.positive
def test_ordering(driver):
    page = MainPage(driver)
    page.accept_cookie.click()
    page.add_to_cart.click()
    page.wait_page_loaded()
    page.cart.click()
    cart_page = CartPage(driver, page.get_current_url())
    cart_page.wait_page_loaded()
    cart_page.go_to_checkout_button.click()
    cart_page.wait_page_loaded()
    checkout_page = CheckoutPage(driver, page.get_current_url())
    checkout_page.wait_page_loaded()
    assert 'Оформление заказа' in checkout_page.page_title.get_text()


# test35 Очистить корзину
@pytest.mark.positive
def test_clear_cart(driver):
    page = MainPage(driver)
    page.accept_cookie.click()
    page.add_to_cart.click()
    page.wait_page_loaded()
    page.cart.click()
    cart_page = CartPage(driver, page.get_current_url())
    cart_page.wait_page_loaded()
    cart_page.empty_cart_button.click()
    cart_page.wait_page_loaded()
    # проверяем, что после нажатия на кнопку "Очистить корзину" появляется сообщение 'ВАША КОРЗИНА ПУСТА. ПОЧЕМУ?'
    assert 'ВАША КОРЗИНА ПУСТА. ПОЧЕМУ?' in cart_page.empty_cart_text.get_text()


# test36 Увеличить количество товара в корзине
@pytest.mark.positive
def test_increase_num_of_items_in_cart(driver):
    page = MainPage(driver)
    page.accept_cookie.click()
    page.add_to_cart.click()
    page.wait_page_loaded()
    page.cart.click()
    cart_page = CartPage(driver, page.get_current_url())
    cart_page.wait_page_loaded()
    cart_page.item_increase_button.click()
    cart_page.wait_page_loaded()
    goods_quantity = int(cart_page.goods_quantity_input.get_attribute('value'))
    assert goods_quantity == 2


# test37 Увеличить, затем уменьшить количество товара в  корзине
@pytest.mark.positive
def test_increase_num_of_items_in_cart(driver):
    page = MainPage(driver)
    page.accept_cookie.click()
    page.add_to_cart.click()
    page.wait_page_loaded()
    page.cart.click()
    cart_page = CartPage(driver, page.get_current_url())
    cart_page.wait_page_loaded()
    cart_page.item_increase_button.click()
    cart_page.wait_page_loaded()
    cart_page.item_reduction_button.click()
    cart_page.wait_page_loaded()
    goods_quantity = int(cart_page.goods_quantity_input.get_attribute('value'))
    assert goods_quantity == 1


# test38 Оформление покупки, ввод пустых значений в поля с именем и фамилией
@pytest.mark.negative
@pytest.mark.parametrize("empty_value", ['', ' '], ids=['empty', 'space'])
def test_making_purchases_with_empty_data(driver, empty_value):
    page = MainPage(driver)
    page.accept_cookie.click()
    page.add_to_cart.click()
    page.cart.wait_to_be_clickable()
    page.cart.click()
    cart_page = CartPage(driver, page.get_current_url())
    cart_page.go_to_checkout_buttont.wait_to_be_clickable()
    cart_page.go_to_checkout_buttont.click()
    cart_page.wait_page_loaded()
    cart_page.name_input.send_keys(empty_value)
    cart_page.surname_input.send_keys(empty_value)
    cart_page.checkout_button.wait_to_be_clickable()
    cart_page.checkout_button.click()
    assert 'Имя обязательно' in cart_page.text_under_name_input.get_text()
    assert 'Фамилия обязательна' in cart_page.text_under_surname_input.get_text()


# test39 Оформление покупки, ввод невалидных значений в поля с именем и фамилией
@pytest.mark.negative
@pytest.mark.parametrize("invalid_value", ['1', special_chars(), chinese_chars()],
                         ids=['number', 'special_chars', 'chinese_chars'])
def test_making_purchases_with_empty_data(driver, invalid_value):
    page = MainPage(driver)
    page.accept_cookie.click()
    page.add_to_cart.click()
    page.cart.wait_to_be_clickable()
    page.cart.click()
    cart_page = CartPage(driver, page.get_current_url())
    cart_page.go_to_checkout_buttont.wait_to_be_clickable()
    cart_page.go_to_checkout_buttont.click()
    cart_page.wait_page_loaded()
    cart_page.name_input.send_keys(invalid_value)
    cart_page.surname_input.send_keys(invalid_value)
    cart_page.checkout_button.wait_to_be_clickable()
    cart_page.checkout_button.click()
    assert 'Разрешены только буквы' in cart_page.text_under_name_input.get_text()
    assert 'Разрешены только буквы' in cart_page.text_under_surname_input.get_text()


# test40 Оформление покупки, ввод длинных значений в поля с именем и фамилией
@pytest.mark.negative
def test_making_purchases_with_long_data(driver):
    long_text = generate_string(100)
    page = MainPage(driver)
    page.accept_cookie.click()
    page.add_to_cart.click()
    page.cart.wait_to_be_clickable()
    page.cart.click()
    cart_page = CartPage(driver, page.get_current_url())
    cart_page.go_to_checkout_buttont.wait_to_be_clickable()
    cart_page.go_to_checkout_buttont.click()
    cart_page.wait_page_loaded()
    cart_page.name_input.send_keys(long_text)
    cart_page.surname_input.send_keys(long_text)
    cart_page.checkout_button.wait_to_be_clickable()
    cart_page.checkout_button.click()
    assert 'Можно указать не более 50 символов' in cart_page.text_under_name_input.get_text()
    assert 'Можно указать не более 50 символов' in cart_page.text_under_surname_input.get_text()


# test41 Проверка ввода валидного зарегистрированного номера телефона
@pytest.mark.positive
def test_input_valid_phone_number(driver):
    phone = valid_phone
    page = MainPage(driver)
    page.accept_cookie.click()
    page.add_to_cart.click()
    page.cart.wait_to_be_clickable()
    page.cart.click()
    cart_page = CartPage(driver, page.get_current_url())
    cart_page.go_to_checkout_buttont.wait_to_be_clickable()
    cart_page.go_to_checkout_buttont.click()
    cart_page.wait_page_loaded()
    cart_page.phone_input.scroll_to_element()
    cart_page.phone_input.wait_to_be_clickable()

    element = cart_page.get_phone_input(driver)
    actions = ActionChains(driver)
    actions.move_to_element(element).send_keys(phone).perform()

    cart_page.checkout_button.wait_to_be_clickable()
    cart_page.checkout_button.click()
    assert 'Этот телефон уже есть в Лабиринте' in cart_page.text_under_phone_input.get_text()


# test42 Проверка ввода невалидного номера телефона
@pytest.mark.parametrize("invalid_phone", ['111', '+7111111111111', '++++++++', '----------', '()'],
                         ids=['short_num', 'long_num', 'pluses', 'minuses', 'brackets'])
@pytest.mark.negative
def test_input_invalid_phone_number(driver, invalid_phone):
    phone = invalid_phone
    page = MainPage(driver)
    page.accept_cookie.click()
    page.add_to_cart.click()
    page.cart.wait_to_be_clickable()
    page.cart.click()
    cart_page = CartPage(driver, page.get_current_url())
    cart_page.go_to_checkout_buttont.wait_to_be_clickable()
    cart_page.go_to_checkout_buttont.click()
    cart_page.wait_page_loaded()
    cart_page.phone_input.scroll_to_element()
    cart_page.phone_input.wait_to_be_clickable()

    element = cart_page.get_phone_input(driver)
    actions = ActionChains(driver)
    actions.move_to_element(element).send_keys(phone).perform()

    cart_page.checkout_button.wait_to_be_clickable()
    cart_page.checkout_button.click()
    assert 'Ошибка в номере телефона' in cart_page.text_under_phone_input.get_text()


# test43 Проверка ввода невалидных данных в поле для телефона
@pytest.mark.parametrize("invalid_symbols", [' ', 'abc', 'абв'], ids=['space', 'eng_letters', 'ru_letters'])
@pytest.mark.negative
def test_input_invalid_value_in_phone_field(driver, invalid_symbols):
    phone = invalid_symbols
    page = MainPage(driver)
    page.accept_cookie.click()
    page.add_to_cart.click()
    page.cart.wait_to_be_clickable()
    page.cart.click()
    cart_page = CartPage(driver, page.get_current_url())
    cart_page.go_to_checkout_buttont.wait_to_be_clickable()
    cart_page.go_to_checkout_buttont.click()
    cart_page.wait_page_loaded()
    cart_page.phone_input.scroll_to_element()
    cart_page.phone_input.wait_to_be_clickable()

    element = cart_page.get_phone_input(driver)
    actions = ActionChains(driver)
    actions.move_to_element(element).send_keys(phone).perform()

    cart_page.checkout_button.wait_to_be_clickable()
    cart_page.checkout_button.click()
    assert 'Телефон обязателен' in cart_page.text_under_phone_input.get_text()


# test44 Успешный поиск по слову на странице Помощи
@pytest.mark.positive
def test_success_search_in_help(driver):
    search_request = 'доставка'
    help_page = HelpPage(driver)
    help_page.search_input.wait_to_be_clickable()
    help_page.search_input.send_keys(search_request)
    help_page.find_button.click()
    help_page.wait_page_loaded()
    search_request_in_head_found_post = search_request in help_page.found_post_head.get_text()
    search_request_in_body_found_post = search_request in help_page.found_post_body_preview.get_text()
    # проверяем что в найденных сообщениях содержится искомое слово
    assert search_request_in_head_found_post or search_request_in_body_found_post


# test45 Безрезультатный поиск по слову на странице Помощи
@pytest.mark.negative
def test_unsuccess_search_in_help(driver):
    search_request = 'fffffffff'
    help_page = HelpPage(driver)
    help_page.search_input.wait_to_be_clickable()
    help_page.search_input.send_keys(search_request)
    help_page.find_button.click()
    help_page.wait_page_loaded()
    # проверяем что по запросу ничего не нашлось
    assert 'Поиск в разделе Помощь не дал результатов' in help_page.not_found_post_message.get_text()


# test46 Переход на главную страницу со страницы Помощи
@pytest.mark.negative
def test_unsuccess_search_in_help(driver):
    help_page = HelpPage(driver)
    help_page.logo.wait_to_be_clickable()
    help_page.logo.click()
    # проверяем что по нажатию на логотип происходит возврат на главную страницу
    assert help_page.get_current_url() == project_url



