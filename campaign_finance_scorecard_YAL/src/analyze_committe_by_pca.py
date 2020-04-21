import csv

data = []
all_data = csv.reader(open('D:/506_final/pac/pac_ocpf.csv'))
for i in all_data:
    data.append(i)

needed = []
for i in data:
    if i[9] == '17105':
        needed.append(i)

info = {}
for i in needed:
    try:
        info[i[5].upper()] += float(i[7])
    except:
        info[i[5].upper()] = float(i[7])

sum = 0
for key in info.keys():
    print(key + ":\t\t" + str(info[key]))
    sum += info[key]
print(sum)
