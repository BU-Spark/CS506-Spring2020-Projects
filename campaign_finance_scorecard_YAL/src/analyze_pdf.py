from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
import os
import logging
from tqdm import tqdm
import csv


def read_pdf(pdf):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    process_pdf(rsrcmgr, device, pdf)
    device.close()
    content = retstr.getvalue()
    retstr.close()
    lines = str(content).split("\n")
    return lines


def handle(rst):
    name = ''
    business = ''
    for i in range(len(rst)):
        if 'Exact name' in rst[i]:
            tmp = rst[i].split(': ')
            name = tmp[1].lstrip().rstrip()
        elif 'The general character' in rst[i] or 'Briefly describe' in rst[i]:
            count = i + 1
            tmp = rst[count]
            while 'cid' in tmp or tmp == ' ' or tmp == '' or 'service, the service to be rendered:' in tmp:
                count += 1
                tmp = rst[count]
            business = tmp.lstrip().rstrip()
    return name, business


def write_csv(content, path):
    with open(path, 'w') as f:
        w = csv.writer(f)
        w.writerows(content.items())


if __name__ == '__main__':
    logging.propagate = False
    logging.getLogger().setLevel(logging.ERROR)
    path = './r'
    dirs = os.listdir(path)
    business = {}
    for file in tqdm(dirs):
        pdf = path + '/' + file
        with open(pdf, 'rb') as f:
            try:
                rst = read_pdf(f)
            except:
                continue
            if len(rst) == 1:
                continue
            info = handle(rst)
            try:
                a = business[info[0]]
            except KeyError:
                if info[0] == '' or info[1] == '':
                    continue
                business[info[0]] = info[1]
    write_csv(business, './r.csv')
    print(len(business))
