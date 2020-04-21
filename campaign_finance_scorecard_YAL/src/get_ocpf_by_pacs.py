import pypyodbc
import csv

all_data = csv.reader(open('./pacs_name.csv'))
open('D:/506_final/pac/pac_ocpf.csv', 'w')
connecter = pypyodbc.win_connect_mdb(u'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' +
                                     'D:/506_final/data/OCPF Donor data/campaign-finance-reports/campaign-finance-reports.mdb')
cur = connecter.cursor()

for i in all_data:
    if i[0] != 'BT' and i[0] != 'RE':
        continue
    name = i[1]
    name = name.replace("'", "''")
    try:
        cur.execute("select re.id, re.report_id, re.occupation, re.employer, re.first_name, re.last_name, "
                    "re.date, re.amount, ma.full_name, ma.cpf_id, re.city, re.state, re.contributor_type "
                    "from vUPLOAD_tCURRENT_RECEIPTS as re left join vUPLOAD_MASTER as ma "
                    "on re.report_id = ma.report_id "
                    "where date>='2016-01-01' and date<='2019-12-31'"
                    "and re.last_name='" + name + "'")
        list = cur.fetchall()
    except:
        print(name)
        continue

    with open('D:/506_final/pac/pac_ocpf.csv', 'a+', newline='') as file:
        out_file = csv.writer(file)
        for q in list:
            out_file.writerow(q)

