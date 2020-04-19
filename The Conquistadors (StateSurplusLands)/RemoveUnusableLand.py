import pandas as pd
import geopandas as gpd
from geopandas.tools import geocode
from geopy.geocoders import Nominatim
from shapely.geometry import Point, Polygon
import numpy as np
from pyproj import Proj, transform


def getlat(address):
    geolocator = Nominatim()
    location=geolocator.geocode(address)
    try:
        lat = str(location.latitude)
    except:
        lat = 'NA'
    return lat

def getlong(address):
    geolocator = Nominatim()
    location=geolocator.geocode(address)
    try:
        long = str(location.longitude)
    except:
        long = 'NA'
    return long

#Convert lat,long to epsg 4326 format
def convertToMassGISCoordinate(x,y):
    inProj = Proj('epsg:4326', preserve_units = True)
    outProj = Proj('epsg:26986')
    x2,y2 = transform(inProj,outProj,x,y)
    return (x2,y2)

#false indicate no, true indicate yes
def checkIfAddressInWater(x,polygons):
    return any([True for i in polygons if x.within(i)])


hydro = gpd.read_file("./data/census2000hydro_poly/census2000hydro_poly.shp")
polygons = hydro["geometry"]
print(polygons.crs)
print(hydro.columns.values)
print(polygons.head())
print(polygons.shape)

data=pd.read_csv("./result/AttomEstimateResult.csv")

data["address"] = data["address"].astype(str)+", USA"
data['latitude'] = data['address'].apply(lambda x: getlat(x))
data['longitude'] = data['address'].apply(lambda x: getlong(x))

data['point'] = data.apply(lambda x:Point(convertToMassGISCoordinate(float(x["latitude"]),float(x["longitude"]))) if (x["latitude"]!='NA' and x["longitude"]!='NA') else np.nan,axis=1)
data['removable']=data['point'].apply(lambda x: checkIfAddressInWater(x,polygons.tolist()) if not np.isnan(x).all() else np.nan)
print(data['point'])
print(data['removable'])
