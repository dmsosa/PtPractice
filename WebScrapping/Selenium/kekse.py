from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time
# from pathlib import Path

# executable path has been deprecated, we better use service variables now.
# dpath = Path('C:/Users/duria/Desktop/worktool/driver/chromedriver.exe')
options = webdriver.ChromeOptions()
service = Service(ChromeDriverManager().install())
options.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=options, service=service)
driver.get('https://orteil.dashnet.org/cookieclicker/')
button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.fc-button.fc-cta-consent.fc-primary-button'))
                                         )
print(button.text, 'cookies')
button.click()
driver.implicitly_wait(3)
lang = driver.find_element(By.ID, 'langSelect-DE')
lang.click()
print('selecting language...')
driver.implicitly_wait(5)

cookie = driver.find_element(By.ID, 'bigCookie')
count = driver.find_element(By.ID, 'cookies').text
print(count)
products = [driver.find_element(By.ID, 'productPrice'+str(i)) for i in range(1,-1,-1)]

actions = ActionChains(driver)
actions.click(cookie)
for i in range(0, 5001):
    actions.perform()
# for product in products:
#     content = product.find_element(By.CSS_SELECTOR, 'div.content')
#     price = content.find_element(By.CSS_SELECTOR, 'span.price').text
#     print(price)
#     break