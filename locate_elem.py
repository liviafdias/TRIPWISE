from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# DRIVER
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run in headless mode
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.instagram.com/reel/DAMs7ojuyK0/")

elem = []
elem = driver.find_elements(By.XPATH, ".//h3[@class='_a9zc']//a")

for e in elem:
    print(e.text)