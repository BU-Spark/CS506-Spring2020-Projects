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

def do_geocode(address, locator, loop=0):
    try:
        time.sleep(1)
        return locator.geocode(address)
    except GeocoderTimedOut:
        if loop >=5:
            return None
        return do_geocode(address, locator, loop+1)


# =============================================================================
# read filtered dataframe csv file
# =============================================================================
df = pd.read_csv('/Users/taylorhazlett/Documents/spring2020/cs506/usable_std_land_std_agencies.csv')
df =  df.loc[:,df.columns]
df.sort_values(by=['objectid'])

# Update dataset to maintain lat_long columns.
lat_long = pd.read_csv('/Users/taylorhazlett/Documents/spring2020/cs506/CS506-Spring2020-Projects/State-Surplus-TeamTaylor/data/state_land_plus_long_lat.csv')
lat_long = lat_long.sort_values(by=['objectid'])

df['longitude'] = lat_long['longitude']
df['latitude'] = lat_long['latitude']

#clean zipcode
addressZip = df['addr_zip']
addressZip = addressZip.astype(str)
addressZip = addressZip.apply(convertZip)
df['addr_zip'] = addressZip


# clean address column
address = df['addr_str']
df['addr_str'] = address.astype(str)

# =============================================================================
# Google Places API Find nearby places
# =============================================================================
#api_key = #You'll need your own API key: https://developers.google.com/places/web-service/get-api-key
business_types = ['transit_station']


def get_nearby_places(lat, long, business_type, next_page, radius=805):
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

#initialize variables to store location proximity information
numTransitStops = [-1 for i in range(len(geoLocations))]

# get number of nearby transit stops within 1/2 mile
for i in range(len(geoLocations)):
    lat = str(geoLocations[i][0])
    long = str(geoLocations[i][1])
    print('Finding ',i,'th stops')
    if lat != 'None' and long != 'None':
        time.sleep(1)
        total_results = []
        get_nearby_places(lat, long, business_types[0],'')
        # get number of nearby bus stops for ith location
        numTransitStops[i] = len(total_results)

# =============================================================================
# Google API: find average distance to bus, subway, train stops
# =============================================================================
# calculate average distance to different stations within 1/2 mile
def get_avg_distance(lat, long, business_type, next_page,radius=805):
    URL = ('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='
		+lat+','+long+'&radius='+str(radius)+'&key='+ api_key +'&type='
		+business_type+'&pagetoken='+next_page)
    r = requests.get(URL)
    response = r.text
    python_object = json.loads(response)
    results = python_object["results"]
    for result in results:
        geometry = result.get('geometry')
        location = geometry.get('location')
        lat_i = float(location.get('lat'))
        lng_i = float(location.get('lng'))
        distance = calculateDistance(float(lat), float(long), lat_i, lng_i)
        if distance >= 0:
            avg_distance.append(distance)
    try:
        next_page_token = python_object["next_page_token"]
        time.sleep(1)
        get_avg_distance(lat, long, business_type, next_page_token, radius=805)
    except KeyError:
		#no next page
        return


# =============================================================================
# Append avg distance to stations within 1/2 mile on the final dataframe
# =============================================================================
df['numTransitStops'] = numTransitStops

# save final result as csv
df.to_csv('transport_proximity.csv',index=False)

df = df[df['owner_name'].str.endswith('HOUSING AUTHORITY',na=False)==False]
print(df.shape)

#Individual Parcels with the most stops
result_parcels = df.sort_values(by='numTransitStops',ascending = False)
print(tabulate(result_parcels[['muni','owner_name','longitude','latitude','numTransitStops']].head(),headers='keys', tablefmt='psql'))


#Municipalities with the most Stops
muni_parcels = df[['muni','numTransitStops']].groupby(['muni']).sum()
muni_parcels = muni_parcels.sort_values(by = 'numTransitStops', ascending = False)
print(tabulate(muni_parcels.head(),headers='keys', tablefmt='psql'))



