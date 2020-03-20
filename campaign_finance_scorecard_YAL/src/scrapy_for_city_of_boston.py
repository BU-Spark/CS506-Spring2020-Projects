from selenium import webdriver
from time import sleep
import random

from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome(executable_path='./chromedriver')
# ['Real Estate', 'Construction', 'Building', 'Property', 'Property Management', 'Surveyor', 'Civil Engineer']
keywords = ['real estate']

for keyword in keywords:
    rst = []
    driver.get('https://www.cityofboston.gov/cityclerk/dbasearch/Default.aspx')
    sleep(2 + random.uniform(-1, 1))
    driver.find_element_by_id('business_name').send_keys(keyword)
    # driver.find_element_by_id('type_of_business').send_keys(keyword)
    driver.find_element_by_id('btnSubmit').click()
    sleep(2 + random.uniform(-1, 1))
    total = driver.find_element_by_id('RadGrid1_ctl00').find_elements_by_tag_name('strong')
    total = int(total[1].text)
    for _ in range(total):
        table = driver.find_element_by_id('RadGrid1_ctl00')
        for item in table.find_elements_by_class_name('item'):
            all_info = item.text
            all_info = all_info.split('\n')
            try:
                info = [all_info[1].split(': ')[1].replace(',', ' ').lower(),
                        all_info[0].split(': ')[1].replace(',', ' ').lower(),
                        all_info[5].split(': ')[1].replace(',', ' ').lower()]
            except IndexError:
                info = [all_info[1].split(': ')[1].replace(',', ' ').lower(),
                        all_info[0].split(': ')[1].replace(',', ' ').lower(),
                        '']
            rst.append(info)
        for item in table.find_elements_by_class_name('alternatingItem'):
            all_info = item.text
            all_info = all_info.split('\n')
            try:
                info = [all_info[1].split(': ')[1].replace(',', ' ').lower(),
                        all_info[0].split(': ')[1].replace(',', ' ').lower(),
                        all_info[5].split(': ')[1].replace(',', ' ').lower()]
            except IndexError:
                info = [all_info[1].split(': ')[1].replace(',', ' ').lower(),
                        all_info[0].split(': ')[1].replace(',', ' ').lower(),
                        '']
            rst.append(info)
        table.find_element_by_class_name('rgPageNext').click()
        sleep(2 + random.uniform(-1, 1))
    with open('./data/' + keyword + '.csv', 'w') as file:
        file.write('file number,name,type\n')
        for i in rst:
            file.write(i[0] + ',' + i[1] + ',' + i[2] + '\n')
driver.close()
