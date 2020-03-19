from selenium import webdriver
from time import sleep
import random
from bs4 import BeautifulSoup


def scrape():
    alphas = ['p', 'q', 'r']

    for alpha in alphas:
        driver = webdriver.Chrome(executable_path='D:\\506_final\\phantomjs-2.1.1-windows\\bin\\chromedriver.exe')
        driver.get("http://lgwhd2o.x.incapdns.net/CorpWeb/CorpSearch/CorpSearch.aspx")
        sleep(2 + random.uniform(-1, 1))
        driver.find_element_by_id('MainContent_txtEntityName').send_keys(alpha)
        driver.find_element_by_id('MainContent_ddRecordsPerPage').send_keys('All items')
        html = driver.page_source
        soup = BeautifulSoup(html)
        table = soup.findAll('table', id='MainContent_SearchControl_grdSearchResultsEntity')
        tr_list = table[0].findAll('a')
        with open('./company_links/' + alpha, 'w') as file:
            for tr in tr_list:
                try:
                    file.write('http://lgwhd2o.x.incapdns.net/CorpWeb/CorpSearch/' + tr['href'] + '\n')
                except:
                    continue
        driver.close()


if __name__ == '__main__':
    scrape()
