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
button_xpath = '//tp-yt-paper-dialog[@id="dialog"]/div[@id="content"]/div[last()]/div[6]/div[1]/ytd-button-renderer[last()]//button'
bar_xpath = '//div[@id="content"]/div[@id="masthead-container"]/ytd-masthead[@id="masthead"]//div[@id="center"]/ytd-searchbox[@id="search"]/form[@id="search-form"]//div[@id="search-input"]/input[@id="search"]'

try:
    # Die akzeptieren schaltflache finden
    accept_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, button_xpath))
    )
    print(accept_button.text)
except:
    accept_button = None
if accept_button is not None:
    accept_button.click()

time.sleep(5)
bar = driver.find_element(By.NAME, 'search_query')
bar.send_keys('Hello Mann!')
time.sleep(2)
bar.send_keys(Keys.RETURN)

quit()


