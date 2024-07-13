'''
Открыть http://uitestingplayground.com/
Найти элемент-ссылку Dinamic ID
Открыть ее
Нажать кнопку Playground
Вернуться на главную страницу кликом по пункту UITAP в заголовке
'''

import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
@pytest.mark.usefixtures("start_stop_driver")

class TestSeleniumDyn:

    @allure.suite("Main suite")
    @allure.title("Test actions")
    @allure.description("This test check dynamicid")
    @allure.tag("CheckActions")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("owner", "Zhanna Morozova")
    def test_1_dynamic_id(self):
        self.driver.find_element(By.CSS_SELECTOR, 'a[href="/dynamicid"]').click()
        assert self.driver.find_element(By.XPATH, '//button[text()="Button with Dynamic ID"]').is_displayed()

        self.driver.find_element(By.CSS_SELECTOR, 'a[href="/"]').click()
        assert  self.driver.find_element(By.CSS_SELECTOR, '#title').is_displayed()

    @allure.suite("Main suite")
    @allure.title("Test actions")
    @allure.description("This test check classattr")
    @allure.tag("CheckActions")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("owner", "Zhanna Morozova")
    def test_2_class_attribute(self):
        self.driver.find_element(By.CSS_SELECTOR, 'a[href="/classattr"]').click()
        self.driver.find_element(By.XPATH, '//button[contains(@class, "btn-primary")]').click()

        try:
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            print("Alert detected: ", alert.text)
            alert.accept()
        except TimeoutException:
            print("No alert detected within timeout.")

        self.driver.find_element(By.CSS_SELECTOR, 'a[href="/"]').click()
        assert self.driver.find_element(By.CSS_SELECTOR, '#title').is_displayed()

    @allure.suite("Main suite")
    @allure.title("Test actions")
    @allure.description("This test check hidden layers")
    @allure.tag("CheckActions")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("owner", "Zhanna Morozova")
    def test_3_hidden_layers(self):
        pass

    '''def test_4_load_delay(self):
        pass
    def test_5_AJAX_data(self):
        pass
    def test_6_Client_side_delay(self):
        pass

    def test_7_click(self):
        pass
    def test_8_text_input(self):
        pass
    def test_9_scrollbars(self):
        pass
    def test_10_dinamic_table(self):
        pass
    def test_11_verify_text(self):
        pass
    def test_12_progress_bar(self):
        pass
    def test_13_visibility(self):
        pass
    def test_14_samplre_app(self):
        pass
    def test_15_mous_over(self):
        pass
    def test_16_non_breaking(self):
        pass
    def test_17_overlapped_element(self):
        pass
    def test_18_shadow_DOM(self):
        pass
    def test_19_alerts(self):
        pass
'''