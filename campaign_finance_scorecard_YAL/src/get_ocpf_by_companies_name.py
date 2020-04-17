import pypyodbc
import csv
from tqdm import tqdm

all_data = csv.reader(open('D:/506_final/companies_name/NAIOP/naiop.csv', encoding='utf-8'))

connecter = pypyodbc.win_connect_mdb(u'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' +
                                     'D:/506_final/data/OCPF Donor data/campaign-finance-reports/campaign-finance-reports.mdb')
cur = connecter.cursor()

open('D:/506_final/companies_name/NAIOP/naiop_ocpf.csv', 'w')

for i in all_data:
    if i[0] == '':
        continue

    i[0] = i[0].replace("'", "''")

    try:
        cur.execute("select re.id, re.report_id, re.occupation, re.employer, re.first_name, re.last_name, "
                    "re.date, re.amount, ma.full_name, ma.cpf_id, re.city, re.state, re.contributor_type "
                    "from vUPLOAD_tCURRENT_RECEIPTS as re left join vUPLOAD_MASTER as ma "
                    "on re.report_id = ma.report_id "
                    "where date>='2016-01-01' and date<='2019-12-31'"
                    "and re.employer='" + i[0] + "' or re.last_name='" + i[0] + "'")
        list = cur.fetchall()
    except:
        print(i[0])
        continue

    if len(list) == 0:
        continue

    with open('D:/506_final/companies_name/NAIOP/naiop_ocpf.csv', 'a+', newline='') as file:
        out_file = csv.writer(file)
        for q in list:
            out_file.writerow(q)
