from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import os
import re
from operator import itemgetter
import pandas as pd
import numpy as np

#read data in batches,
def readfile(filename):
    # entries=os.listdir("data/")
    streets = []
    ownerNames=[]

    df = pd.read_csv(os.path.join("data/",filename))

    x = pd.DataFrame(df.owner_addr)
    y = pd.DataFrame(df.owner_name)
    z = pd.DataFrame(df.owner_city)
    q = pd.DataFrame(df.owner_stat)
    result = pd.concat([x,z,q,y], axis=1, join='inner')
    result = result.values.tolist()
    for row in result:
        streets.append(str(row[0])+" "+str(row[1])+" "+str(row[2]))
        ownerNames.append(str(row[3]))

    # print(list(zip(streets, ownerNames)))
    df["FullOwnerAddress"] = pd.DataFrame(streets)
    df["FullOwnerAddress"].fillna("",inplace=True)
    df["owner_name"] = pd.DataFrame(ownerNames)
    df["owner_name"].fillna("",inplace=True)
    print(df["FullOwnerAddress"].head)
    print(df.shape)
    return df

def matchOnName(x,agencylist,matchflag):
    # agencylist -> [(name,address)]
    highestscorematch= max([(fuzz.ratio(x,i),i) for (i,j) in agencylist],key=itemgetter(0))
    # print(highestscorematch)
    if highestscorematch[0]>50:
        matchflag.append(1)
        return highestscorematch[1]
    else:
        matchflag.append(0)
        return x

def matchOnAddress(x,agencylist,matchflag):
    # x is a row from the dataframe
    # print(x.head)
    address= x['FullOwnerAddress']
    originalName = x["std_name"]
    highestscorematch= max([(fuzz.ratio(address,j),i) for (i,j) in agencylist],key=itemgetter(0))
    if highestscorematch[0]>50:
        # print("address",address)
        print("find a match, name: ",highestscorematch[1])
        matchflag.append(1)
        return highestscorematch[1]
    else:
        matchflag.append(0)
        return originalName

def matchAgencyNames(filename,data):
    # print(data.columns.values)
    df = pd.read_csv(os.path.join("data/",filename),encoding = "ISO-8859-1")
    agency = pd.DataFrame(df.Agency)
    address = pd.DataFrame(df.Address)
    choice = pd.concat([agency,address],axis=1,join='inner')
    choice = choice.values.tolist()
    matchflag=[]
    #match names with agencynames if score>50 otherwise keep original names
    data['std_name']=data['std_name'].apply(lambda x: matchOnName(x,choice,matchflag))
    # data['std_name'] = data.apply(lambda x: matchOnAddress(x,choice,matchflag),axis=1)
    data['matchAgencyList']=pd.DataFrame(matchflag)

    # print(data['matchAgencyList'])
    print("Done")
    print(sum(matchflag))
    data.to_csv("./result/MatchWithAgencyNames.csv", index=False)

    return data



def compareOwnerNames(data):
    tuples = pd.concat([data["FullOwnerAddress"],data["owner_name"]],axis=1).values.tolist()
    curr=""
    backtrack=0    #keep track of index of the starting row to calculate score for name standardization
    prevaddr=tuples[0][0]
    for tup in range(1,len(tuples)):

        if(tuples[tup][0]!=prevaddr or tup==(len(tuples)-1)):
            # find owner name with highest score
            scores={}
            for i in range(backtrack,tup):
                if(tuples[i][1] not in scores):
                    scores[tuples[i][1]]=0
                else:
                    similarity=[(fuzz.ratio(tuples[i][1], x), x) for x in scores.keys()]
                    for score,name in similarity:
                        scores[name]+=score


            standardizeName=max(scores, key=scores.get)
            # print("standardize name",scores.keys())

            #standardize owner names in data
            if(max(scores.values())>0):
                for i in range(backtrack,tup):
                    tuples[i]=(tuples[i][0],standardizeName)

            #reset variables
            prevaddr=tuples[tup][0]
            backtrack=tup

    print("comparing owner names")
    # print(data["FullOwnerAddress"].head())
    # print(data["objectid"].head())
    df = pd.DataFrame(tuples,columns=['FullOwnerAddress',"std_name"])
    df.reset_index(drop=True, inplace=True)
    data.reset_index(drop=True, inplace=True)
    df = pd.concat([df, data["objectid"]],axis=1)
    # print(df["FullOwnerAddress"].head())
    # print("data",data["objectid"].head())
    # print("df", df['objectid'].head())
    result = data.merge(df, on=["objectid","FullOwnerAddress"])
    print("df",df.shape)
    print("data",data.shape)
    print("result",result.columns.values)
    print("result",result.shape)
    return result



def sort_streets(data):

    data["FullOwnerAddress"] = data["FullOwnerAddress"].apply(lambda x: cleanupStreet(x))
    data.sort_values(by=['FullOwnerAddress'],inplace=True)
    print(data.shape)
    return data

def cleanupStreet(street):

    regex = re.compile(
        r'(?P<prefix>^North\w*\s|^South\w*\s|^East\w*\s|^West\w*\s|^N\.?\s|^S\.?\s|^E\.?\s|^W\.?\s)?(?P<street>.*)',
        re.IGNORECASE
    )
    street_prefix=""
    street = street.strip()
    street_match = regex.search(street)
    if street_match.group('prefix'):
            street_prefix = street_match.group('prefix')

    street_root = street_match.group('street')
    return street_prefix +street_root
    
def extractStreetTuple(street):
    return (street[0][1],street[0][0])

def mergeFile(dataset1,dataset2):

    # print(dataset1.objectid.head())
    # dataset1.objectid=dataset1.objectid.astype(np.int64)
    # dataset2=dataset2.astype(object)
    # print("dataset1",dataset1.dtypes)
    result=dataset1.merge(dataset2,left_on="std_name",right_on="Agency")
    print(result.shape)

def mergeDatasetWithOtherTeam():
    dataset1=pd.read_csv("./data/usable_state_land.csv")
    dataset2=pd.read_csv("./data/TaylorTeamData.csv")
    dataset1.drop(dataset1.columns[[0, 1]], axis=1, inplace=True)
    dataset2.drop(dataset2.columns[[0]], axis=1, inplace=True)

    print("dataset1 shape",dataset1.shape)
    print("dataset2 shape",dataset2.shape)

    dataset1 = pd.concat([dataset1["objectid"], dataset1["std_name"],dataset1["FullOwnerAddress"]],axis=1)
    res=dataset2.merge(dataset1, on="objectid", how="outer")
    res.to_csv("./data/mergedDataset.csv",index=False)
    print("---------------------")
    print(res.shape)
    print(res.columns.values)
    # print("nan values",res["mapc_id"].isna())

def highlightdiffernce(row):
        print(row)

        color = 'white'
        if row["std_name"] != row["agency_name"]:
            print("not equal")
            color = 'yellow'

        return ['background-color: %s' % color]*len(row.values)

def main():
    # data=readfile("original_luc_gt_909.csv")
    # print("finished reading data")

    # streets=sort_streets(data)
    # print("finished sorted street")

    # data=compareOwnerNames(streets)
    # print("finished comparing owner names")

    # matchAgencyNames("MassGovernmentAgencyList.csv",data)


    mergeDatasetWithOtherTeam()

main()
