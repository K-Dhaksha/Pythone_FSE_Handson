from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage

class InputFormPage(BasePage):
    NAME_INPUT = (By.ID, "name")
    EMAIL_INPUT = (By.XPATH, "//input[@placeholder='Email'] | //input[@id='inputEmail4']")
    PASSWORD_INPUT = (By.ID, "inputPassword4")
    COMPANY_INPUT = (By.ID, "company")
    WEBSITE_INPUT = (By.ID, "websitename")
    COUNTRY_SELECT = (By.NAME, "country")
    CITY_INPUT = (By.ID, "inputCity")
    ADDRESS1_INPUT = (By.ID, "inputAddress1")
    ADDRESS2_INPUT = (By.ID, "inputAddress2")
    STATE_INPUT = (By.ID, "inputState")
    ZIP_INPUT = (By.ID, "inputZip")
    SUBMIT_BUTTON = (By.XPATH, "//button[text()='Submit']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".success-msg")

    def fill_form(self, name, email, phone, address, country="United States", city="San Jose", state="California", zipcode="95112", password="Password123", address2="Suite 100"):
        self.wait_for_element(self.NAME_INPUT).send_keys(name)
        self.wait_for_element(self.EMAIL_INPUT).send_keys(email)
        self.wait_for_element(self.PASSWORD_INPUT).send_keys(password)
        self.wait_for_element(self.COMPANY_INPUT).send_keys(phone)  # Map phone to company/website per requirements
        self.wait_for_element(self.WEBSITE_INPUT).send_keys("https://example.com")
        
        # Dropdown selection for country
        country_elem = self.wait_for_element(self.COUNTRY_SELECT)
        Select(country_elem).select_by_visible_text(country)

        self.wait_for_element(self.CITY_INPUT).send_keys(city)
        self.wait_for_element(self.ADDRESS1_INPUT).send_keys(address)
        self.wait_for_element(self.ADDRESS2_INPUT).send_keys(address2)
        self.wait_for_element(self.STATE_INPUT).send_keys(state)
        self.wait_for_element(self.ZIP_INPUT).send_keys(zipcode)

    def submit_form(self):
        self.wait_for_element_clickable(self.SUBMIT_BUTTON).click()

    def get_success_message(self):
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        msg_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.SUCCESS_MESSAGE)
        )
        return msg_element.text.strip()
