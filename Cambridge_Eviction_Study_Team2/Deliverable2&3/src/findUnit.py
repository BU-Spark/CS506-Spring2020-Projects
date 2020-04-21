import numpy as np
import pandas as pd
import string


data = pd.read_csv('./csv/withLatDistrictNoDup.csv', sep=',', encoding='latin-1')
number = pd.read_csv("./csv/housingstat.csv")

data = data[data['Property Address'].notnull()]
number = number[number['Geocode Address'].notnull()]


print(data['Property Address'][:2])
print(number['Geocode Address'][:2])


def findUsage(address):

    rec = number.loc[number['Geocode Address'] == address]
    return rec
    #print(rec)
    #print(address)
    #print(number['Geocode Address'])
    #if(address in number['Geocode Address']):
    #  print(address)

def addressParser(address):
    address = address.translate(table) 
    address = address.replace('Street', 'St')
    address = address.replace('Towers', 'St')
    address = address.replace('Ave', 'St')
    address = address.replace('Avenue', 'St')
    address = address.replace('Ave', 'St')
    address = address.replace('Way', 'St')
    address = address.replace('Drive', 'St')
    address = address.replace('Court', 'St')
    address = address.replace('Lane', 'St')
    address = address.replace('Parks', 'St')
    address = address.replace('Garden', 'St')
    address = address.replace('Park', 'St')
    address = address.replace('Stnue', 'St')
    address = address.replace('Place', 'St')
    address = address.replace('Sts', 'St')
    address = address.replace('Dr', 'St')
    address = address.replace('One', '1')
    return address


table = str.maketrans(dict.fromkeys(string.punctuation))  # OR {key: None for key in string.punctuation}

addresses = []
for x in data['Property Address']:

  splitted = x.split()
  if(len(splitted) >= 3):
    address = splitted[0] + ' ' + splitted[1] + ' ' + splitted[2]
    address = address.translate(table)
    address = addressParser(address)
  addresses.append(address)
  

data['Address'] = addresses


GeoAddresses = []

for x in number['Geocode Address']:
  splitted = x.split()
  
  if(len(splitted) >= 3):
    address = splitted[0] + ' ' + splitted[1] + ' ' + splitted[2]
    address = address.translate(table) 
    address = addressParser(address)
  GeoAddresses.append(address)
number['Geocode Address'] = GeoAddresses

if 'units'  not in data.columns:
        data['units'] = ''

for i in range(data.shape[0]):
  address = val = data['Address'].values[i]
  res = findUsage(address)
  print(res)
  if (res.empty == False) :
    data.at[i, 'units'] = res['Housing Starts'].values[0]

print(data)

data.to_csv('withLatDistrictUnit.csv') 
