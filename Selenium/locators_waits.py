from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import Select

from selenium.common.exceptions import NoSuchElementException
import time

# ------------------------------------------
# Driver Setup
# ------------------------------------------

options = Options()

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.maximize_window()

wait = WebDriverWait(driver,10)

driver.get("https://www.lambdatest.com/selenium-playground/")

# ==========================================================
# Task 32
# All Locator Strategies
# ==========================================================

driver.find_element(By.LINK_TEXT,"Simple Form Demo").click()

message_box = driver.find_element(By.ID,"user-message")
print("Found using ID")

message_box = driver.find_element(By.NAME,"message")
print("Found using NAME")

message_box = driver.find_element(By.CLASS_NAME,"form-control")
print("Found using CLASS_NAME")

message_box = driver.find_element(By.TAG_NAME,"input")
print("Found using TAG_NAME")

message_box = driver.find_element(
    By.XPATH,
    "/html/body/div[2]/div/div/div[2]/div/div[1]/div/input"
)
print("Found using Absolute XPath")

message_box = driver.find_element(
    By.XPATH,
    "//input[@id='user-message']"
)
print("Found using Relative XPath")

# ==========================================================
# Task 33
# CSS Selectors
# ==========================================================

driver.find_element(
    By.CSS_SELECTOR,
    "#user-message"
)

driver.find_element(
    By.CSS_SELECTOR,
    "input[name='message']"
)

driver.find_element(
    By.CSS_SELECTOR,
    "div > input"
)

print("CSS Selectors Working")

# ==========================================================
# Task 34
# XPath text() and contains()
# ==========================================================

driver.back()

driver.find_element(By.LINK_TEXT,"Checkbox Demo").click()

label = driver.find_element(
    By.XPATH,
    "//label[text()='Option 1']"
)

print(label.text)

labels = driver.find_elements(
    By.XPATH,
    "//label[contains(text(),'Option')]"
)

print("Checkbox Labels:")

for i in labels:
    print(i.text)

# ==========================================================
# Task 35
# Preferred Locator Ranking
# ==========================================================

"""
Preferred Locator Ranking

1. ID
2. CSS Selector
3. Name
4. XPath (Relative)
5. Class Name
6. XPath (Absolute)

Reason:

ID is unique and fastest.

CSS Selectors are fast and readable.

Name works well when unique.

Relative XPath is flexible.

Class Names are often reused.

Absolute XPath is fragile because any HTML
change breaks it.
"""

# ==========================================================
# Task 36
# Explicit Wait
# ==========================================================

driver.get("https://www.lambdatest.com/selenium-playground/bootstrap-alert-messages-demo")

success_btn = wait.until(
    EC.element_to_be_clickable(
        (By.ID,"autoclosable-btn-success")
    )
)

success_btn.click()

alert = wait.until(
    EC.visibility_of_element_located(
        (By.CSS_SELECTOR,".alert-success")
    )
)

assert "successfully" in alert.text.lower()

print("Explicit Wait Successful")

# ==========================================================
# Task 37
# Compare sleep() vs Explicit Wait
# ==========================================================

driver.refresh()

start = time.time()

driver.find_element(By.ID,"autoclosable-btn-success").click()

time.sleep(3)

sleep_time = time.time() - start

print("Sleep Time:",sleep_time)

driver.refresh()

start = time.time()

driver.find_element(By.ID,"autoclosable-btn-success").click()

wait.until(
    EC.visibility_of_element_located(
        (By.CSS_SELECTOR,".alert-success")
    )
)

wait_time = time.time() - start

print("Explicit Wait Time:",wait_time)

"""
Explicit Wait is better because it waits only
until the condition is satisfied.

sleep() always pauses for the full duration,
making tests slower.
"""

# ==========================================================
# Task 38
# Clickable Wait
# ==========================================================

driver.refresh()

button = wait.until(
    EC.element_to_be_clickable(
        (By.ID,"autoclosable-btn-success")
    )
)

button.click()

"""
visibility_of_element_located
-----------------------------
Element is present and visible.

element_to_be_clickable
-----------------------
Element is visible AND enabled so it can be clicked.
"""

# ==========================================================
# Task 39
# Fluent Wait
# ==========================================================

fluent_wait = WebDriverWait(
    driver,
    timeout=10,
    poll_frequency=0.5,
    ignored_exceptions=[NoSuchElementException]
)

try:

    element = fluent_wait.until(
        EC.presence_of_element_located(
            (By.TAG_NAME,"body")
        )
    )

    print("Fluent Wait Successful")

except:

    print("Element not found")

driver.quit()