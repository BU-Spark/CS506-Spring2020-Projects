import os
from time import sleep
from selenium import webdriver


def download_nh_cases(download_dir, year_start, year_end):
    """
        download pdf from NH court website
        https://www.courts.state.nh.us/supreme/opinions
        into pdf_ri_cases folder

        :param: download_dir: the download directory
        :param: year_start: download starts from this year (no earlier than 1995)
        :param: year_end: download ends with this year (no later than 2019)

        e.g.
        download_nh_cases(my_download_dir, 2008, 2018) is to download cases from 2008 to 2018
        download_nh_cases(my_download_dir, 2010, 2010) is to download cases in 2010
    """

    # configure chrome webdriver
    prefs = {
        "download.default_directory": download_dir+"/year",
        "profile.default_content_settings.popups": 0,
        "plugins.always_open_pdf_externally": True
    }
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('prefs', prefs)
    browser = webdriver.Chrome(options=chrome_options)
    browser.get("https://www.courts.state.nh.us/supreme/opinions/")

    total_cases = 0

    for year in range(year_start, year_end+1):
        previous_years = browser.find_elements_by_xpath('//*[@id="content"]/div/ul[2]/li/a')

        # find the year to be downloaded in previous years
        for previous_year in previous_years:
            if previous_year.text == str(year):
                previous_year.click()
                sleep(1)

                # locate all elements of case
                if year == 2009:
                    cases = browser.find_elements_by_xpath('//*[@id="content"]/div/ul/li/span/a')
                else:
                    cases = browser.find_elements_by_xpath('//*[@id="content"]/div/ul/li/a')

                # record number of pdf files in this year
                with open(download_dir + "/download_log.txt", 'a') as download_log:
                    download_log.write(str(year) + " contains " + str(len(cases)) + " cases\n")
                total_cases += len(cases)

                # create a temporary folder for the downloaded pdfs files and pdfs_log
                if not os.path.exists(download_dir+"/year"):
                    os.makedirs(download_dir+"/year")
                # download each case of this year
                for n, case in enumerate(cases):
                    # record pdf number, filename, case title
                    with open(download_dir + "/year/pdfs_log.txt", 'a') as pdfs_log:
                        pdfs_log.write(str(n+1) + "\t" +
                                       case.get_attribute("href").split("/")[-1] + "\t" +
                                       case.text + "\n")
                    case.click()
                    sleep(1)

                os.rename(download_dir + "/year", download_dir + "/" + str(year))
                os.mkdir(download_dir + "/year")
                break

        browser.back()
        sleep(1)

    browser.close()

    if os.path.exists(download_dir + "/year"):
        os.rmdir(download_dir + "/year")

    with open(download_dir + "/download_log.txt", 'a') as download_log:
        download_log.write("\n" + str(total_cases) + " cases in total")


if __name__ == "__main__":

    # download to ../pdf_nh_cases
    my_download_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/pdf_nh_cases"
    # download cases from 2008 to 2018
    download_nh_cases(my_download_dir, 2008, 2018)
