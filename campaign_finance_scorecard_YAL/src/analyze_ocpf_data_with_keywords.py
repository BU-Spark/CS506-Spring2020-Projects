import matplotlib.pyplot as plt

def get_filtered_data_real(filename):
    data = []
    keywords_occupation = ["Realtor", "Contractor", "Builder", "Carpenter", "Painter",
                           "Architect", "Developer", "Planner", "Environmental Reviewer", "Surveyor"]
    keywords_employer = ["Real Estate", "Construction", "Building", "Property",
                         "Property Management", "Surveyor", "Civil Engineer"]
    keywords_PACS = ['Greater Boston Real Estate Board', 'Real Estate Bar Association for MA', 'NAIOP MA']

    with open(filename) as file:
        for line in file:
            temp = []
            line = line.replace('\n', '')
            line = line.split(',')
            for i in line:
                temp.append(i)
            flag = False
            for occupation in keywords_occupation:
                if occupation.lower() in line[2].lower():
                    temp.append('occupation')
                    temp.append(occupation.lower())
                    data.append(temp)
                    flag = True
                    break
            if not flag:
                for employer in keywords_employer:
                    if employer.lower() in line[3].lower():
                        temp.append('employer')
                        temp.append(occupation.lower())
                        data.append(temp)
                        flag = True
                        break
            if not flag:
                for pac in keywords_PACS:
                    if pac.lower() in line[3].lower():
                        temp.append('pac')
                        temp.append(occupation.lower())
                        data.append(temp)
                        break
    # with open('./raw_real_estate.csv', 'w') as file:
    #     for d in data:
    #         for i in d:
    #             file.write(i + ',')
    #         file.write('\n')
    return data

def get_all(filename):
    data = []
    with open(filename) as file:
        for line in file:
            temp = []
            line = line.replace('\n', '')
            line = line.split(',')
            for i in line:
                temp.append(i)
            data.append(temp)
    return data

def get_filtered_health(filename):
    data = []
    keywords_occupation = ['Nurse','Doctor','Physician','MD',
                           'Medical','Hospital','Clinical','RN',
                           'Patient','Health','Patient']
    keywords_employer = ['Hospital','Health','Healthcare','Medical']

    with open(filename) as file:
        for line in file:
            temp = []
            line = line.replace('\n', '')
            line = line.split(',')
            for i in line:
                temp.append(i)
            flag = False
            for occupation in keywords_occupation:
                if occupation.lower() in line[2].lower():
                    temp.append('occupation')
                    temp.append(occupation.lower())
                    data.append(temp)
                    flag = True
                    break
            if not flag:
                for employer in keywords_employer:
                    if employer.lower() in line[3].lower():
                        temp.append('employer')
                        temp.append(employer.lower())
                        data.append(temp)
                        flag = True
                        break
    # with open('./raw_real_estate.csv', 'w') as file:
    #     for d in data:
    #         for i in d:
    #             file.write(i + ',')
    #         file.write('\n')
    return data

def get_filtered_data_law(filename):
    data = []
    keywords_occupation = ['President', 'Provost', 'Dean']
    keywords_employer = ['College', 'University']
    keywords_PACS = []

    with open(filename) as file:
        for line in file:
            temp = []
            line = line.replace('\n', '')
            line = line.split(',')
            for i in line:
                temp.append(i)
            flag = False
            for occupation in keywords_occupation:
                if occupation.lower() in line[2].lower():
                    temp.append('occupation')
                    temp.append(occupation.lower())
                    data.append(temp)
                    flag = True
                    break
            if not flag:
                for employer in keywords_employer:
                    if employer.lower() in line[3].lower():
                        temp.append('employer')
                        temp.append(occupation.lower())
                        data.append(temp)
                        flag = True
                        break
            if not flag:
                for pac in keywords_PACS:
                    if pac.lower() in line[3].lower():
                        temp.append('pac')
                        temp.append(occupation.lower())
                        data.append(temp)
                        break
    with open('./raw_law.csv', 'w') as file:
        for d in data:
            for i in d:
                file.write(i + ',')
            file.write('\n')
    return data

def compute_amount_by_cpfid(data):
    cpf_id = {}
    for row in data:
        try:
            try:
                cpf_id[(row[9].upper(), row[8].upper())] += float(row[7])
            except KeyError:
                cpf_id[(row[9].upper(), row[8].upper())] = float(row[7])
        except ValueError:
            print(row)
    cpf_id = sorted(cpf_id.items(), key=lambda x:x[1])
    sum = 0
    for key in cpf_id:
        sum += key[1]
        print(key[0][0] + ": " + key[0][1] + ": " + str(key[1]))
    print(sum)
    # with open('./temp_amount.csv', 'w') as file:
    #     for key in cpf_id:
    #         file.write(key[0][0] + ',' + key[0][1] + ',' + str(key[1]) + ',')
    #         file.write('\n')

def compute_amount_by_cpfid_v2(ind_data, data):
    import numpy as np
    value = []
    id = '15563'
    for row in data:
        if row[9] == id:
            value.append(float(row[7]))
    a = np.array(value).sum()
    print(a)
    for row in ind_data:
        if row[9] == id:
            value.append(float(row[7]))
    value = np.array(value)
    print(value.sum())
    print(value.sum() - a)
    print(value.mean())
    print(value.std())

def compute_amount_by_cpfid_v3(data):
    import numpy as np
    value = []
    id = '17105'
    for row in data:
        if row[9] == id:
            value.append(float(row[7]))
    value = np.array(value)
    print(value.sum())
    print(value.mean())
    print(value.std())

def get_season_index(date):
    date_splited = date.split('-')
    if(date_splited[1] >= '01' and date_splited[1] <='03'):
        return 0
    elif (date_splited[1] >= '04' and date_splited[1] <= '06'):
        return 1
    elif (date_splited[1] >= '07' and date_splited[1] <= '09'):
        return 2
    elif (date_splited[1] >= '10' and date_splited[1] <= '12'):
        return 3
    else:
        raise ValueError()

def compute_amount_by_season(data, com_data):
    res = {}
    for row in data:
        try:
            res[get_season_index(row[6])] += float(row[7])
        except KeyError:
            res[get_season_index(row[6])] = float(row[7])
    num_list = []
    lable_list = []
    for item in res.items():
        print(str(item[0]) + ": " + str(item[1]))
        lable_list.append(item[0])
        num_list.append(item[1])

    com_res = {}
    for row in com_data:
        try:
            com_res[get_season_index(row[6])] += float(row[7])
        except KeyError:
            com_res[get_season_index(row[6])] = float(row[7])
    com_num_list = []
    com_lable_list = []
    for item in com_res.items():
        print(str(item[0]) + ": " + str(item[1]))
        com_lable_list.append(item[0])
        com_num_list.append(item[1])

    total_width, n = 0.8, 2
    width = total_width / n
    x = list(range(len(num_list)))
    plt.bar(x, num_list, width=width, tick_label=lable_list, fc='b', label='individual')
    for i in range(len(x)):
        x[i] = x[i] + width
    plt.bar(x, com_num_list, width=width, tick_label=com_lable_list, fc='r', label='committee')
    plt.legend()
    plt.show()
    return

def compute_amount_by_year(data, com_data):
    res = {}
    for row in data:
        try:
            res[row[6].split('-')[0]] += float(row[7])
        except KeyError:
            res[row[6].split('-')[0]] = float(row[7])
    num_list = []
    lable_list = []
    for item in res.items():
        print(str(item[0]) + ": " + str(item[1]))
        lable_list.append(item[0])
        num_list.append(item[1])

    com_res = {}
    for row in com_data:
        try:
            com_res[row[6].split('-')[0]] += float(row[7])
        except KeyError:
            com_res[row[6].split('-')[0]] = float(row[7])
    com_num_list = []
    com_lable_list = []
    for item in com_res.items():
        print(str(item[0]) + ": " + str(item[1]))
        com_lable_list.append(item[0])
        com_num_list.append(item[1])

    total_width, n = 0.8, 2
    width = total_width / n
    x = list(range(len(num_list)))
    plt.bar(x, num_list, width=width, tick_label=lable_list, fc='b', label='individual')
    for i in range(len(x)):
        x[i] = x[i] + width
    plt.bar(x, com_num_list, width=width, tick_label=com_lable_list, fc='r', label='committee')
    plt.legend()
    plt.show()
    return


def computer_amount_by_size(data, com_data):
    size = {}
    amount = {}
    for i in range(6):
        size[i] = 0
        amount[i] = 0.
    for entry in data:
        if float(entry[7]) < 25:
            size[0] += 1
            amount[0] += float(entry[7])
        elif 25 <= float(entry[7]) < 100:
            size[1] += 1
            amount[1] += float(entry[7])
        elif 100 <= float(entry[7]) < 250:
            size[2] += 1
            amount[2] += float(entry[7])
        elif 250 <= float(entry[7]) < 500:
            size[3] += 1
            amount[3] += float(entry[7])
        elif 500 <= float(entry[7]) < 1000:
            size[4] += 1
            amount[4] += float(entry[7])
        else:
            size[5] += 1
            amount[5] += float(entry[7])

    com_size = {}
    com_amount = {}
    for i in range(6):
        com_size[i] = 0
        com_amount[i] = 0.
    for entry in com_data:
        if float(entry[7]) < 25:
            com_size[0] += 1
            com_amount[0] += float(entry[7])
        elif 25 <= float(entry[7]) < 100:
            com_size[1] += 1
            com_amount[1] += float(entry[7])
        elif 100 <= float(entry[7]) < 250:
            com_size[2] += 1
            com_amount[2] += float(entry[7])
        elif 250 <= float(entry[7]) < 500:
            com_size[3] += 1
            com_amount[3] += float(entry[7])
        elif 500 <= float(entry[7]) < 1000:
            com_size[4] += 1
            com_amount[4] += float(entry[7])
        else:
            com_size[5] += 1
            com_amount[5] += float(entry[7])
    print(amount)
    print(com_amount)


    lable_list = ['<$25', '$25-$99', '$100-$249', '$250-$499', '$500-$1000', '>$1000']
    plt.bar(range(len(amount)), amount.values(), tick_label=lable_list)
    plt.show()

    total_width, n = 0.8, 2
    width = total_width / n
    x = list(range(len(amount)))
    plt.bar(x, amount.values(), width=width, tick_label=lable_list, fc='b', label='individual')
    for i in range(len(x)):
        x[i] = x[i] + width
    plt.bar(x, com_amount.values(), width=width, tick_label=lable_list, fc='r', label='committee')
    plt.legend()
    plt.show()



def computer_amount_by_city(data, com_data):
    res = {}
    for row in data:
        try:
            res[row[10].lower()] += float(row[7])
        except KeyError:
            res[row[10].lower()] = float(row[7])
    city = sorted(res.items(), key=lambda x: x[1])
    for key in city:
        print(key[0] + ": " + str(key[1]))
    print(len(city))
    com_res = {}
    for row in com_data:
        try:
            com_res[row[10].lower()] += float(row[7])
        except KeyError:
            com_res[row[10].lower()] = float(row[7])
    com_city = sorted(com_res.items(), key=lambda x: x[1])
    for key in com_city:
        print(key[0] + ": " + str(key[1]))
    print(len(com_city))
    return

def computer_amount_by_state(data, com_data):
    res = {}
    for row in data:
        try:
            res[row[11].upper()] += float(row[7])
        except KeyError:
            res[row[11].upper()] = float(row[7])
    state = sorted(res.items(), key=lambda x: x[1])
    distributions = [0, 0]
    for key in state:
        print(key[0] + ": " + str(key[1]))
        if key[0].upper() == 'MA':
            distributions[0] += key[1]
        else:
            distributions[1] += key[1]
    print(len(state))
    print("in state: " + str(distributions[0]))
    print("out of state: " + str(distributions[1]))

    com_res = {}
    for row in com_data:
        try:
            com_res[row[11].upper()] += float(row[7])
        except KeyError:
            com_res[row[11].upper()] = float(row[7])
    com_state = sorted(com_res.items(), key=lambda x: x[1])
    com_distributions = [0, 0]
    for key in com_state:
        print(key[0] + ": " + str(key[1]))
        if key[0].upper() == 'MA':
            com_distributions[0] += key[1]
        else:
            com_distributions[1] += key[1]
    print(len(com_state))
    print("in state: " + str(com_distributions[0]))
    print("out of state: " + str(com_distributions[1]))
    return

def computer_amount_by_contributor_type(data, com_data):
    res = {}
    for row in data:
        try:
            res[row[12].lower()] += float(row[7])
        except KeyError:
            res[row[12].lower()] = float(row[7])

    for row in com_data:
        try:
            res[row[12].lower()] += float(row[7])
        except KeyError:
            res[row[12].lower()] = float(row[7])

    for key in res.items():
        print(key[0] + ": " + str(key[1]))
    return

def import_com_data():
    import csv
    data = []
    all_data = csv.reader(open('D:/506_final/ocpf_data/pac_ocpf.csv'))
    for i in all_data:
        data.append(i)
    return data

def import_law_data():
    import csv
    data = []
    all_data = csv.reader(open('D:/506_final/raw_law.csv'))
    for i in all_data:
        data.append(i)
    return data


def import_law_pac():
    import csv
    data = []
    all_data = csv.reader(open('D:/506_final/ocpf_data/law_pac.csv'))
    for i in all_data:
        data.append(i)
    return data


def import_health_pac():
    import csv
    data = []
    all_data = csv.reader(open('D:/506_final/ocpf_data/health_pac.csv'))
    for i in all_data:
        data.append(i)
    return data


def the_most(data):
    import numpy as np
    name = {}
    company = {}
    name_total = {}
    company_total = {}
    for i in data:
    #     cur_name = i[4] + ' ' + i[5]
    #     cur_name = cur_name.upper()
        cur_com = i[3].upper()
        # try:
        #     name[cur_name] += float(i[7])
        # except KeyError:
        #     name[cur_name] = float(i[7])
        # try:
        #     name_total[cur_name].append(float(i[7]))
        # except KeyError:
        #     name_total[cur_name] = [float(i[7])]
        if cur_com == 'NONE' or cur_com == 'AT HOME' or cur_com == 'HOMEMAKER':
            continue
        if cur_com == 'SELF' or cur_com == 'SELF EMPLOYED':
            cur_com = 'SELF-EMPLOYED'
        try:
            company[cur_com] += float(i[7])
        except KeyError:
            company[cur_com] = float(i[7])
        try:
            company_total[cur_com].append(float(i[7]))
        except KeyError:
            company_total[cur_com] = [float(i[7])]
    # name = sorted(name.items(), key=lambda x: x[1], reverse=True)
    # company = sorted(company.items(), key=lambda x: x[1], reverse=True)
    # for i in name[:10]:
    #     total = np.array(name_total[i[0]])
    #     print(i[0] + " " + str(i[1]) + " " + str(total.mean()) + " " + str(total.std()))
    # print()
    company_average = {}
    company_number = {}
    for key in company_total.keys():
        company_average[key] = np.array(company_total[key]).mean()
        company_number[key] = len(company_total[key])
    company_average = sorted(company_average.items(), key=lambda x: x[1], reverse=True)
    company_number = sorted(company_number.items(), key=lambda x: x[1], reverse=True)
    for i in company_average[:10]:
        print(i[0] + " " + str(i[1]))
    print('')
    for i in company_number[:10]:
        print(i[0] + " " + str(i[1]))


def companies_insight(data):
    import numpy as np
    compnies = {}
    names = {}
    for i in data:
        cur_com = i[3].upper()
        reciver_id = int(i[9])
        names[reciver_id] = i[8]
        if cur_com == 'NONE' or cur_com == 'AT HOME' or cur_com == 'HOMEMAKER':
            continue
        if cur_com == 'SELF' or cur_com == 'SELF EMPLOYED':
            cur_com = 'SELF-EMPLOYED'
        try:
            compnies[cur_com][reciver_id].append(float(i[7]))
        except KeyError:
            try:
                compnies[cur_com][reciver_id] = [float(i[7])]
            except KeyError:
                compnies[cur_com] = {reciver_id: [float(i[7])]}
    for key in compnies:
        donor = compnies[key]
        for id in donor:
            if len(donor[id]) > 1000:
                total = np.array(donor[id])
                print(key + ", " + names[id] + ", " + str(len(donor[id])) + ", " + str(total.sum()))
    print(' ')
    for key in compnies:
        if len(compnies[key]) > 100:
            print(key + ", " + str(len(compnies[key])))



ind_data = get_filtered_data_law('./temp_all.csv')
compute_amount_by_cpfid(ind_data)
#data = get_filtered_data_law('./temp_all.csv')
# com_data = import_health_pac()
# compute_amount_by_cpfid(com_data)
# data = get_all('./temp_all.csv')
# compute_amount_by_cpfid_v3(data)
# compute_amount_by_season(ind_data, com_data)
# compute_amount_by_year(ind_data, com_data)
# computer_amount_by_size(ind_data, com_data)
# computer_amount_by_city(ind_data, com_data)
# computer_amount_by_state(ind_data, com_data)
# computer_amount_by_contributor_type(ind_data, com_data)
