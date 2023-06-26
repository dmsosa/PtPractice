from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time


dpath = 'C:\Users\duria\Desktop\worktool\driver\chromedriver.exe'
driver = webdriver.Chrome(dpath)
service = webdriver.service()

driver = webdriver.Chrome()