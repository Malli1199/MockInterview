from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sys

options = webdriver.ChromeOptions()
options.add_argument('--headless') # Runs silently in the background
driver = webdriver.Chrome(options=options)

try:
    # Point Selenium directly to the live environment port deployed by Jenkins
    driver.get("http://localhost:3000")
    time.sleep(2)
    
    # Target elements on the page
    user_field = driver.find_element(By.ID, "username")
    pass_field = driver.find_element(By.ID, "password")
    action_btn = driver.find_element(By.ID, "submitBtn")
    
    # Emulate automated user input
    user_field.send_keys("student2026")
    pass_field.send_keys("secureaccess")
    action_btn.click()
    time.sleep(1)
    
    # Assert validation results
    status_text = driver.find_element(By.ID, "displayStatus").text
    if "Access Granted" in status_text:
        print("SELENIUM CONFIRMATION: Login Flow Verified Perfectly.")
        sys.exit(0)
    else:
        print("SELENIUM ERROR: Verification mismatch.")
        sys.exit(1)
except Exception as ex:
    print(f"Selenium execution hit an environmental block: {ex}")
    sys.exit(1)
finally:
    driver.quit()