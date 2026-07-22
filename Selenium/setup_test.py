"""
Hands-On 4
Selenium WebDriver Setup, Browser Drivers & Basic Commands

Selenium Components

1. WebDriver
WebDriver is the core Selenium component that communicates directly with the browser
through browser-specific drivers such as ChromeDriver. It performs browser automation
by sending commands like click, type, navigate, and retrieve elements.

2. Selenium Grid
Selenium Grid enables parallel execution of tests across multiple machines,
operating systems, and browsers. It is mainly used to reduce execution time
and improve cross-browser testing.

3. Selenium IDE
Selenium IDE is a browser extension used to record and playback browser actions.
It is useful for beginners and can generate Selenium code automatically.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os

# ----------------------------
# Chrome Options
# ----------------------------

options = Options()

# Headless mode
options.add_argument("--headless=new")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# ---------------------------------------------------
# Implicit Wait
# ---------------------------------------------------
# Implicit wait tells Selenium to wait for an element
# before throwing NoSuchElementException.
#
# Although easy to use, global implicit waits are not
# recommended because they slow every element lookup
# and make debugging harder.
#
# Explicit waits are preferred since they wait only
# for specific conditions.
# ---------------------------------------------------

driver.implicitly_wait(10)

# ===================================================
# Task 25
# ===================================================

driver.get("https://www.lambdatest.com/selenium-playground/")

print("Page Title:")
print(driver.title)

# ===================================================
# Task 28
# ===================================================

driver.find_element(By.LINK_TEXT, "Simple Form Demo").click()

assert "simple-form-demo" in driver.current_url

print("Navigated successfully.")

driver.back()

print("Returned to previous page.")

# ===================================================
# Task 29
# ===================================================

driver.execute_script(
    'window.open("https://www.google.com");'
)

print("\nWindow Handles:")
print(driver.window_handles)

driver.switch_to.window(driver.window_handles[1])

print("\nGoogle Title:")
print(driver.title)

# ===================================================
# Task 30
# ===================================================

driver.switch_to.window(driver.window_handles[0])

driver.save_screenshot("playground_screenshot.png")

if os.path.exists("playground_screenshot.png"):
    print("\nScreenshot saved successfully.")

# ===================================================
# Task 31
# ===================================================

print("\nCurrent Window Size:")

print(driver.get_window_size())

driver.set_window_size(1280, 800)

print("\nNew Window Size:")

print(driver.get_window_size())

# Consistent window size ensures responsive layouts
# behave the same during every automation run.

driver.quit()

print("\nExecution Completed Successfully.")