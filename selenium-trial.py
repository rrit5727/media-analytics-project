# /usr/local/bin - chromedriver filepath

from selenium import webdriver
from selenium.webdriver.common.by import By

# Initialize WebDriver
driver = webdriver.Chrome() 

driver.get("https://www.google.com")

# Perform actions
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("Selenium WebDriver")
search_box.submit()

# close the browser
driver.quit
