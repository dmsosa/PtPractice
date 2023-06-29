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
import threading
# from pathlib import Path

# executable path has been deprecated, we better use service variables now.
# dpath = Path('C:/Users/duria/Desktop/worktool/driver/chromedriver.exe')

def run():
    def getValue(item: str) -> int:
        if ('"') in item:
            value = int(item.strip('"'))
        else:
            value = int(item.split(" ")[0])
        return value
    def clickCookie(driver, element):
            actions = ActionChains(driver)
            actions.click(element)
            actions.perform()
    def purchaseProduct(driver, element):
        actions = ActionChains(driver)
        actions.move_to_element(element)
        actions.click()
        actions.perform()
        print('purchased!')

#Setting up Selenium
    options = webdriver.ChromeOptions()
    service = Service(ChromeDriverManager().install())
    options.add_experimental_option('detach', True)
    driver = webdriver.Chrome(options=options, service=service)
    driver.get('https://orteil.dashnet.org/cookieclicker/')


#Closing cookies windows / Unerwunschte Fernster schliessen
    button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.fc-button.fc-cta-consent.fc-primary-button')))
    print(button.text, 'cookies')
    button.click()
    driver.implicitly_wait(3)

#Selecting Language / Sprache auswahlen
    lang = driver.find_element(By.ID, 'langSelect-DE')
    sprach = lang.text
    lang.click()
    print('selecting language...', sprach)
    time.sleep(4)
    ads2 = driver.find_element(By.CSS_SELECTOR, 'div.cc_banner.cc_container.cc_container--open a.cc_btn.cc_btn_accept_all')
    ads2.click()
    ads = driver.find_element(By.XPATH, '//ins/img[last()]')
    ads.click()
    time.sleep(2)

#Kekse finden
    cookie = driver.find_element(By.CSS_SELECTOR, '#bigCookie')
    count = driver.find_element(By.ID, 'cookies')
    products = [driver.find_element(By.ID, 'productPrice'+str(i)) for i in range(1,-1,-1)]

#Kekse klicken und Produkte kaufen!
    for j in range(0, 5000):
        clickCookie(driver, cookie)
        my_cookies = getValue(count.text)
        for product in products:
            price = getValue(product.text)
            if price <= my_cookies:
                purchaseProduct(driver, product)

if __name__ == '__main__':
    run()