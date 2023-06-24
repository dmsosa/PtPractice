import time
#Selenium imports 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#////////////////////////////////////////////////////////////////////////
path = 'C:/Users/duria/Desktop/worktool/driver/chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get('https://www.youtube.com/')
time.sleep(3)
cookies_window = 'eom-v1-dialog style-scope ytd-consent-bump-v2-lightbox style-scope ytd-consent-bump-v2-lightbox'
try:
    window = driver.find_element(By.ID, 'dialog')
    print(window.value_of_css_property('color'))

    buttons = WebDriverWait(window, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'button')))
except:
    print("Not found")
# if button is not None:
#     button.click()
# bar = driver.find_element(By.ID, 'search')

# bar.click()
# bar.send_keys('Hellos')
