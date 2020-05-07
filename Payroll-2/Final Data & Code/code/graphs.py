import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import numpy as np
from csv import reader
import statistics


with open('finalData/all_data+race.csv', 'r') as read_file:
    csv_reader = reader(read_file)
    count = 0
    x = {'gem': [], 'gef': [], 'jm': [], 'jf': [], 'gam': [], 'gaf': [], 'hm': [], 'hf': [], 'eam': [], 'eaf': [], 'ism': [], 'isf': []}
    for line in csv_reader:
        if count != 0:
            salary=float(line[2])
            if line[0] == 'male':
                if line[1] == 'Greater European':
                    x['gem'].append(salary)
                if line[1] == 'Jewish':
                    x['jm'].append(salary)
                if line[1] == 'Greater African':
                    x['gam'].append(salary)
                if line[1] == 'Hispanic':
                    x['hm'].append(salary)
                if line[1] == 'East Asian':
                    x['eam'].append(salary)
                if line[1] == 'Indian Subcontinent':
                    x['ism'].append(salary)
            if line[0] == 'female':
                if line[1] == 'Greater European':
                    x['gef'].append(salary)
                if line[1] == 'Jewish':
                    x['jf'].append(salary)
                if line[1] == 'Greater African':
                    x['gaf'].append(salary)
                if line[1] == 'Hispanic':
                    x['hf'].append(salary)
                if line[1] == 'East Asian':
                    x['eaf'].append(salary)
                if line[1] == 'Indian Subcontinent':
                    x['isf'].append(salary)
        count += 1

    gem = statistics.mean(x['gem'])
    gef = statistics.mean(x['gef'])
    jm = statistics.mean(x['jm'])
    jf = statistics.mean(x['jf'])
    gam = statistics.mean(x['gam'])
    gaf = statistics.mean(x['gaf'])
    hm = statistics.mean(x['hm'])
    hf = statistics.mean(x['hf'])
    eam = statistics.mean(x['eam'])
    eaf = statistics.mean(x['eaf'])
    ism = statistics.mean(x['ism'])
    isf = statistics.mean(x['isf'])

    gemn = len(x['gem'])
    gefn = len(x['gef'])
    jmn = len(x['jm'])
    jfn = len(x['jf'])
    gamn = len(x['gam'])
    gafn = len(x['gaf'])
    hmn = len(x['hm'])
    hfn = len(x['hf'])
    eamn = len(x['eam'])
    eafn = len(x['eaf'])
    ismn = len(x['ism'])
    isfn = len(x['isf'])


    objects = ('Greater European Male', 'Greater European Female', 'Jewish Male', 'Jewish Female', 'Greater African Male', 'Greater African Female', 'Hispanic Male', 'Hispanic Female', 'East Asian Male', 'East Asian Female', 'Indian Subcontinent Male', 'Indian Subcontinent Female')
    y_pos = np.arange(len(objects))
    avgSalary = [gem, gef, jm, jf, gam, gaf, hm, hf, eam, eaf, ism, isf]
    num = [gemn, gefn, jmn, jfn, gamn, gafn, hmn, hfn, eamn, eafn, ismn, isfn]
    print(avgSalary)
    print(num)

    plt.barh(y_pos, avgSalary, align='center', alpha=0.5)
    plt.yticks(y_pos, objects)
    plt.xlabel('Average Yearly Salary')
    plt.ylabel('Race and Gender')
    plt.title('Average Salary by Race and Gender')

    plt.show()


with open('finalData/all_data.csv', 'r') as read_file:
    csv_reader = reader(read_file)
    count = 0
    x = {'male': [], 'female': []}
    for line in csv_reader:
        if count != 0:
            salary=float(line[1])
            if line[0] == 'male':
                x['male'].append(salary)
            if line[0] == 'female':
                x['female'].append(salary)
        count += 1

    avgSalaryF = len(x['female'])
    avgSalaryM = len(x['male'])

    objects = ('Male', 'Female')
    y_pos = np.arange(len(objects))
    avgSalary = [avgSalaryM, avgSalaryF]
    print(avgSalary)

    plt.barh(y_pos, avgSalary, align='center', alpha=0.5)
    plt.yticks(y_pos, objects)
    plt.xlabel('Number of Employees')
    plt.ylabel('Gender')
    plt.title('Number of Police Employees by Gender')

    plt.show()



