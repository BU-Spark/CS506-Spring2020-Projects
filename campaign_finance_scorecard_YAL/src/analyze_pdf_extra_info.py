import pdfplumber
import os
import logging
from tqdm import tqdm
import csv
import re
import pandas as pd
import numpy as np

def print_result(pdf):
    for page in pdf.pages:
        for table in page.extract_tables():
            for row in table:
                print(row)
            print('----------------')
        print('page============')

def next_page_fist_line(pdf, page_num):
    res = ''
    if len(pdf.pages) - 1 > page_num:
        page = pdf.pages[page_num+1]
        tables = page.extract_tables()
        if not len(tables) == 0:
            res = tables[0][0][0]
    return res

def extract_address(col):
    tmp = col.split(':', 1)
    address = tmp[1].replace('\n', '')
    address = re.sub(' +', ' ', address)
    address = address.replace('No. and Street:', '')
    address = address.replace('City or Town:', ', ')
    address = address.replace('State:', ', ')
    address = address.replace('Zip:', ', ')
    address = address.replace('Country:', ', ')
    address = address.replace(' ,', ',')
    return address

def extract_adderss_name(col):
    tmp = col.split(':', 3)
    name = ''
    address = ''
    # if len(tmp) >= 4:
    name = tmp[2].replace('No. and Street', '')
    name = name.replace('\n', '')
    address = tmp[3].replace('\n', '')
    address = re.sub(' +', ' ', address)
    address = address.replace('City or Town:', ', ')
    address = address.replace('State:', ', ')
    address = address.replace('Zip:', ', ')
    address = address.replace('Country:', ', ')
    address = address.replace(' ,', ',')
    return name, address

def process_pdf(pdf):
    # print_result(pdf)
    all_info = []
    name = ''
    business = ''
    street_address = ''
    registered_agent_name = ''
    registered_agent_address = ''
    members = []
    office_address = ''
    for i in range(len(pdf.pages)):
        page = pdf.pages[i]
        str = next_page_fist_line(pdf, i)
        if(str == '' or str == ' ' or str[0].isdigit()):
            str = ''
        for j in range(len(page.extract_tables())):
            table = page.extract_tables()[j]
            for k in range(len(table)):
                row = table[k]
                if k == len(table) - 1:
                    if len(row) == 1:
                        row[0]  = row[0] + ' ' + str
                    elif not str == '':
                        row.append(str)
                for col in row:
                    if col == None:
                        continue
                    if 'Exact name' in col or 'exact name' in col:
                        tmp = col.split(': ')
                        name = tmp[1].lstrip().rstrip()
                        name_words = name.split(' ')
                        if len(name_words) > 10:
                            name = name.split('If')[0]
                    elif 'The general character' in col or 'Briefly describe' in col:
                        tmp = col.split(':')
                        business = tmp[1].lstrip().rstrip()
                    elif 'Location of its principal office' in col or 'corporation\'s principal office' in col:
                        office_address = extract_address(col)
                    elif 'registered agent at that office' in col or 'Resident Agent' in col:
                        registered_agent_name, registered_agent_address = extract_adderss_name(col)
                        if 'registered agent at that office' in col:
                            street_address = registered_agent_address
                    elif 'Street address of the office' in col:
                        street_address = extract_address(col)
        for table in page.extract_tables():
            if len(table) == 0 or not len(table[0]) == 3 :
                continue
            if table[0][0] == 'Title' and 'Individual Name' in table[0][1] and 'Address' in table[0][2]:
                for i in range(1, len(table)):
                    if not table[i][-1] == None:
                        table[i][-1] = table[i][-1].replace('\n', '')
                    members.append(table[i])
    pdf.close()

    # for i in range(len(members)):
    #     print(members[i])
    # print('name: ', name)
    # print('business: ', business)
    # print('street_address: ', street_address)
    # print('office_address: ', office_address)
    # print('registered_agent_name: ', registered_agent_name)
    # print('registered_agent_address: ', registered_agent_address)


    for i in range(len(members)):
        line_info = []
        line_info.append(name)
        line_info.append(street_address)
        line_info.append(office_address)
        line_info.append(registered_agent_name)
        line_info.append(business)
        for j in range(len(members[i])):
            line_info.append(members[i][j])
        all_info.append(line_info)
    return all_info


def write_csv(filename, data):
    with open(filename,'a+') as f:
        csv_write = csv.writer(f)
        csv_write.writerow(data)


if __name__ == '__main__':
    logging.propagate = False
    logging.getLogger().setLevel(logging.ERROR)
    write_path = './s.csv'
    path = './s'
    if os.path.exists(write_path):
        os.remove(write_path)

    dirs = os.listdir(path)
    title = [['Name of Corporation', 'Street Address', 'Street Address of Corporation Principal Office', 'Registered Agent',
             'Description', 'Member Title', 'Member Individual Name', 'Member Address']]
    title = pd.DataFrame(title)
    title.to_csv(write_path, header= False, index=False, mode='a+')
    # write_csv(write_path, title)
    count = 0
    for file in tqdm(dirs):
        # print(file)
        p = path + '/' + file
        try:
            pdf = pdfplumber.open(p)
        except:
            continue

        try:
            if len(pdf.pages[0].extract_tables()) == 0:
                continue
            info = process_pdf(pdf)
            data = pd.DataFrame(info)
            data.to_csv(write_path, header=False, index=False, mode='a+')
        except:
            count += 1
            print(file)
            continue
    print('error file: ', count)
        # data = np.concatenate((data, info), axis= 0)
        # print(data.shape)
