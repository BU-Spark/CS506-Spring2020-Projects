import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import numpy as np
from csv import reader
from csv import writer
import statistics

with open('State_gender_preds.csv', 'r') as state, open('quincy.csv', 'r') as quincy, open('lowell.csv', 'r') as lowell, open('Worcester.csv', 'r') as worcester, open('NB.csv', 'r') as nb, open('all_data+race.csv', 'a') as all_data:
    state_reader = reader(state)
    lowell_reader = reader(lowell)
    quincy_reader = reader(quincy)
    worcester_reader = reader(worcester)
    nb_reader = reader(nb)
    all_writer = writer(all_data)

    all_writer.writerow(['Gender', 'Race', 'Salary'])
    count = 0

    greater_european=['GreaterEuropean,British', 'GreaterEuropean,EastEuropean', 'GreaterEuropean,WestEuropean,French','GreaterEuropean,WestEuropean,Germanic','GreaterEuropean,WestEuropean,Nordic', 'GreaterEuropean,WestEuropean,Italian']
    jewish=['GreaterEuropean,Jewish']
    greater_african=['GreaterAfrican,Africans', 'GreaterAfrican,Muslim']
    hispanic=['GreaterEuropean,WestEuropean,Hispanic']
    east_asian=['Asian,GreaterEastAsian,EastAsian', 'Asian,GreaterEastAsian,Japanese']
    indian_subcontinent=['Asian,IndianSubContinent']


    for line0 in state_reader:
        if count == 0:
            count += 1
        else:
            race = line0[21]
            gender = line0[20]
            salary = line0[7]
            if race in greater_european:
                all_writer.writerow([gender, 'Greater European', salary])
            elif race in jewish:
                all_writer.writerow([gender, 'Jewish', salary])
            elif race in greater_african:
                all_writer.writerow([gender, 'Greater African', salary])
            elif race in hispanic:
                all_writer.writerow([gender, 'Hispanic', salary])
            elif race in east_asian:
                all_writer.writerow([gender, 'East Asian', salary])
            elif race in indian_subcontinent:
                all_writer.writerow([gender, 'Indian Subcontinent', salary])
            else:
                all_writer.writerow([gender, 'ERROR', salary])        
    print("state done")
    count = 0

    for line1 in lowell_reader:
        if count == 0:
            count += 1
        else:
            race = line1[7]
            gender = line1[21]
            salary = line1[0].replace(',', '')
            if race in greater_european:
                all_writer.writerow([gender, 'Greater European', salary])
            elif race in jewish:
                all_writer.writerow([gender, 'Jewish', salary])
            elif race in greater_african:
                all_writer.writerow([gender, 'Greater African', salary])
            elif race in hispanic:
                all_writer.writerow([gender, 'Hispanic', salary])
            elif race in east_asian:
                all_writer.writerow([gender, 'East Asian', salary])
            elif race in indian_subcontinent:
                all_writer.writerow([gender, 'Indian Subcontinent', salary])
            else:
                all_writer.writerow([gender, 'ERROR', salary]) 
    print("lowell done")
    count = 0

    for line2 in quincy_reader:
        if count == 0:
            count += 1
        else:
            race = line2[7]
            gender = line2[21]
            salary = line2[0].replace(',', '')
            if race in greater_european:
                all_writer.writerow([gender, 'Greater European', salary])
            elif race in jewish:
                all_writer.writerow([gender, 'Jewish', salary])
            elif race in greater_african:
                all_writer.writerow([gender, 'Greater African', salary])
            elif race in hispanic:
                all_writer.writerow([gender, 'Hispanic', salary])
            elif race in east_asian:
                all_writer.writerow([gender, 'East Asian', salary])
            elif race in indian_subcontinent:
                all_writer.writerow([gender, 'Indian Subcontinent', salary])
            else:
                all_writer.writerow([gender, 'ERROR', salary]) 
    print("quincy done")
    count = 0

    for line3 in worcester_reader:
        if count == 0:
            count += 1
        else:
            race = line3[7]
            gender = line3[21]
            salary = line3[0].replace(',', '')
            if race in greater_european:
                all_writer.writerow([gender, 'Greater European', salary])
            elif race in jewish:
                all_writer.writerow([gender, 'Jewish', salary])
            elif race in greater_african:
                all_writer.writerow([gender, 'Greater African', salary])
            elif race in hispanic:
                all_writer.writerow([gender, 'Hispanic', salary])
            elif race in east_asian:
                all_writer.writerow([gender, 'East Asian', salary])
            elif race in indian_subcontinent:
                all_writer.writerow([gender, 'Indian Subcontinent', salary])
            else:
                all_writer.writerow([gender, 'ERROR', salary]) 
    print("worcester done")
    count = 0

    for line4 in nb_reader:
        if count == 0:
            count += 1
        else:
            race = line4[7]
            gender = line4[21]
            salary = line4[0].replace(',', '')
            if race in greater_european:
                all_writer.writerow([gender, 'Greater European', salary])
            elif race in jewish:
                all_writer.writerow([gender, 'Jewish', salary])
            elif race in greater_african:
                all_writer.writerow([gender, 'Greater African', salary])
            elif race in hispanic:
                all_writer.writerow([gender, 'Hispanic', salary])
            elif race in east_asian:
                all_writer.writerow([gender, 'East Asian', salary])
            elif race in indian_subcontinent:
                all_writer.writerow([gender, 'Indian Subcontinent', salary])
            else:
                all_writer.writerow([gender, 'ERROR', salary]) 
    print("nb done")
    count = 0

    print("DONE")





