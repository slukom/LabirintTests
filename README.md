# Автотесты для интернет-магазина Labirint
Реализован проект тестирования интернет-магазина https://www.labirint.ru/ с помощью 
Python и Selenium.

В рамках данного проекта автоматизированы основные сценарии пользователей:
* авторизация на сайте
* поиск автора
* поиск книги по названию
* поиск книги по ISBN
* добавление книги в Отложенные
* добавление книги в Корзину
* оформление покупки
* отправки вопроса в поддержку

# Запуск тестов
Необходимо предварительно установить selenium:

    pip install pytest-selenium

В Pycharm выбрать File - Settings - Python Interpreter - Добавить pytest-selenium 
(кликнуть на знак “+” в правом меню, и выбрать pytest-selenium — Установка)
Для запуска в консоли выполнить команду: 

    python3 -m pytest -v --driver Chrome --driver-path /drivers/chromedriver tests/test_for_labirint.py
