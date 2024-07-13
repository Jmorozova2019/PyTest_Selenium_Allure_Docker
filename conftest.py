'''
является необязательным. Он считается pytest как “local plugin” и может содержать hook functions и fixtures. Hook functions являются способом вставки кода в часть процесса выполнения pytest для изменения работы pytest.
 Hook functions и fixtures, которые используются в тестах в нескольких подкаталогах, должны содержаться в tests/conftest.py. Вы можете иметь несколько файлов conftest.py; например, можно иметь по одному в тестах
 и по одному для каждой поддиректории tests.
'''

import pytest
from selenium import webdriver

# Регистрация кастомного аргумента командной строки
# пример вызова pytest --base-url=http://api.zippopotam.us zip_api_test.py
# https://software-testing.ru/library/testing/testing-tools/4074-pytest-and-custom-command-line-arguments
def pytest_addoption(parser):
    parser.addoption(
        '--base-url', action='store', default='http://uitestingplayground.com/', help='Base URL for the API tests'
    )
# Считать значение из командной строки
@pytest.fixture
def base_url(request):
    return request.config.getoption('--base-url')

@pytest.fixture()
def start_stop_driver(base_url, request):
    service = webdriver.ChromeService(executable_path='C://Users//zh.morozova//Desktop//Progs//pythonParametrize//tests//resources//chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    request.cls.driver = driver
    driver.maximize_window()
    driver.implicitly_wait(5)
    driver.get(base_url)

    yield

    driver.quit()