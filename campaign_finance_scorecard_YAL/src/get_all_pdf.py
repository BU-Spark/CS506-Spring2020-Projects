from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.common.exceptions import *
import random
from datetime import datetime


def scrape():
    chrome_options = Options()
    chrome_options.add_experimental_option('prefs', {
        "plugins.always_open_pdf_externally": True,
        "download.default_directory": "D:\\506_final\\all_files\\s"
    })
    driver = webdriver.Chrome(executable_path='D:\\506_final\\phantomjs-2.1.1-windows\\bin\\chromedriver.exe',
                              options=chrome_options)
    with open('./company_links/s') as file:
        i = 0
        d = 34846  # 34746
        for line in file:
            i += 1
            if i < 64721:  # 64560
                continue
            if i % 40 == 0:
                driver.close()
                driver = webdriver.Chrome(
                    executable_path='D:\\506_final\\phantomjs-2.1.1-windows\\bin\\chromedriver.exe',
                    options=chrome_options)
            print(i, end=' ')
            driver.get(line)
            driver.implicitly_wait(0.1)
            try:
                driver.find_element_by_id('MainContent_lstFilings').send_keys('Annual Report')
                driver.find_element_by_id('MainContent_btnViewFilings').click()
                driver.find_element_by_id('MainContent_grdSearchResults')
            except NoSuchElementException:
                print('')
                continue
            first = driver.find_element_by_xpath("//*[@id='MainContent_grdSearchResults']/tbody/tr[2]")
            try:
                first.find_element_by_class_name('link').click()
                d += 1
                print(d, end=' ')
            except NoSuchElementException:
                pass
            print('')


if __name__ == '__main__':
    scrape()
