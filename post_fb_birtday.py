'''
Python script for automating birtday posts on facebook.
'''
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.chrome.options import Options 
from selenium.common.exceptions import TimeoutException 
from selenium.webdriver.common.keys import Keys 
import time 

chrome_options = webdriver.ChromeOptions() 

prefs = {"profile.default_content_setting_values.notifications": 2} 
chrome_options.add_experimental_option("prefs", prefs) 
browser = webdriver.Chrome(executable_path='your chromedriver path')
# browser = webdriver.Chrome(executable_path="chromedriver.exe") 

# Facebook website
browser.get('https://www.facebook.com/') 

# Your fb username
username = "your username"

# Getting your password from 'test.txt' file
with open('test.txt', 'r') as myfile: 
	password = myfile.read().replace('\n', '') 

element = browser.find_elements_by_xpath('//*[@id ="email"]') 
element[0].send_keys(username) 

element = browser.find_element_by_xpath('//*[@id ="pass"]') 
element.send_keys(password)  

log_in = browser.find_elements_by_id('u_0_b')
log_in[0].click() 

time.sleep(3)
# Going to birthdays URL
browser.get('https://www.facebook.com/events/birthdays/') 
time.sleep(3)

# Customized birthday message
birthday_msg = 'Happy Birthday! Enjoy your day.'

element = browser.find_elements_by_xpath("//*[@class ='_1p1v']") 
cnt = 0

for el in element: 
	cnt += 1
	element_id = str(el.get_attribute('id')) 
	XPATH = '//*[@id ="' + element_id + '"]'
	post_field = browser.find_element_by_xpath(XPATH) 
	# Writing birthday message
	post_field.send_keys(birthday_msg) 
	# Hitting enter
	post_field.send_keys(Keys.RETURN) 
	print("Birthday Wish posted for friend " + str(cnt)) 

browser.close() 
