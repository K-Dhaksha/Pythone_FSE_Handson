from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CheckboxPage(BasePage):
    def get_checkbox_locator(self, index):
        # Retrieves the 1-indexed checkbox element
        return (By.XPATH, f"(//input[@type='checkbox'])[{index}]")

    def check_option(self, index):
        locator = self.get_checkbox_locator(index)
        checkbox = self.wait_for_element_clickable(locator)
        if not checkbox.is_selected():
            checkbox.click()
            try:
                WebDriverWait(self.driver, 1.5).until(
                    lambda d: d.find_element(*locator).is_selected()
                )
            except Exception:
                # Retry if first click was missed/ignored
                elem = self.driver.find_element(*locator)
                if not elem.is_selected():
                    elem.click()

    def uncheck_option(self, index):
        locator = self.get_checkbox_locator(index)
        checkbox = self.wait_for_element_clickable(locator)
        if checkbox.is_selected():
            checkbox.click()
            try:
                WebDriverWait(self.driver, 1.5).until(
                    lambda d: not d.find_element(*locator).is_selected()
                )
            except Exception:
                # Retry if first click was missed/ignored
                elem = self.driver.find_element(*locator)
                if elem.is_selected():
                    elem.click()

    def is_option_checked(self, index):
        locator = self.get_checkbox_locator(index)
        checkbox = self.wait_for_element(locator)
        return checkbox.is_selected()
