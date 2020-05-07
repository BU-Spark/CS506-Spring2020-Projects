import requests
from csv import writer
from csv import reader

API_KEY = '1a4d90cf81ee714a36ca2dac341c903b'

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




with open('data/RegularData/NB2_race_preds.csv', 'r') as read_file, open('data/RegularData/finalData/NB.csv', 'a', newline='') as write_file:
    csv_reader = reader(read_file)
    csv_writer = writer(write_file)
    # head = False
    count = 0
    include= ['Police Officer - Quinn', 'Pol Officer-Nights-Quinn', 'Police Officer - Nights', 'Police Officer - Nights', 'Pol Officer-Night-Quinn', 'Police Captain - Days - Det', 'Police Officer', 'Police Sgt Nights', 'Asst Training Officer', 'Police Lt - Nights', 'Pol Lieutenant -Quinn', 'Deputy Police Chief', 'Police Chief', 'Police Officer - N', 'Police Cadet Apprentice', 'Police Cadet', 'Police Recruit', 'Compliance Officer', 'Pol Sergeant-nights', 'Police Off Det']
    for line in csv_reader:
        if count == 0:
            csv_writer.writerow(line)
            print(line)
            count += 1
        else:
            if line[2] in include:
                fname=line[4]
                lname=line[5]
                url= "https://v2.namsor.com/NamSorAPIv2/api2/json/gender/"
                url += fname
                url += '/'
                url += lname
                response = requests.get(url=url, headers={'Content-Type': 'application/json','X-API-KEY': API_KEY})
                data = response.json()
                gender = data["likelyGender"]
                line.append(gender)
                csv_writer.writerow(line)
                print(line)
        # if line == ['2015', 'Barry', 'Sean', 'DEPARTMENT OF STATE POLICE (POL)', 'State Police Trooper,1st Class', 'Full Time Employee', '12/26/2015', '145625.75', '104743.06', '0', '28857.69', '12025', '101010.52', '145625.75', '024741155', 'SPAM - MA State Police (5A)', '5A', 'SPAM - MA State Police', '16262974', 'POL']:
        #     head = True
    print("DONE")



            