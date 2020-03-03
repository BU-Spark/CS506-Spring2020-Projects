from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#System.setProperty("webdriver.chrome.marionette","/usr/local/bin/chromedriver");

#os.environ["webdriver.chrome.driver"] = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome()  

driver.get('http://www.yahoo.com')
print("source code: ", driver.page_source[0:500])

assert 'Yahoo' in driver.title

elem = driver.find_element_by_name('p')  # Find the search box
elem.send_keys('selceniumhq' + Keys.RETURN)

#driver.quit()
