from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
from selenium.common.exceptions import NoSuchElementException 

#System.setProperty("webdriver.chrome.marionette","/usr/local/bin/chromedriver");

#os.environ["webdriver.chrome.driver"] = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome()  





caseslist = ["http://masscases.com/425-449.html", "http://masscases.com/450-474.html", 
"http://masscases.com/475-499.html"]

cases = []


for c in caseslist: 
    driver.get(c)
    for sec in driver.find_elements_by_xpath( "/html/body/section/section"):
        for a in sec.find_elements_by_tag_name('a'):
            cases.append(a.get_attribute('href'))

applist = ["http://masscases.com/app50-74.html", "http://masscases.com/app75-99.html" ]

appeals = [] 
for l in applist:
    driver.get(l)
    for sec in driver.find_elements_by_xpath( "/html/body/section/section"):
        for a in sec.find_elements_by_tag_name('a'):
            appeals.append(a.get_attribute('href'))
not_handled = []
cases = cases[350:]
cases_des= []

for c in cases:
    driver.get(c)
    case_info = {} 
    try:
        name = driver.find_element_by_xpath( "/html/body/header/h1")
        case_info["case:"] = name.text[:-8]
    except NoSuchElementException:
        not_handled.append(c)
        continue
    try:
        header = driver.find_element_by_xpath( "/html/body/section[1]")
        case_info["header:"] = header.text
    except NoSuchElementException:
        not_handled.append(c)
        continue
    try:
        des = driver.find_element_by_xpath( "/html/body/section[2]")
        case_info["text"] = des.text
    except NoSuchElementException:
        not_handled.append(c)
        continue

    date = driver.find_element_by_xpath( "/html/body/header/h3")
    case_info["Date:"] = date.text
    print(date.text)

    try:
        county = driver.find_element_by_xpath( "/html/body/header/h4")
        county = county.text
    except NoSuchElementException:
        county = ""
    case_info["County:"] = county
    date_test = 0 
    if date.text[-1] == ".":
        date_test = int(date.text[-5:-1])
    else:
        date_test = int(date.text[-4:])
    if (date_test > 1999) and (date_test < 2009):
        cases_des.append(case_info)
    elif date_test == 2019:
        cases_des.append(case_info)
    else:
        continue



appeals_des= []
for a in appeals:
    driver.get(a)
    case_info = {} 
    try:
        name = driver.find_element_by_xpath( "/html/body/header/h1")
        case_info["case:"] = name.text[:-8]
    except NoSuchElementException:
        not_handled.append(c)
        continue
    try:
        header = driver.find_element_by_xpath( "/html/body/section[1]")
        case_info["header:"] = header.text
    except NoSuchElementException:
        not_handled.append(c)
        continue
    try: 
        des = driver.find_element_by_xpath( "/html/body/section[2]")
        case_info["text:"] = des.text
    except NoSuchElementException:
        not_handled.append(c)
        continue
    try: 
        date = driver.find_element_by_xpath( "/html/body/header/h3")
        case_info["Date:"] = date.text
    except:
        not_handled.append(c)
        continue 
    try:
        county = driver.find_element_by_xpath( "/html/body/header/h4")
        county = county.text
    except NoSuchElementException:
        county = ""
        case_info["County:"] = county
        continue
    date_test = 0 
    if date.text[-1] == ".":
        date_test = int(date.text[-5:-1])
    elif date.text[-1] == "]":
        date_test = int(date.text[-14:-10])
    else:
        date_test = int(date.text[-4:])
    if (date_test > 1999) and (date_test < 2009):
        appeals_des.append(case_info)
    elif date_test == 2019:
        appeals_des.append(case_info)
    else:
        continue
with open('cases_mass_new.json', 'w') as fout:
    json.dump(cases_des , fout, indent =2 )   

with open('appeal_mass_new.json', 'w') as fout:
    json.dump(appeals_des , fout, indent = 2 ) 


print( not_handled)

#/html/body/header/h1/text()
#elem = driver.find_element_by_name('p')  # Find the search box
#elem.send_keys('http://masscases.com/425-449.html' + Keys.RETURN)

driver.quit()
