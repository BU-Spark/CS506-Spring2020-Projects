import pandas as pd
import numpy as np
from pyproj import CRS, Transformer

def add_long_lat(dataframe):
    '''
    Uses parloc_id column in land parcel database (i.e. X, Y coordinates in NAD83 spatial reference)
    and transforms them into longitude, latitude coordinates (in ESPG:4326 = WGS84). Saves corresponding longitude, latitude
    coordinate information for each record in new columns appended to original dataframe.
    Note: parloc_id may start with 'F_' or 'M_' (designating feet or meters).
        For feet, initial spatial reference NAD83 is equivalent to ESPG:3586.
        For meters, initial spatial reference NAD83 is equivalent to ESPG:26986.
    '''
    # need to reset indices to account for removal of rows from filtering
    dataframe = dataframe.reset_index()

    # add columns to store longitude and latitude coordinates
    dataframe['longitude'] = np.nan
    dataframe['latitude'] = np.nan

    # convert parloc_id column to longitude, latitude coordinates
    crs_4326 = CRS.from_epsg(4326) # target spatial reference to transform to
    crs_26986 = CRS.from_epsg(26986) # for coordinates in meters
    crs_3586 = CRS.from_epsg(3586) # for coordinates in feet

    transformer_meters = Transformer.from_crs(crs_26986, crs_4326, always_xy=True)
    transformer_feet = Transformer.from_crs(crs_3586, crs_4326, always_xy=True)

    for i in range(len(dataframe)):
        # make sure there are no whitespaces
        parloc_id = str(dataframe.at[i, 'parloc_id']).replace(" ", "")
        dataframe.at[i, 'parloc_id'] = parloc_id
        
        if (parloc_id.startswith('F')):
            end_x_idx = parloc_id.find('_', 2)
            x = parloc_id[2:end_x_idx]
            y = parloc_id[end_x_idx+1:]
            longitude, latitude = transformer_feet.transform(x, y)
            dataframe.at[i, 'longitude'] = longitude
            dataframe.at[i, 'latitude'] = latitude
        elif (parloc_id.startswith('M')):
            end_x_idx = parloc_id.find('_', 2)
            x = parloc_id[2:end_x_idx]
            y = parloc_id[end_x_idx+1:]
            longitude, latitude = transformer_meters.transform(x, y)
            dataframe.at[i, 'longitude'] = longitude
            dataframe.at[i, 'latitude'] = latitude
        else:
            print('At index ', i, ' parloc_id does not start with M_ or F_')

    dataframe.to_csv('./State-Surplus-TeamTaylor/data/state_land_plus_long_lat.csv',index=False)