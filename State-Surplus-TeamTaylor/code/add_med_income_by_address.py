import pandas as pd
import numpy as np
import requests
from pprint import pprint
from datetime import datetime
from statistics import mean

def add_census_median_hh_income(dataframe):
    '''
        Adds a column containing Census 2010 Median HH Income data for each land parcel to the dataframe.
        Process:
            - Utilizes address fields (addr_num, addr_str, addr_zip) to obtain census tract number.
            - Downloads median household income for all tracts in MA.
            - Matches tract numbers in both tables to combine median income data into the input dataframe.
    '''
    def add_tract_numbers(dataframe):
        '''
            Adds a 'census_tract' column to the input dataframe. 
            Uses helper method get_tract_number to populate the column with data. 
        '''

        def get_tract_number(addr_num, addr_str, addr_zip=None):
            '''
                Makes a request to Census Geocoder API and returns a tract number for a given address.
                Inputs:
                    - addr_num = street number, can be a range of street numbers, e.g. 200-400
                    - addr_str = street name
                    - addr_zip = zip code
                Note: addr_num, addr_str, and addr_zip are all required fields! If any are unavailable, then the request fails.
                    This is despite the API documentation stating that zip code is an optional field.
            '''
            # remove any extra white space in the addr_num field
            addr_num = str(addr_num).replace(" ", "")
            addr_str = addr_str.replace('#', "")
            
            # join separate words in street name with '+'
            street_split = addr_str.split()
            addr_str_formatted = ''
            # remove extra white spaces
            for i in range(len(street_split)):
                if (not street_split[i].isspace()):
                    addr_str_formatted = addr_str_formatted + street_split[i]

                    if (i != len(street_split)-1):
                        addr_str_formatted = addr_str_formatted + '+'
            
            URL = "https://geocoding.geo.census.gov/geocoder/geographies/address?street=" + addr_num + "+" \
                + addr_str_formatted
            
            if (addr_zip is not None and addr_zip):
                URL = URL + "&zip=" + str(addr_zip).replace(" ", "")
            
            URL = URL + "&benchmark=Public_AR_Census2010&vintage=Census2010_Census2010" + \
                "&layers=14&format=json"

            response = requests.get(url = URL)
            tract = np.nan
            
            if (response.status_code == 200):
                data = response.json()
                # pprint(data)
                if (len(data['result']['addressMatches']) > 0):
                    # if data['result']['addressMatches'][0]['geographies']['Census Blocks'][0]['TRACT']:
                    tract = data['result']['addressMatches'][0]['geographies']['Census Blocks'][0]['TRACT']
            
            return tract

        dataframe['census_tract'] = np.nan

        for i in range(len(dataframe)):
            # in order to make request, need street address (number & street name), AND zip code
            addr_num = str(dataframe.iloc[i]['addr_num']).replace(" ", "")
            addr_str = dataframe.iloc[i]['addr_str']
            addr_zip = str(dataframe.iloc[i]['addr_zip']).replace(" ", "")
            
            #print(i, addr_num, addr_str, addr_zip)
            if (i % 100 == 0):
                print('Step: ', i)
                print("Current Time =", datetime.now().strftime("%H:%M:%S"))
            
            # check for any blanks or nan values
            if not ((not addr_num or addr_num == 'nan') \
                or (not addr_str or addr_str == 'nan') \
                or (not addr_zip or addr_zip == 'nan')):
                try:
                    tract = get_tract_number(addr_num, addr_str, addr_zip)
                    dataframe.at[i, 'census_tract'] = tract
                except:
                    print('Error at step: ', i)
        
        return dataframe

    def get_median_hh_income():
        '''
            Returns Pandas DataFrame representation Median Household Income Estimate by Census Tract for MA.
            American Community Survey (ACS) 2018 Census data used.
            Specific table: ACS 2018 5-year detailed table "B19013_001E"
        '''
        URL = "https://api.census.gov/data/2018/acs/acs5?get=B19013_001E&for=tract:*&in=state:25"
    
        response = requests.get(url = URL)
        data = response.json()

        # pprint(data)
        
        median_income_df = pd.DataFrame(data[1:len(data)-1], columns = data[0])
        # outputs median income data to .csv file in current directory 
        median_income_df.to_csv('ma_med_income_tract.csv',index=False)
        
        return median_income_df

    dataframe = add_tract_numbers(dataframe)
    median_income_df = get_median_hh_income()
    
    # only check for land parcels that we were able to obtain tract numbers for
    for i in dataframe[dataframe['census_tract'].notna()].index:
        tract = str(dataframe.loc[i]['census_tract'])
        median_hh_income = median_income_df[median_income_df['tract'] == tract]['B19013_001E']
        
        # ACS data is broken down by state > county > tract
        # sometimes tract covered more than 1 county
        # averaged the median incomes
        if (len(median_hh_income) > 1):
            median_hh_income = mean([int(m) for m in median_income_df[median_income_df['tract'] == tract]['B19013_001E'].values])
        
        try:
            dataframe.at[i, 'median_hh_income'] = median_hh_income
        except:
            print('Error at index: ', i)
