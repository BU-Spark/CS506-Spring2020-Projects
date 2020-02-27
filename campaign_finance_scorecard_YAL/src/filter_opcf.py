import pypyodbc

connecter = pypyodbc.win_connect_mdb(u'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' +
                       'D:/506_final/data/OCPF Donor data/campaign-finance-reports/campaign-finance-reports.mdb')
cur = connecter.cursor()

"""get all data"""
def get_all_data():
    cur.execute("select re.id, re.report_id, re.occupation, re.employer, re.first_name, re.last_name, "
                "re.date, re.amount, ma.full_name, ma.cpf_id, re.city, re.state, re.contributor_type "
                "from vUPLOAD_tCURRENT_RECEIPTS as re left join vUPLOAD_MASTER as ma "
                "on re.report_id = ma.report_id "
                "where date>='2016-01-01' and date<='2019-12-31' and occupation<>'' and employer<>''")
    list = cur.fetchall()
    print(len(list))
    with open('./temp_all.csv', 'w') as file:
        for rst in list:
            for i in rst:
                i = str(i).replace(',', '')
                file.write(i + ',')
            file.write('\n')

"""get data filtered by keywords"""
def get_filtered_data():
    keywords_occupation = ["Realtor", "Contractor", "Builder", "Carpenter", "Painter",
                           "Architect", "Developer", "Planner", "Environmental Reviewer", "Surveyor"]
    keywords_employer = ["Real Estate", "Construction", "Building", "Property",
                         "Property Management", "Surveyor", "Civil Engineering",]
    keywords_PACS = ['Greater Boston Real Estate Board', 'Real Estate Bar Association for MA', 'NAIOP MA']

    strr = "select re.id, re.report_id, re.occupation, re.employer, re.first_name, re.last_name, " \
          "re.date, re.amount, ma.full_name, ma.cpf_id, re.city, re.state, re.contributor_type from vUPLOAD_tCURRENT_RECEIPTS as re left join vUPLOAD_MASTER as ma " \
          "on re.report_id = ma.report_id where date>='2016-01-01' and date<='2019-12-31' and occupation<>'' and employer<>'' and ("
    for ocp in keywords_occupation:
        strr += "occupation like '%" + ocp + "%' or "
    for emp in keywords_employer:
        strr += "employer like '%" + emp + "%' or "
    for i in range(len(keywords_PACS)-1):
        strr += "employer like '%" + keywords_PACS[i] + "%' or "
    strr += "employer like '%" + keywords_PACS[len(keywords_PACS)-1] + "%')"
    cur.execute(strr)
    list = cur.fetchall()
    print(len(list))

    with open('./temp_keywords.csv', 'w') as file:
        for rst in list:
            for i in rst:
                i = str(i).replace(',', '')
                file.write(i + ',')
            file.write('\n')

# get_all_data()
get_filtered_data()





