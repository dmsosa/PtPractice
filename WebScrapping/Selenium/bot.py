from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
path = 'C:/Users/duria/Desktop/worktool/driver/chromedriver.exe'
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://www.youtube.com/')
bar = driver.find_element(by=id, 'search')
bar.click()
bar.send_keys('Hellos')