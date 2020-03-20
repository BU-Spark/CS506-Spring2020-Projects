from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.common.exceptions import *
import random


def scrape():
    chrome_options = Options()
    chrome_options.add_experimental_option('prefs', {"plugins.always_open_pdf_externally": True})

    driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)

    alphabet = ['aaaa']

    for alpha in alphabet:
        driver.get("http://lgwhd2o.x.incapdns.net/CorpWeb/CorpSearch/CorpSearch.aspx")
        sleep(2 + random.uniform(-1, 1))
        driver.find_element_by_id('MainContent_txtEntityName').send_keys(alpha)
        driver.find_element_by_id('MainContent_btnSearch').click()
        try:
            total = driver.find_element_by_id('MainContent_SearchControl_ltNumOfPages').text
            total = int(total.replace('\n', '').split(': ')[1])
        except NoSuchElementException:
            total = 1
        total_number = driver.find_element_by_id('MainContent_SearchControl_ltNumOfRecords').text
        total_number = int(total_number.replace('\n', '').split(': ')[1].replace(',', ''))
        last = total_number % 25
        for page in range(total):
            if page == total - 1:
                number = last
            else:
                number = 25
            for i in range(number):
                attr = []
                for j in driver.find_element_by_id('MainContent_SearchControl_grdSearchResultsEntity'). \
                        find_elements_by_class_name('link'):
                    attr.append(j)
                if i < len(attr):
                    attr[i].click()
                    sleep(2 + random.uniform(-1, 1))
                    driver.find_element_by_id('MainContent_btnViewFilings').click()
                    sleep(2 + random.uniform(-1, 1))
                    table = driver.find_element_by_id('MainContent_grdSearchResults')
                    table_tr_list = table.find_elements_by_tag_name('tr')
                    for tr in table_tr_list:
                        info = []
                        table_td_list = tr.find_elements_by_tag_name("td")
                        for td in table_td_list:
                            info.append(td.text)
                        if 'Annual Report' in info:
                            try:
                                tr.find_element_by_class_name('link').click()
                                sleep(1.1 + random.uniform(-1, 1))
                            except NoSuchElementException:
                                break
                            break
                    driver.back()
                    sleep(2 + random.uniform(-1, 1))
                    driver.back()
                    sleep(2 + random.uniform(-1, 1))
            if page != total - 1:
                driver.find_element_by_link_text(str(page + 2)).click()
                sleep(2 + random.uniform(-1, 1))
    driver.close()


if __name__ == '__main__':
    scrape()
