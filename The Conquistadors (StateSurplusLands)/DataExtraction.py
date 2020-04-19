import http.client
import json
import pandas as pd
import time
import datetime
from config.config import key

"""use Attom API to retreive information about a property"""
ApiCallCounts=0
lastmin=""

"""return property profile in json format given address"""
def GetPropertyDetails(address="street,city,state"):
    global ApiCallCounts
    global lastmin
    print("getdetails")
    print("last min",lastmin)
    print("curr time",GetCurrMinute())
    print("count",ApiCallCounts)

    if(ApiCallCounts>=10):
        time.sleep(60)
        ApiCallCounts=0
        lastmin=GetCurrMinute()

    address = address.replace(" ","%20").split(",")
    """need to have the full address(street, city, state)"""
    address1 = address[0]
    address2 = address[1]+"%2C"+address[2]

    conn = http.client.HTTPSConnection("api.gateway.attomdata.com")
    payload = ''
    headers = {
      'accept': "application/json",
      'apikey': key
    }
    # conn.request("GET", "/propertyapi/v1.0.0/property/basicprofile?address1=4529%20Winona%20Court&address2=Denver%2C%20CO", headers=headers)
    conn.request("GET", "/propertyapi/v1.0.0/property/basicprofile?address1="+address1+"&address2="+address2, headers=headers)
    ApiCallCounts+=1

    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    return data.decode('utf-8')

"""get [latitude,longitude] from property profile"""
def GetLatLong(profile="json"):
    profile=json.loads(profile)
    return [profile.get("property")[0].get("location").get("latitude"),profile.get("property")[0].get("location").get("longitude")]


"""return list of areas in json format"""
def GetAreas(lat="lat",long="long"):
    print("get areas")
    global ApiCallCounts
    global lastmin
    if(ApiCallCounts>=10):
        time.sleep(60)
        ApiCallCounts=0
        lastmin=GetCurrMinute()

    conn = http.client.HTTPSConnection("api.gateway.attomdata.com")
    headers = {
        'accept': "application/json",
        'apikey': key
    }
    conn.request("GET", "/areaapi/v2.0.0/hierarchy/lookup?latitude="+str(lat)+"&longitude="+str(long),headers=headers)
    ApiCallCounts+=1

    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    return data.decode('utf-8')

"""take in areas in json format and return [ids] for neighborhoods"""
def GetNeighborhoodID(areas="json"):
    areas = json.loads(areas)
    list = areas.get("response").get("result").get("package").get("item")

    """only retrieve CS (County Subdivision -- aka -- Town) neighborhood areas"""
    
    for area in list:
        if area.get("type")=="CS":
            # ids.append(area.get("id"))
            return area.get("id")


def GetNeighborhoodInfo(id=""):
    print("GetNeighborhoodInfo")
    global ApiCallCounts
    global lastmin
    if(ApiCallCounts>=10):
        time.sleep(60)
        ApiCallCounts=0
        lastmin=GetCurrMinute()

    conn = http.client.HTTPSConnection("api.gateway.attomdata.com")
    headers = {
        'accept': "application/json",
        'apikey': key
    }
    conn.request("GET", "/communityapi/v2.0.0/Area/Full?AreaId="+id,headers=headers)
    ApiCallCounts+=1

    res = conn.getresponse()
    data = res.read()
    data = json.loads(data)
    price=data.get("response").get("result").get("package").get("item")[0].get("avgsaleprice")
    # print(price)
    # print(data.decode("utf-8"))
    return price

def RetrievePropertyValuesHelper(x):
    # print(x["FullOwnerAddress"])
    # address=x["owner_addr"]+", "+x["owner_city"]+", "+x["owner_stat"]
    address=x
    print(address)
    profile=GetPropertyDetails(address)
    profileJson=json.loads(profile)
    if(profileJson.get("property")!=None):
        if(len(profileJson.get("property"))>0):
            coord=GetLatLong(profile)
            ID=GetNeighborhoodID(GetAreas(coord[0],coord[1]))
            return GetNeighborhoodInfo(ID)
    return -1


def GetCurrMinute():
    return str(datetime.datetime.now().time()).split(":")[1]

def RetrievePropertyValues():
    global lastmin
    lastmin = GetCurrMinute()

    data = pd.read_csv("./result/MatchWithAgencyAddresses.csv")
    data = data[data["matchAgencyList"]==1]
    address = data.apply(lambda x: x["owner_addr"]+", "+x["owner_city"]+", "+x["owner_stat"],axis=1)
    address=address.drop_duplicates()
    address = pd.DataFrame(address,columns=["address"])
    print(address.shape)
    address['avgsaleprice'] = address.apply(lambda x: RetrievePropertyValuesHelper(x["address"]),axis=1)
    address.to_csv("./result/AttomEstimateResult.csv",index=False)
    
    # data.merge(address,how='left',on=[""])

    # data.to_csv("./result/AvgPriceForAddressInList.csv",index=False)


# coord=GetLatLong(GetPropertyDetails("10 park plaza,boston,MA"))
# GetNeighborhoodID(GetAreas(coord[0],coord[1]))
# GetNeighborhoodInfo("CO44003")

RetrievePropertyValues()

# print(str(datetime.datetime.now().time()))
