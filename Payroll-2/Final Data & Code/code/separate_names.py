import csv

filename = 'Worcester.csv'

occupations = ['Captain', 'Sergeant', 'Police', 'Officer', 'Commissioner', 'Lieutenant', 'Patrol', 'Sheriff', 'Chief']

with open(filename) as oldfile, open('Worcester_split_names.csv','w') as newfile:
    writer=csv.writer(newfile) # create one csv writer object
    reader=csv.reader(oldfile)
    for c,row in enumerate(reader): # read through input csv
        if c==0:                            # first row is the header
            header=row[:]
            del header[4]       # delete 'address'
            header[4:4]=['First_Name', 'Last_Name'] # insert these column names
            writer.writerow(header)                  # write column names to csv
        else:                                               # for all other input rows, except the first
            full_name=[i.strip() for i in row[4].split(' ')] # split the address by space
            names=[full_name[0], full_name[1]]
            del row[4]                                             
            row[4:4]=names
            if any(job in row[2] for job in occupations):
                writer.writerow(row)