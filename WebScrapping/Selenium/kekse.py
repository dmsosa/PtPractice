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

print('selecting language...', lang.text)

time.sleep(4)
ads2 = driver.find_element(By.CSS_SELECTOR, 'div.cc_banner.cc_container.cc_container--open a.cc_btn.cc_btn_accept_all')
ads2.click()
ads = driver.find_element(By.XPATH, '//ins/img[last()]')
ads.click()
time.sleep(2)


time.sleep(2)
cookie = driver.find_element(By.CSS_SELECTOR, 'button#bigCookie')
count = driver.find_element(By.ID, 'cookies')
products = [driver.find_element(By.ID, 'productPrice'+str(i)) for i in range(1,-1,-1)]
actions = ActionChains(driver)

info = driver.find_element(By.ID, 'logButton')
close = driver.find_element(By.CSS_SELECTOR, 'div#menu > div.close.menuClose')
actions.click(info)
actions.click(close)

for j in range(0, 50):
    actions.perform()
# for product in products:
#     content = product.find_element(By.CSS_SELECTOR, 'div.content')
#     price = content.find_element(By.CSS_SELECTOR, 'span.price').text
#     print(price)
#     break