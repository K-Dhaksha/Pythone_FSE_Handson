import pytest
from pages.simple_form_page import SimpleFormPage
from pages.checkbox_page import CheckboxPage
from pages.dropdown_page import DropdownPage
from pages.input_form_page import InputFormPage

@pytest.mark.parametrize("message", [
    "Hello",
    "Selenium Automation",
    "12345"
])
def test_simple_form_submission(driver, base_url, message):
    page = SimpleFormPage(driver)
    page.navigate_to(base_url + "simple-form-demo/")
    page.enter_message(message)
    page.click_submit()
    assert page.get_displayed_message() == message

def test_checkbox_demo(driver, base_url):
    page = CheckboxPage(driver)
    page.navigate_to(base_url + "checkbox-demo/")
    
    # Check the first checkbox
    page.check_option(1)
    assert page.is_option_checked(1)
    
    # Uncheck the first checkbox
    page.uncheck_option(1)
    assert not page.is_option_checked(1)

def test_dropdown_selection(driver, base_url):
    page = DropdownPage(driver)
    page.navigate_to(base_url + "select-dropdown-demo/")
    page.select_day("Wednesday")
    assert page.get_selected_day() == "Wednesday"

def test_input_form_submit(driver, base_url):
    page = InputFormPage(driver)
    page.navigate_to(base_url + "input-form-demo/")
    page.fill_form(
        name="John Doe",
        email="john.doe@example.com",
        phone="1234567890",
        address="123 Science Park Drive"
    )
    page.submit_form()
    
    success_text = page.get_success_message()
    assert "Thanks for contacting us" in success_text

# ========================================================================================
# POM DESIGN PATTERN EXPLANATION (Hands-On 7, Step 59)
# ========================================================================================
# What problem would occur in a flat (non-POM) script if the Submit button's ID changed 
# from 'submit' to 'btn-submit'?
# 1. High Maintenance: If we have multiple test files (or multiple tests in the same file) 
#    that submit forms, we would have to search and replace 'submit' with 'btn-submit' 
#    across every single line where `driver.find_element(By.ID, 'submit')` occurs.
# 2. Code Duplication: Flat scripts duplicate structural locator logic in test actions, 
#    violating the DRY (Don't Repeat Yourself) principle.
#
# How does POM solve this?
# 1. Single Source of Truth: POM encapsulates all locators as class-level variables inside 
#    specific Page Classes.
# 2. Easy Update: If the Submit button ID changes to 'btn-submit', we only need to update 
#    one line in simple_form_page.py (SUBMIT_BUTTON = (By.ID, "btn-submit")). All tests calling 
#    `page.click_submit()` will automatically use the updated locator without any changes.
# 3. Separation of Concerns: Test files focus only on assertions and logic, while page 
#    files handle HTML structural interactions.