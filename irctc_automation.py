'''
Python script for checking trains, their seat availability, fares and other relevant details 
for a given pair of stations and journey date (read from a separate 'query_trains.txt' file) from IRCTC website.
'''
from selenium import webdriver
import time
from datetime import datetime

from selenium.webdriver.common.keys import Keys

with open('query_trains.txt', 'r') as f:
    for line in f.readlines():
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2} 
        chrome_options.add_experimental_option("prefs", prefs)
        # browser = webdriver.Chrome(executable_path='chromedriver.exe')
        browser = webdriver.Chrome(executable_path='your chromedriver path')

        # IRCTC website
        browser.get('https://www.irctc.co.in/nget/train-search/')
        time.sleep(2)

        # For popup that appears during COVID times, may not appear in future
        element = browser.find_elements_by_xpath('//*[@class ="btn btn-primary"]') 
        element[0].click() 
        time.sleep(2)

        # Finding origin, destination and journey date from each line read from file
        values = line.split()

        origin = values[0]
        element = browser.find_elements_by_xpath('//*[@class ="ng-tns-c58-8 ui-inputtext ui-widget ui-state-default ui-corner-all ui-autocomplete-input ng-star-inserted"]') 
        element[0].send_keys(origin) 
        time.sleep(2)
        auto_list = browser.find_element_by_xpath('//*[@id = "p-highlighted-option"]')
        auto_list.click()

        dest = values[1]
        element = browser.find_elements_by_xpath('//*[@class ="ng-tns-c58-9 ui-inputtext ui-widget ui-state-default ui-corner-all ui-autocomplete-input ng-star-inserted"]') 
        element[0].send_keys(dest)
        time.sleep(2)
        auto_list = browser.find_element_by_xpath('//*[@id = "p-highlighted-option"]')
        auto_list.click()

        journey_date = values[2]
        element = browser.find_elements_by_xpath('//*[@class ="ng-tns-c59-10 ui-inputtext ui-widget ui-state-default ui-corner-all ng-star-inserted"]') 
        element[0].send_keys(Keys.CONTROL + 'a')
        element[0].send_keys(Keys.DELETE)
        time.sleep(1)
        element[0].send_keys(journey_date)

        # Click on search button along with given parameters
        element = browser.find_elements_by_xpath('//*[@class ="search_btn train_Search"]') 
        element[0].click()
        time.sleep(2)

        # Finding parent div element
        element = browser.find_elements_by_xpath('//*[@class ="form-group no-pad col-xs-12 bull-back border-all"]')
        # Appending origin, destination and current time to filename
        file_name = 'res '+ origin +'-'+ dest + ' ' + datetime.now().strftime("%H%M%S") + '.txt'
        with open(file_name, 'w+', encoding='utf-8') as file:
            for el in element:
                # Reading relevant information and writing it into a separate file
                file.write("Train No.: " +el.find_element_by_xpath(".//*[@class = 'col-sm-5 col-xs-11 train-heading']").find_element_by_tag_name('strong').text + '\n')
                file.write("Dep Time: " + el.find_element_by_xpath(".//span[@class = 'time']").find_element_by_tag_name('strong').text + " ")
                file.write("Dep Stn and Date: " + el.find_element_by_xpath(".//div[@class = 'col-xs-5 hidden-xs']").text + " ")
                file.write("Duration: " + el.find_element_by_xpath(".//span[@class = 'col-xs-3 pull-left line-hr']").find_element_by_tag_name('span').text + " ")
                file.write("Arr Time: " + el.find_element_by_xpath(".//span[@class = 'pull-right']").find_element_by_tag_name('strong').text + " ")
                file.write("Arr Stn and Date: " + el.find_element_by_xpath(".//span[@class = 'pull-right']").text + "\n")
                for k,l,m in zip(el.find_elements_by_xpath(".//*[@class = 'hidden-xs col-xs-12 remove-padding']"), el.find_elements_by_xpath('.//*[@class = "AVAILABLE col-xs-12" or @class = "WL col-xs-12" or @class = "RAC col-xs-12" or @class = "REGRET col-xs-12"]'), el.find_elements_by_xpath(".//div[@class = 'hidden-xs']")):
                    file.write(m.find_element_by_tag_name('strong').text + ' ' + l.find_element_by_tag_name('strong').text + ' ' + k.find_element_by_tag_name('strong').text + '\n')
                file.write('\n')

        time.sleep(1)
        browser.close()
        time.sleep(1)