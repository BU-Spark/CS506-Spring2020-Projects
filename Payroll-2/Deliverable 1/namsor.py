import requests
from csv import writer
from csv import reader

API_KEY = '71a0f7cbad8acc20d69d5e0da282d45a'

# with open('lowell.csv', 'r') as read_file, open('lowell_namsor.csv', 'w', newline='') as write_file:
#     csv_reader = reader(read_file)
#     csv_writer = writer(write_file)
#     for line in csv_reader:
#         if len(line) > 0:
#             name=line[0]
#             url= "https://v2.namsor.com/NamSorAPIv2/api2/json/genderFull/"
#             url += name
#             response = requests.get(url=url, headers={'Content-Type': 'application/json','X-API-KEY': API_KEY})
#             data = response.json()
#             gender = data["likelyGender"]
#             line.append(gender)
#             print(line)
#             csv_writer.writerow(line)


# with open('quincy.csv', 'r') as read_file, open('quincy_namsor.csv', 'w', newline='') as write_file:
#     csv_reader = reader(read_file)
#     csv_writer = writer(write_file)
#     count = 0
#     for line in csv_reader:
#         if len(line) > 0 and count >= 4162:
#             # print(line)
#             # break
#             name=line[0]
#             url= "https://v2.namsor.com/NamSorAPIv2/api2/json/genderFull/"
#             url += name
#             response = requests.get(url=url, headers={'Content-Type': 'application/json','X-API-KEY': API_KEY})
#             data = response.json()
#             gender = data["likelyGender"]
#             line.append(gender)
#             print(line)
#             csv_writer.writerow(line)
#         else:
#             count +=1




# with open('state2013.csv', 'r') as read_file, open('state2013_namsor.csv', 'w', newline='') as write_file:
#     csv_reader = reader(read_file)
#     csv_writer = writer(write_file)
#     # count = 0
#     here = False
#     for line in csv_reader:
#         if len(line) > 0 and line[3] == "DEPARTMENT OF STATE POLICE (POL)" and here:
#             fname=line[2]
#             lname=line[1]
#             url= "https://v2.namsor.com/NamSorAPIv2/api2/json/gender/"
#             url += fname
#             url += '/'
#             url += lname
#             response = requests.get(url=url, headers={'Content-Type': 'application/json','X-API-KEY': API_KEY})
#             data = response.json()
#             gender = data["likelyGender"]
#             line.append(gender)
#             csv_writer.writerow(line)
#             print(line)
#         if line == ['2016', 'Lee', 'Cheri', 'DEPARTMENT OF STATE POLICE (POL)', 'Procurement Mgr', 'Full Time Employee', '12/24/2016', '81829.55', '81829.55', '0', '0', '0', '81461.021', '81829.55', '017022203', 'Managers  (EXE) (M99)', 'M99', 'Managers  (EXE)', '14599065', 'POL']:
#             here = True
#         # else:
#         #     count +=1
#     print("DONE")




with open('state.csv', 'r') as read_file, open('state_police.csv', 'w', newline='') as write_file:
    csv_reader = reader(read_file)
    csv_writer = writer(write_file)
    for line in csv_reader:
        if line[3] == "DEPARTMENT OF STATE POLICE (POL)":
            csv_writer.writerow(line)
            print(line)
    print("DONE")




            