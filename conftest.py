# Для дополнительной настройки работы браузера (размер окна, режим отображения и так далее), рекомендуется
# использовать фикстуры. Их стоит вставлять в файл conftest.py, который находится в корневой директории тестового
# проекта.

import pytest
import uuid
import pytest
import requests
from selenium import webdriver
from settings import valid_email, valid_password, project_url

"""
@pytest.fixture
def chrome_options(chrome_options):
    # chrome_options.binary_location = '/usr/bin/google-chrome-stable'
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--log-level=DEBUG')

    return chrome_options
"""

@pytest.fixture(scope='function')
def driver():
    driver = webdriver.Chrome('../drivers/chromedriver')
    driver.maximize_window()
    #driver.implicitly_wait(5)

    yield driver

    driver.close()
    driver.quit()



@pytest.fixture(scope='function')
def driver_with_cookies(driver):
    response = requests.post(url = f"{project_url}/login", data = {"email": valid_email, "pass": valid_password})
    assert response.status_code == 200
    assert 'Cookie' in response.request.headers, 'В запросе не передан ключ авторизации'
    print('\n getting auth_key')
    driver.get(project_url)
    cookie_list = response.request.headers.get('Cookie').split('=')
    driver.add_cookies({'name': cookie_list[0], 'value': cookie_list[1]})
    yield driver

"""
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # This function helps to detect that some test failed
    # and pass this information to teardown:

    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep
"""

"""
@pytest.fixture
def web_browser(request, selenium):

    browser = selenium
    browser.set_window_size(1400, 1000)

    # Return browser instance to test case:
    yield browser

    # Do teardown (this code will be executed after each test):

    if request.node.rep_call.failed:
        # Make the screen-shot if test failed:
        try:
            browser.execute_script("document.body.bgColor = 'white';")

            # Make screen-shot for local debug:
            browser.save_screenshot('screenshots/' + str(uuid.uuid4()) + '.png')

            # For happy debugging:
            print('URL: ', browser.current_url)
            print('Browser logs:')
            for log in browser.get_log('browser'):
                print(log)

        except:
            pass # just ignore any errors here

"""

"""
def get_test_case_docstring(item):
    
    # This function gets doc string from test case and format it
    # to show this docstring instead of the test case name in reports.
   
    

    full_name = ''

    if item._obj.__doc__:
        # Remove extra whitespaces from the doc string:
        name = str(item._obj.__doc__.split('.')[0]).strip()
        full_name = ' '.join(name.split())

        # Generate the list of parameters for parametrized test cases:
        if hasattr(item, 'callspec'):
            params = item.callspec.params

            res_keys = sorted([k for k in params])
            # Create List based on Dict:
            res = ['{0}_"{1}"'.format(k, params[k]) for k in res_keys]
            # Add dict with all parameters to the name of test case:
            full_name += ' Parameters ' + str(', '.join(res))
            full_name = full_name.replace(':', '')

    return full_name


def pytest_itemcollected(item):
    # This function modifies names of test cases "on the fly"
    # during the execution of test cases.

    if item._obj.__doc__:
        item._nodeid = get_test_case_docstring(item)

"""

"""
def pytest_collection_finish(session):
    # This function modified names of test cases "on the fly"
    # when we are using --collect-only parameter for pytest
    # (to get the full list of all existing test cases).   

    if session.config.option.collectonly is True:
        for item in session.items:
            # If test case has a doc string we need to modify it's name to
            # it's doc string to show human-readable reports and to
            # automatically import test cases to test management system.
            if item._obj.__doc__:
                full_name = get_test_case_docstring(item)
                print(full_name)

        pytest.exit('Done!')
"""