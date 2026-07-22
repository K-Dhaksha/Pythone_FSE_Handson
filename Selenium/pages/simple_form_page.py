from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class SimpleFormPage(BasePage):
    MESSAGE_INPUT = (By.ID, "user-message")
    SUBMIT_BUTTON = (By.ID, "showInput")
    DISPLAYED_MESSAGE = (By.XPATH, "//p[@id='message'] | //span[@id='message']")

    def enter_message(self, text):
        input_box = self.wait_for_element(self.MESSAGE_INPUT)
        input_box.clear()
        input_box.send_keys(text)

    def click_submit(self):
        button = self.wait_for_element_clickable(self.SUBMIT_BUTTON)
        button.click()
        
        # Wait up to 2 seconds for the text to be non-empty (signals successful submission)
        try:
            WebDriverWait(self.driver, 2).until(
                lambda d: d.find_element(*self.DISPLAYED_MESSAGE).text.strip() != ""
            )
        except Exception:
            # If it timed out, the first click was a dead click due to hydration delay; click again
            button.click()

    def get_displayed_message(self):
        result = self.wait_for_element(self.DISPLAYED_MESSAGE)
        return result.text.strip()
