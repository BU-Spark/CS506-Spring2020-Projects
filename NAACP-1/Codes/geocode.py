import logging
import pandas as pd
import requests
import numpy as np
import requests

BingMapsAPIKey = "Ag9OGZ8tuL2y_uhT0cKaTg-tuS4wocFWrEmWaIWCcfcMoLC5_2Jma00ZhRVoT0XK"

pcode = []
nbhd  = []
countys = []
cities = []
la_lng = pd.read_csv('tract_lat_lng.csv')

# def get_zipcode(lat, lng):
for i in range(len(la_lng)):
    lat = la_lng['LATITUDE'][i]
    lng = la_lng['LONGITUDE'][i]
    loc = str(lat) + ',' + str(lng)

    fields= ['Zipcode', 'Neighborhood', 'County', 'City']
    df = pd.DataFrame(columns = fields)
    search_url = "http://dev.virtualearth.net/REST/v1/Locations/" + loc + "?includeEntityTypes=Neighborhood,Postcode1&includeNeighborhood=1" + "&key=" + BingMapsAPIKey

    response = requests.get(search_url)
    # if response.status_code == 200:
    #     print('Success!')
    # elif response.status_code == 404:
    #     print('Not Found.')

    search_result = response.json()

    if search_result['resourceSets'][0]:
        try:
            loc_res = search_result['resourceSets'][0]['resources'][0]['address']
            zipcode = loc_res["postalCode"]
            neighborhood = loc_res["neighborhood"]
            city = loc_res["locality"]
        except:
            pass
            #
        pcode.append(zipcode)
        nbhd.append(neighborhood)
        cities.append(city)


df["Zipcode"] = ["'"+str(x) for x in pcode]
df["Neighborhood"] = nbhd
df["City"] = cities

df.to_csv('zipDone.csv', index = False, header = True)
