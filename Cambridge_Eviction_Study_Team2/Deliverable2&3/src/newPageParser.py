from stringMatch import StringMatch
from bs4 import BeautifulSoup
import csv


class NewPageParser():
    def __init__(self, fp, soup_parser):
        self.s = BeautifulSoup(fp, soup_parser)     # BeautifulSoup object
        self.matcher = StringMatch()

    # Clean text
    def _clean(self, stri):

        sphere = str(stri)
        sphere = sphere.replace("\t", "").replace("\r", "").replace("\n", "")
        sphere = sphere.replace("\t", "").replace("\r", "").replace("\n", "")
        return sphere


    def getTable(self):
        #return self._clean(self.s.find(id="titleBar").get_text().split(" ")[0])

        t = self.s.find('tbody')
        #print(t)
        #table = self._clean(t)
        #print(t)

        res =[];

        table_rows = t.find_all('tr')

        with open("file.csv", 'w') as f:
            for tr in table_rows:
                td = tr.find_all('td')
                row = [self._clean(i.text) for i in td]

                res.append(row)
                print(row)
            csv.writer(f).writerows(res)





