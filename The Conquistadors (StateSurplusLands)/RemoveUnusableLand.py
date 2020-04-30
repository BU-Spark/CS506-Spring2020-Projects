import pandas as pd
import geopandas as gpd
from geopandas.tools import geocode
from geopy.geocoders import Nominatim
from shapely.geometry import Point, Polygon
import numpy as np
from pyproj import Proj, transform
from geopy.extra.rate_limiter import RateLimiter
import time
from geopy.exc import GeocoderTimedOut

def getlat(address):
    try:
        geolocator = Nominatim()
        location = geolocator.geocode(address)
        lat = str(location.latitude)
    except:
        lat = 'NA'
    return lat

def getlong(address):
    try:
        geolocator = Nominatim()
        location = geolocator.geocode(address)
        long = str(location.longitude)
    except:
        long = 'NA'
    return long

def getlatlong(address,list):
    lat=""
    long=""
    try:
        geolocator = Nominatim()
        # geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
        location = geolocator.geocode(address,timeout=2)
        lat = str(location.latitude)
        long = str(location.longitude)
        print("find an address")
        list.append((lat, long))
    except GeocoderTimedOut:
        getlatlong(address,list)
    except:
        print("can't find address")
        long = 'NA'
        lat = 'NA'
        list.append((lat, long))
    time.sleep(1)
    # print(address)
    # print("lat long",(lat,long))


"""Convert lat,long to epsg 26986 format"""
def convertToMassGISCoordinate(x,y):
    inProj = Proj('epsg:4326', preserve_units = True)
    outProj = Proj('epsg:26986')
    x2,y2 = transform(inProj,outProj,x,y)
    return (x2,y2)

#false indicate no, true indicate yes
def checkIfAddressInWater(x,polygons):
    return any([True for i in polygons if x.within(i)])


"""remove addresses in unusable lands in 3 datasets:census2000hydro_poly, OPENSPACE_POLY,WETLANDSDEP_ORIG_POLY """
def removeUnusableLands(dataset):

    """get all water bodies"""
    polygons = gpd.read_file("./data/census2000hydro_poly/census2000hydro_poly.shp")["geometry"]

    """check for state owned conservation land"""
    polygons2 = gpd.read_file("./data/openspace/OPENSPACE_POLY.shp")
    polygons2 = polygons2[polygons2["OWNER_TYPE"]=="S"]["geometry"]

    """check for wet lands """
    polygons3 = gpd.read_file("./data/wetlandsdep_orig/wetlandsdep_orig/WETLANDSDEP_ORIG_POLY.shp")["geometry"]

    #print(polygons2.crs)
    #print(polygons2.columns.values)
    # print(polygons.head())
    # print(polygons3.shape)

    """read in our input dataset that we want to filter"""
    data=pd.read_csv("./result/"+dataset)
    print(data.shape)

    """convert valid addresses to point format"""
    data['address'] = data.apply(lambda x: str(x["owner_addr"])+", "+str(x["owner_city"])+", "+str(x["owner_stat"])+", USA",axis=1)
    address=pd.DataFrame(data['address'].drop_duplicates(),columns=['address'])
    data=address
    print("finished building addresses")


    latlong=[]
    data['address'].apply(lambda x: getlatlong(x,latlong))
    df = pd.DataFrame(latlong,columns=["latitude","longitude"])
    # print(df["latitude"])
    data['latitude'] = df["latitude"].tolist()
    # print(data['latitude'])
    data['longitude'] = df["longitude"].tolist()
    print("finished lat long")
    data['point'] = data.apply(lambda x:Point(convertToMassGISCoordinate(float(x["latitude"]),float(x["longitude"]))) if (x["latitude"]!='NA' and x["longitude"]!='NA') else np.nan,axis=1)
    print("finished converting to points")

    data['removable']=False
    data['removable']=data.apply(lambda x: any([checkIfAddressInWater(x['point'],polygons.tolist()),x['removable']]) if np.all(pd.notna(x)) else np.nan,axis=1)
    print("finished checking water bodies")
    data['removable']=data.apply(lambda x: any([checkIfAddressInWater(x['point'],polygons2.tolist()),x['removable']]) if np.all(pd.notna(x)) else np.nan,axis=1)
    print("finished checking conservation lands")
    data['removable']=data.apply(lambda x: any([checkIfAddressInWater(x['point'],polygons3.tolist()),x['removable']]) if np.all(pd.notna(x)) else np.nan,axis=1)
    print("finished checking wetlands")
    data.to_csv("./result/filter.csv",index=False)

"""merge dataset with the filter csv produced from checking if addresses are removable from above"""
def mergeFilterFileWithDataSet(dataset):

    data = pd.read_csv("./result/"+dataset)
    print("data shape",data.shape)
    filter = pd.read_csv("./result/filter.csv")
    print("filter shape",filter.shape)
    filter["address"] = filter["address"].apply(lambda x:  "".join(x.split(",")[:-1]))
    filter = filter.drop_duplicates(subset=["address"])
    filter= filter.rename(columns={"address":"FullOwnerAddress"})

    data=data.merge(filter, on="FullOwnerAddress",validate = 'm:1',how='left')
    data.to_csv("./result/FinalDataset.csv",index=False)
    print(data.shape)



removeUnusableLands("mergedDataset.csv")
mergeFilterFileWithDataSet("mergedDataset.csv")