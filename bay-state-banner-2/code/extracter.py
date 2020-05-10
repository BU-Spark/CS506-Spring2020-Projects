from PyPDF2 import PdfFileReader
import re
from tika import parser
import csv
import os
import numpy as np

def flat(l):
    for k in l:
        if not isinstance(k, (list, tuple)):
            yield k
        else:
            yield from flat(k)


def get_info(path,outPath):
    addresses = re.compile("Street address of the corporation's principal office:.*?[0-9A-Za-z,\n].*[\s\S][0-9A-Za-z,\n].*[\s\S][0-9A-Za-z,\n].*")
    company_name=re.compile("Exact name of the corporation:.*?[0-9A-Za-z,\n\-].*")
    agent_address = re.compile("agent at that office:.*?[0-9A-Za-z,\n].*[\s\S][0-9A-Za-z,\n].*[\s\S][0-9A-Za-z,\n].*[\s\S][0-9A-Za-z,\n].*")
    descrption=re.compile("Briefly describe the business of the corporation:.*?[0-9A-Za-z,\n\-].*[\s\S][0-9A-Za-z,\n].*")
    title=re.compile("and chief financial officer. .*?[0-9A-Za-z,\n\-].*[\s\S][0-9A-Za-z,\n].*",re.DOTALL)

    raw = parser.from_file(path)
    address_matches = addresses.findall(raw['content'])
    cn_matches=company_name.findall(raw['content'])
    ag_matches=agent_address.findall(raw['content'])
    descrption_matches=descrption.findall(raw['content'])
    title_matches=title.findall(raw['content'])

    #cn_matches=''.join(cn_matches)[32:]
    #address_matches=''.join(address_matches)[55:].replace("6. Provide the name and addresses of the corporation's board of directors and its president, treasurer,","")
    #ag_matches=''.join(ag_matches)[21:].replace("5. Street address of the corporation's principal office:","")
    #descrption_matches=''.join(descrption_matches)[54:]
    #cn_matches=''.join(cn_matches).replace("Exact name of the corporation:  ", "")
    #descrption_matches=''.join(descrption_matches).replace("Briefly describe the business of the corporation:","")

    #print(address_split)
    print(address_matches)
    print(cn_matches)
    print(ag_matches)
    print(descrption_matches)
    print(title_matches)
    print(len(address_matches))
    print(len(cn_matches))

    
    with open(outPath, 'a',newline='') as f:
        writer = csv.writer(f,dialect='excel')
        writer.writerows(zip(cn_matches,address_matches,ag_matches,descrption_matches))
    

def fileTotxt(fileDir):
    files=os.listdir(fileDir)
    tarDir=fileDir+'csv'
    if not os.path.exists(tarDir):
        os.mkdir(tarDir)
    #replace=re.compile(r'\.pdf',re.I)
    for file in files:
        filePath=fileDir+'\\'+file
        outPath=tarDir+'\\'+'n.csv'
        get_info(filePath,outPath)
        print("Saved ")

if __name__ == '__main__':
    #path = 'CorpSearchViewPDF - 2020-03-19T142507.771.pdf'
    #get_info(path)
    fileTotxt("./extracter")