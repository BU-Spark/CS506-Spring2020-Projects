from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import os
import re
from operator import itemgetter
import pandas as pd

#read data in batches,
def readfile():
    entries=os.listdir("data/")
    streets = []
    ownerNames=[]
    for entry in entries:
        # f2=open("NameAndAddress.txt","w")
        with open(os.path.join("data/",entry),'r') as f:
            # for line in f.readlines()[1:]:
            #     line=line.split(",");
            #
            #     #ignore rows with empty owner address or owner names
            #     if(line[31]!='""' and line[30]!='""' and len(line[31])!=0 and len(line[30])!=0):
            #
            #         if (len(line[31]) != 0):
            #             index = 31
            #             st = line[31]
            #             while (True):
            #                 if (len(line[index + 1]) != 0):
            #                     if (line[index + 1][0] == " "):
            #                         st += line[index + 1]
            #                     else:
            #                         break
            #                 index += 1
            #             st+=" "+line[index+1]+" "+line[index+2]
            #             streets.append(st)
            #
            #         if(len(line[30])!=0):
            #             index=30
            #             name=line[30]
            #             while(True):
            #                 if(len(line[index+1])!=0):
            #                     if(line[index+1][0]==" "):
            #                         name+=line[index+1]
            #                     else:
            #                         break
            #                 index+=1
            #             ownerNames.append(name)
            df = pd.read_csv(os.path.join("data/",entry))
            x = pd.DataFrame(df.owner_addr)
            y = pd.DataFrame(df.owner_name)
            z = pd.DataFrame(df.owner_city)
            q = pd.DataFrame(df.owner_stat)
            result = pd.concat([x,z,q,y], axis=1, join='inner')
            result = result.values[:3000].tolist()
            for row in result:
                streets.append(str(row[0])+" "+str(row[1])+" "+str(row[2]))
                ownerNames.append(row[3])

        # read only 1 file so far
        break
        f.close()

    # for i in range(len(streets)):
    #     f2.write(streets[i]+ "             "+ownerNames[i]+"\n")

    # f2.close()
    print(list(zip(streets, ownerNames)))
    return list(zip(streets, ownerNames))

def compareOwnerNames(tuples):
    curr=""
    choice=[tuples[0][1]]
    backtrack=0
    prevaddr=tuples[0][0]
    for tup in range(1,len(tuples)):
        # build up choice list
        if(tuples[tup][0]==prevaddr):
            choice.append(tuples[tup][1])
        if(tuples[tup][0]!=prevaddr or tup==(len(tuples)-1)):
            # find owner name with highest score
            scores={}
            for i in range(backtrack,tup):
                if(tuples[i][1] not in scores):
                    scores[tuples[i][1]]=0
                else:
                    if(process.extractOne(tuples[i][1],choice)!=None):
                        scores[tuples[i][1]]+=process.extractOne(tuples[i][1],choice)[1]
                    # print(process.extractOne(tuples[i][1],choice)[1])
            standardizeName=max(scores, key=scores.get)
            # print("standardize name",scores.keys())

            #standardize owner names in data
            if(max(scores.values())>0):
                for i in range(backtrack,tup):
                    tuples[i]=(tuples[i][0],standardizeName)

            #reset variables
            prevaddr=tuples[tup][0]
            backtrack=tup
            choice=[]

    # print(tuples)
    f = open("CleanONResult.txt", "w")
    for key,val in tuples:
        f.write(key+ "             "+val+"\n")
    f.close()

    return tuples



def sort_streets(street_list):
    """
    Sort streets alphabetically, ignoring cardinal direction prefixes such as North, South, East and West
    :param street_list: list of street names
    """
    # compile a sorted list to extract the direction prefixes and street root from the street string
    # created using https://regex101.com/#python
    regex = re.compile(
        r'(?P<prefix>^North\w*\s|^South\w*\s|^East\w*\s|^West\w*\s|^N\.?\s|^S\.?\s|^E\.?\s|^W\.?\s)?(?P<street>.*)',
        re.IGNORECASE
    )

    # list to store tuples for sorting
    street_sort_list = []

    # for every street
    counter=0
    for street in street_list:
        street_prefix=""
        # just in case, strip leading and trailing whitespace
        street = street[0].strip()

        # extract the prefix and street using regular expression matching
        street_match = regex.search(street)

        # convert both the returned strings to lowercase
        if street_match.group('prefix'):
            street_prefix = street_match.group('prefix')

        street_root = street_match.group('street')

        # print(street_root)
        # print(street_prefix)

        # place the prefix, street extract and full street string in a tuple and add it to the list
        street_sort_list.append(((street_prefix, street_root, street),list(map(itemgetter(1),street_list))[counter]))
        counter+=1

    # sort the streets first on street name, and second with the prefix to address duplicates
    street_sort_list.sort(key=extractStreetTuple, reverse=False)
    # print(street_list[1])
    # print(street_sort_list)

    # return just a list of sorted streets, using a list comprehension to pull out the original street name in order
    # return [street_tuple[2] for street_tuple in street_sort_list]
    return [(street_tuple[0][2],street_tuple[1]) for street_tuple in street_sort_list]

def extractStreetTuple(street):
    return (street[0][1],street[0][0])

def test(str):
    line=str.split(",")
    for each in line:
        if(each[0]!=" "):
            print(each[0])

def main():
    data=readfile()
    streets=sort_streets(data)
    # print(streets)
    # print(data)

    compareOwnerNames(streets)
    # testdata='""'
    # test(testdata)

main()
