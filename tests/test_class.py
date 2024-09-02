import time
import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.color import Color
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

def scroll_and_click_link(driver, partial_link):
    link_element = driver.find_element(By.CSS_SELECTOR, partial_link)
    ActionChains(driver).scroll_to_element(link_element).perform()
    link_element.click()

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
        assert self.driver.find_element(By.XPATH, '//button[.="Button with Dynamic ID"]').is_displayed()

        self.driver.find_element(By.CSS_SELECTOR, 'a[href="/"]').click()
        assert self.driver.find_element(By.CSS_SELECTOR, '#title').is_displayed()

    @allure.suite("Main suite")
    @allure.title("Test actions")
    @allure.description("This test check classattr")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("owner", "Zhanna Morozova")
    def test_2_class_attribute(self):
        self.driver.find_element(By.CSS_SELECTOR, 'a[href="/classattr"]').click()
        self.driver.find_element(By.XPATH, '//button[contains(@class, "btn-primary")]').click()

        try:
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            print("testtAlert detected: ", alert.text)
            alert.accept()
        except TimeoutException:
            print("No alert detected within timeout.")

        self.driver.find_element(By.CSS_SELECTOR, 'a[href="/"]').click()
        assert self.driver.find_element(By.CSS_SELECTOR, '#title').is_displayed()


    @allure.description("This test check hidden layers")
    @allure.label("owner", "Zhanna Morozova")
    #Элементы с более высокими z-index перекрывают элементы с более низким z-индексом
    def test_3_hidden_layers(self):
        self.driver.find_element(By.CSS_SELECTOR, 'a[href="/hiddenlayers"]').click()
        assert self.driver.find_element(By.XPATH, '//h3[.="Hidden Layers"]').is_displayed()

        # нажать зеленую кнопку
        self.driver.find_element(By.ID, 'greenButton').click()

        # получить z-индекс зеленой кнопки
        green_button_div = self.driver.find_element(By.XPATH, '//button[@id="greenButton"]/..').get_attribute('style')

        # получить z-индекс синей кнопки
        blue_button_div = self.driver.find_element(By.XPATH, '//button[@id="blueButton"]/..').get_attribute('style')
        assert int(green_button_div[-2:-1]) < int(blue_button_div[-2:-1])

    def test_4_load_delay(self):
        self.driver.find_element(By.CSS_SELECTOR, 'a[href="/loaddelay"]').click()
        assert self.driver.find_element(By.XPATH, '//h3[.="Load Delays"]').is_displayed()

        element = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.XPATH, "//button[text()='Button Appearing After Delay']")))

        assert element.is_displayed()

    def test_5_AJAX_data(self):
        link_element = self.driver.find_element(By.CSS_SELECTOR, 'a[href="/ajax"]')
        actions = ActionChains(self.driver).scroll_to_element(link_element).perform()
        link_element.click()
        assert self.driver.find_element(By.XPATH, '//h3[.="AJAX Data"]').is_displayed()

        self.driver.find_element(By.XPATH, '//button[text()="Button Triggering AJAX Request"]').click()
        element = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.XPATH, "//p[text()='Data loaded with AJAX get request.']")))

        assert element.is_displayed()

    def test_6_Client_side_delay(self):
        scroll_and_click_link(self.driver,"a[href='/clientdelay']")
        assert self.driver.find_element(By.XPATH, '//h3[.="Client Side Delay"]').is_displayed()

        self.driver.find_element(By.CSS_SELECTOR, '#ajaxButton').click()
        element = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
            (By.XPATH, '//div[@id="content"]/p')))
        assert element.is_displayed()

    def test_7_click(self):
        scroll_and_click_link(self.driver,"a[href='/click']")
        assert self.driver.find_element(By.XPATH, '//h3[.="Click"]').is_displayed()

        element = self.driver.find_element(By.ID, 'badButton')
        ActionChains(self.driver).move_to_element(element).click().perform()

        time.sleep(5)
        btn_bg_colour = Color.from_string(element.value_of_css_property('background-color'))
        assert btn_bg_colour.rgba == 'rgba(33, 136, 56, 1)'

    def test_8_text_input(self):
        scroll_and_click_link(self.driver,"a[href='/textinput']")
        assert self.driver.find_element(By.XPATH, '//h3[.="Text Input"]').is_displayed()

        text_input_element = self.driver.find_element(By.ID, 'newButtonName')

        text_input_value = '123'
        ActionChains(self.driver).send_keys_to_element(text_input_element, text_input_value).perform()

        self.driver.find_element(By.ID, 'updatingButton').click()
        assert self.driver.find_element(By.ID, 'updatingButton').text == text_input_value

    def test_9_scrollbars(self):
        scroll_and_click_link(self.driver, "a[href='/scrollbars']")
        assert self.driver.find_element(By.XPATH, '//h3[.="Scrollbars"]').is_displayed()

        text_input_element = self.driver.find_element(By.ID, 'hidingButton')
        ActionChains(self.driver).scroll_to_element(text_input_element).click().perform()

        assert text_input_element.is_displayed()

    def test_10_dinamic_table(self):
        scroll_and_click_link(self.driver, "a[href='/dynamictable']")
        assert self.driver.find_element(By.XPATH, '//h3[.="Dynamic Table"]').is_displayed()

        cols_name = self.driver.find_elements(By.XPATH, '//span[@role="columnheader"]')
        crome_CPU_value = -1
        # получить индекс столбца CPU
        idx_cols_CPU = -1
        for i in range(len(cols_name)):
            if cols_name[i].text == 'CPU':
                idx_cols_CPU = i
                break

        # Найти индекс строки хрома
        row_groups = self.driver.find_elements(By.XPATH, '//div[@role="row"]')

        for j in range(1, len(row_groups)):
            ts = row_groups[j].find_elements(By.XPATH, './span[@role="cell"]')
            t = ts[0]
            if t.text == 'Chrome':
                crome_CPU_value = row_groups[j].find_element(By.XPATH, './span[@role="cell"][position()=' + str(idx_cols_CPU +1) +']')

        control_text = self.driver.find_element(By.CLASS_NAME, 'bg-warning').text
        assert control_text == 'Chrome CPU: ' + crome_CPU_value.text

    def test_11_verify_text(self):
        scroll_and_click_link(self.driver, "a[href='/verifytext']")
        assert self.driver.find_element(By.XPATH, '//h3[.="Verify Text"]').is_displayed()
        assert self.driver.find_element(By.XPATH, '//span[contains(text(), "Welcome")]').is_displayed()

    def test_12_progress_bar(self):
        scroll_and_click_link(self.driver, "a[href='/progressbar']")
        assert self.driver.find_element(By.XPATH, '//h3[.="Progress Bar"]').is_displayed()

        self.driver.find_element(By.ID, 'startButton').click()

        while int(self.driver.find_element(By.ID, 'progressBar').get_attribute('aria-valuenow')) < 75:
            time.sleep(0.1)
        self.driver.find_element(By.ID, 'stopButton').click()

        res = self.driver.find_element(By.ID, 'result').text
        assert 'Result: 0' in res

    def test_13_visibility(self):
        scroll_and_click_link(self.driver, "a[href='/visibility']")
        assert self.driver.find_element(By.XPATH, '//h3[.="Visibility"]').is_displayed()

        # Все кнопки видны
        assert self.driver.find_element(By.ID, 'hideButton').is_displayed()
        assert self.driver.find_element(By.ID, 'transparentButton').is_displayed()
        assert self.driver.find_element(By.ID, 'removedButton').is_displayed()
        assert self.driver.find_element(By.ID, 'invisibleButton').is_displayed()
        assert self.driver.find_element(By.ID, 'zeroWidthButton').is_displayed()
        assert self.driver.find_element(By.ID, 'notdisplayedButton').is_displayed()
        assert self.driver.find_element(By.ID, 'overlappedButton').is_displayed()
        assert self.driver.find_element(By.ID, 'offscreenButton').is_displayed()

        self.driver.find_element(By.ID, 'hideButton').click()

        # Все кнопки остались в DOM, но не видны
        assert self.driver.find_element(By.ID, 'hideButton').is_displayed()
        assert self.driver.find_element(By.ID, 'transparentButton').get_attribute('style') == 'opacity: 0;'
        assert len(self.driver.find_elements(By.XPATH, '//td[.="Hide"]/following-sibling::td[1]//*')) == 0
        assert self.driver.find_element(By.ID, 'invisibleButton').get_attribute('style') == 'visibility: hidden;'
        assert self.driver.find_element(By.ID, 'zeroWidthButton').size['width'] == 0
        assert self.driver.find_element(By.ID, 'notdisplayedButton').get_attribute('style') == 'display: none;'
        assert self.driver.find_element(By.ID, 'offscreenButton').location.get('x') == -9999
        assert self.driver.find_element(By.ID, 'offscreenButton').location.get('y') == -9999

    def test_14_sample_app(self):
        scroll_and_click_link(self.driver, "a[href='/sampleapp']")
        assert self.driver.find_element(By.XPATH, '//h3[.="Sample App"]').is_displayed()

        self.driver.find_element(By.XPATH, '//input[@name="UserName"]').send_keys('User 1')
        self.driver.find_element(By.XPATH, '//input[@name="Password"]').send_keys('pwd')
        self.driver.find_element(By.ID, 'login').click()

        assert self.driver.find_element(By.XPATH, '//label[.="Welcome, User 1!"]')

    def test_15_mous_over(self):
        scroll_and_click_link(self.driver, "a[href='/mouseover']")
        assert self.driver.find_element(By.XPATH, '//h3[.="Mouse Over"]').is_displayed()

        self.driver.find_element(By.XPATH, '//a[@title="Click me"]').click()
        self.driver.find_element(By.XPATH, '//a[@title="Active Link"]').click()
        self.driver.save_screenshot('res/screen_15.png')
        assert self.driver.find_element(By.ID, 'clickCount').text == '2'

    def test_16_non_breaking(self):
        scroll_and_click_link(self.driver, "a[href='/nbsp']")
        assert self.driver.find_element(By.XPATH, '//h3[.="Non-Breaking Space"]').is_displayed()

        assert self.driver.find_element(By.XPATH, '//button[.="My\u00A0Button"]').is_displayed()
        self.driver.find_element(By.XPATH, '//button[.="My\u00A0Button"]').click()

    def test_17_overlapped_element(self):
        scroll_and_click_link(self.driver, "a[href='/overlapped']")
        assert self.driver.find_element(By.XPATH, '//h3[.="Overlapped Element"]').is_displayed()

        self.driver.find_element(By.ID, 'id').send_keys('J1')
        bottom_element = self.driver.find_element(By.ID, 'subject')
        actions = ActionChains(self.driver).scroll_to_element(bottom_element).perform()
        self.driver.find_element(By.ID, 'name').send_keys('Janna')

    @pytest.mark.skip
    # сначала settings - Preferences - Element - Show user agent shadow DOM
    # не решено - нужно разобраться со вложенным shadow_root
    def test_18_shadow_DOM(self):
        scroll_and_click_link(self.driver, "a[href='/shadowdom']")
        assert self.driver.find_element(By.XPATH, '//h3[.="Shadow DOM"]').is_displayed()

        shadow_host = self.driver.find_element(By.CSS_SELECTOR, 'guid-generator')
        shadow_root = shadow_host.shadow_root
        shadow_root.find_element(By.ID, 'buttonGenerate').click()
        shadow_root.find_element(By.ID, 'buttonCopy').click()

        WebDriverWait(self.driver, 10).until(
        EC.visibility_of(shadow_root.find_element(By.ID, 'editField')))
        inner_shadow_host = shadow_root.find_element(By.ID, 'editField')
        inner_shadow_root = inner_shadow_host.shadow_root
        #inner_shadow_root.find_element(By.CSS_SELECTOR, 'div').text

    def test_19_alerts(self):
        scroll_and_click_link(self.driver, "a[href='/alerts']")
        assert self.driver.find_element(By.XPATH, '//h3[.="Alerts"]').is_displayed()

        self.driver.implicitly_wait(2)

        self.driver.find_element(By.ID, 'alertButton').click()
        alert = self.driver.switch_to.alert
        assert 'Today is a working day.' in alert.text
        alert.accept()

        self.driver.find_element(By.ID, 'confirmButton').click()
        confirm = self.driver.switch_to.alert
        assert 'Today is Friday.\nDo you agree?' in confirm.text
        confirm.dismiss()

        self.driver.find_element(By.ID, 'promptButton').click()
        prompt = self.driver.switch_to.alert
        assert 'Choose "cats" or \'dogs\'.\nEnter your value:' in prompt.text
        prompt.send_keys('cats')
        prompt.accept()

    #не доделано
    @pytest.mark.skip
    def test_20_file_upload(self):
        scroll_and_click_link(self.driver, "a[href='/upload']")
        assert self.driver.find_element(By.XPATH, '//h3[.="File Upload"]').is_displayed()
        self.driver.find_element(By.XPATH, '//div[@class="upload-info"]')
       #.send_keys(os.getcwd()+"/image.png")
    
