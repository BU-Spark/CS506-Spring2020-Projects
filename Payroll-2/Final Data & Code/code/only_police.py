
from csv import writer
from csv import reader


with open('state.csv', 'r') as read_file, open('data/RegularData/State_police.csv', 'w', newline='') as write_file:
    csv_reader = reader(read_file)
    csv_writer = writer(write_file)
    count = 0
    keep = ['State Police Trooper', 'State Police Sergeant', 'State Police Trooper,1st Class', 'State Police, Trainee', 'Lieutenant', 'State Police Trooper,1St Class', 
    'Detective Lieutenant', 'Captain', 'Personnel Officer I', 'Detectives Captain', 'Lieutenant Colonel', 'Supv Identification Agent', 'Deputy Superintendent', 'Administrative Officer IV', 
    'Major', 'Personnel Officer II', 'Chief Science Officer', 'Superintendent', 'Deputy Chief Admin Officer', ]
    for line in csv_reader:
        if count == 0:
            csv_writer.writerow(line)
            count +=1
            print(line)
        elif line[3] == "DEPARTMENT OF STATE POLICE (POL)":
            if line[4] in keep:
                csv_writer.writerow(line)
                print(line)