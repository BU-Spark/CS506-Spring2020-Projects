# Importing required libraries
import requests 
import json
import pandas as pd 
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
from uszipcode import SearchEngine

def convertZip(zipStr):
    """
        convert '2138.0' to '02138'
        """
    zipCode = ''
    if zipStr is not None:
        if '.' in zipStr:
            zipCode = '0' + zipStr[:4]
    return zipCode



# =============================================================================
# Google Places API Find nearby places
# =============================================================================
def get_nearby_places(lat, long, business_type, next_page, radius=805):
    #api_key = #You'll need your own API key: https://developers.google.com/places/web-service/get-api-key
    business_types = ['transit_station']
    URL = ('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='
		+lat+','+long+'&radius='+str(radius)+'&key='+ api_key +'&type='
		+business_type+'&pagetoken='+next_page)
    r = requests.get(URL)
    response = r.text
    python_object = json.loads(response)
    print(python_object)
    results = python_object["results"]
    for result in results:
        place_name = result['name']
        place_id = result['place_id']
        geometry = result['geometry']
        location = geometry['location']
        lat_i = location['lat']
        lng_i = location['lng']
        print([business_type, place_name,lat_i,lng_i])
        total_results.append([place_id, business_type, place_name, lat_i, lng_i])
    try:
        next_page_token = python_object["next_page_token"]
        time.sleep(1)
        print('here')
        get_nearby_places(lat, long, business_type, next_page_token, radius=805)
    except KeyError:
        #no next page
        return



def getNumTransitStops(df):
    #initialize variables to store location proximity information
    numTransitStops = [-1 for i in range(len(geoLocations))]
    # get number of nearby transit stops within 1/2 mile
    for index, row in df.iterrows():
        lat = str(row['latitude'])
        long = str(row['longitude'])
        print('Finding ',i,'th stops')
        if lat != 'None' and long != 'None':
            time.sleep(1)
            total_results = []
            get_nearby_places(lat, long, business_types[0],'')
            # get number of nearby bus stops for ith location
            numTransitStops[i] = len(total_results)
    df['numTransitStops'] = numTransitStops
    # save final result as csv
    df = df[df['owner_name'].str.endswith('HOUSING AUTHORITY',na=False)==False]
    df.to_csv('transport_proximity.csv',index=False)
    return df

df = getNumTransitStops(df)

#Individual Parcels with the most stops
result_parcels = df.sort_values(by='numTransitStops',ascending = False)
print(tabulate(result_parcels[['muni','owner_name','longitude','latitude','numTransitStops']].head(),headers='keys', tablefmt='psql'))


#Municipalities with the most Stops
muni_parcels = df[['muni','numTransitStops']].groupby(['muni']).sum()
muni_parcels = muni_parcels.sort_values(by = 'numTransitStops', ascending = False)
print(tabulate(muni_parcels.head(),headers='keys', tablefmt='psql'))



