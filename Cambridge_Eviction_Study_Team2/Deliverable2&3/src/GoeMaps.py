import csv
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import datetime
import time
import folium
from folium.plugins import HeatMap
import geopandas
import json
from shapely.geometry import Point
from shapely.geometry.multipolygon import MultiPolygon
import branca

def readData(filename): 
    
    data = pd.read_csv(filename)    
    return data

def addGeo(data):
    if 'latitude'  not in data.columns:
        data['latitude'] = 0.0
        data['longitude'] = 0.0
    print (data.head())
    geolocator = Nominatim(user_agent="Eviction")   
    starttime=time.time()
  
    #newData = pd.DataFrame(columns=['Address','GeoAddress', 'lattitude', 'longitude'])

    #df.loc[2176,'foo1'] = 'my_value'

    for index, row in data.iterrows(): 
        if row['latitude'] == 0.0:
            try: 
                if row['Property Address'] != None:
                    zz = getGeoAdress(row['Property Address'])
                    print(zz)
                    location = geolocator.geocode(zz)
                    print((location.latitude, location.longitude))
                    data.at[index, 'latitude'] = location.latitude
                    data.at[index, 'longitude'] = location.longitude
            except:
                print (row['Property Address'])
            time.sleep(1.0 - ((time.time() - starttime) % 1.0))
    print (data.head())
    data.to_csv('withLat1.csv')    

    

def generateBaseMap(defaultlocation=[42.373611,-71.110558]):
    """
    create base map
    :param defaultlocation:
    :return:
    """
    basemap = folium.Map(location=defaultlocation, zoom_start =14, tiles='Mapbox Bright')
    return basemap

def createMapPlot(df, districts_json):
    namestr = "peta"
    color=['blue']
    base_map=generateBaseMap()
    for i in range(0,len(df.index)):
        loc = [df.iloc[i]['latitude'], df.iloc[i]['longitude']]
        folium.Circle(radius=0.5,location=loc,color=color[0],fill=True).add_to(base_map)

    #folium.TopoJson(open('./FY2020_Residential_Districts/ASSESSING_ResidentialDistrictsFY2020.geojson'), object_path='objects.cambridge2020',
    #).add_to(base_map)

    """ base_map.choropleth(geo_path="./FY2020_Residential_Districts/ASSESSING_ResidentialDistrictsFY2020.geojson",
                        fill_opacity=0.5, 
                        line_opacity=0.5) """

    #districts = './FY2020_Residential_Districts/ASSESSING_ResidentialDistrictsFY2020.geojson'

    #districts_json = json.load(open(districts))
    #districts_json = geopandas.read_file(districts)
    print(districts_json.head())

    variable = 'eviction-count' 
    if variable  not in districts_json.columns:
        districts_json[variable] = 0.0

    for index, row in districts_json.iterrows(): 
        if row[variable] == 0.0:
            try: 
                dis = row['name']
                #print (dis)
                count  = df[df["DISTRICT"] == dis].count()['DISTRICT']
                districts_json.at[index, variable] = count 

            except:
                print ("Error")

    print(districts_json.head())
    dc = districts_json[['name',variable]].sort_values(by =variable, ascending = False)
    dc.reset_index(inplace = True)
    leg_brks = list(dc[dc.index.isin([0, 4, 9, 19, 29, 49, 79])][variable])
    leg_brks.append(0)
    leg_brks.sort()


    colorscale = setColor(min=districts_json[variable].min(), max=districts_json[variable].max(), 
    step = 7, quant =leg_brks)

    folium.GeoJson(
    districts_json,
    name='Eviction cases in the city of Cambridge',
    style_function= lambda x: {"weight":1,
                                'color' :'#545453',
                                'fillColor':'#9B9B9B' if x['properties'][variable] == 0 
                                else colorscale(x['properties'][variable]),
                                'fillOpacity' : 0.2 if x['properties'][variable] == 0 
                                else 0.7},
    highlight_function= lambda x: {"weight":3, 'color':'black', 'fillOpacity':0.9},
    tooltip= folium.features.GeoJsonTooltip(
        fields=['name', 'eviction-count'],
        aliases=['District No', '# Eviction']
    ),
    ).add_to(base_map)

    colorscale.add_to(base_map)

    base_map.save(namestr+".html")

def setColor(min=0, max = 1000, step = 17, quant =[]):
    variable ='DISTRICT',
    name = '# Eviction'

    colorscale = branca.colormap.linear.YlOrRd_09.scale(min, max)
    #print(colorscale)

    colorscale = colorscale.to_step(n = step, quantiles = quant)
    return colorscale

def getGeoAdress(add=" "):
    #st = '30 Union Street #3, Cambridge, MA        02141'
    a = add.split('        ')
    add = a[0]
    add1 = add.split(',')
    if '#' in add1[0]:
        add1[0] = add1[0].split('#')[0] 
    if 'Apt' in add1[0]:
        add1[0] = add1[0].split('Apt')[0] 
    if 'apt' in add1[0]:
        add1[0] = add1[0].split('apt')[0] 
    if 'Unit' in add1[0]:
        add1[0] = add1[0].split('Unit')[0] 
    if 'Suite' in add1[0]:
        add1[0] = add1[0].split('Suite')[0] 
    if 'Avenue' in add1[0]:
        add1[0] = add1[0].split('Avenue')[0] +' Avenue'
    if 'Street' in add1[0]:
        add1[0] = add1[0].split('Street')[0] +' Street'
    if 'Place' in add1[0]:
        add1[0] = add1[0].split('Place')[0] +' Place'
    if 'Park' in add1[0]:
        add1[0] = add1[0].split('Park')[0] +' Park'
    if 'Towers' in add1[0]:
        add1[0] = add1[0].split('Towers')[0] +' Towers'
    res = ''
    for b in add1:
        res = res +' '+b.strip().replace("  ", " ")
    return res


def chekInsidePolygon():
    point = Point(0.5, 0.5)
    #polygon = Polygon([(0, 0), (0, 1), (1, 1), (1, 0)])
    #print(polygon.contains(point))

def getRegions(point, regiondf):
   
    res = 0
    
    for index, row in regiondf.iterrows():
        print(row['geometry'])
        p = MultiPolygon(row['geometry'])
        print(p)
        if p.contains(point):
            res = row["name"]
            break
        print(res)
    return res

def addDistrict(data, districts):
    if 'DISTRICT'  not in data.columns:
        data['DISTRICT'] = ''
   

    for index, row in data.iterrows(): 
        if row['DISTRICT'] == '':
            #try: 
                if row['Property Address'] != None:
                   point = Point(float(data['longitude'].iloc[index]), float(data['latitude'].iloc[index]))
                   print(point)
                   data.at[index, 'DISTRICT'] = getRegions(point, districts)
            #except:
            #    print ("No data for "+ row['Property Address'])
    print (data.head())
    data.to_csv('withLatDistrict.csv')    

def InsertNoneExistingCoordinate(maindata, secdata):
    for index, row in maindata.iterrows(): 
        if row['DISTRICT'] == 0.0:
            try: 
                if row['Property Address'] != None:
                   df1 = secdata[secdata['Address'].str.contains(row['Property Address'].strip())]
                   print(df1.Lat.values[0])
                   maindata.at[index, 'latitude'] = df1.Lat.values[0]
                   maindata.at[index, 'longitude'] = df1.Lon.values[0]
            except:
                print ("No data for "+ row['Property Address'])
    print (maindata.head())
    maindata.to_csv('withLatDistrict1.csv')    



def main():
    #filename = './csv/withLat.csv'
    #d = readData(filename)
    #addGeo(d)

    
    filename = './csv/withLatDistrict.csv'
    d = readData(filename)
    # print(d.shape)

    #districts = './csv/NHpolygon.geojson'
    #districts_json = geopandas.read_file(districts)

    #print(districts_json)
    #addDistrict(d, districts_json)
    d['Judgement Total']  = d['Judgement Total'].replace(',','', regex=True)
    d['Judgement Total'] = d['Judgement Total'].astype(float)

    d['Execution Total']  = d['Execution Total'].replace(',','', regex=True)
    d['Execution Total'] = d['Execution Total'].astype(float)
    
    d.to_csv('withLatDistrict.csv')  
    
    #createMapPlot(d,districts_json)

    #setColor(0, 500)
    #chekInsidePolygon()

main()


