import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def pytest_addoption(parser):
    parser.addoption(
        '--base-url', action='store', default='http://uitestingplayground.com/', help='Base URL for the API tests'
    )
# Считать значение из командной строки
@pytest.fixture
def base_url(request):
    return request.config.getoption('--base-url')

@pytest.fixture
def start_stop_driver(base_url, request):
    chrome_driver_path = r'resource/chromedriver_128.exe'
    service = webdriver.ChromeService(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service)
    request.cls.driver = driver

    driver.maximize_window()
    driver.implicitly_wait(5)
    driver.get('http://uitestingplayground.com/')

    yield

    driver.quit()