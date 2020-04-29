import apply_all_filters
import add_long_lat
import add_median_income_by_xy
import pandas as pd
#from findNearByPlaces import *


df = pd.read_csv('../data/usable_std_land_std_agencies.csv')

df = apply_all_filters.apply_all(df)
df = add_long_lat.add_long_lat(df)
df = add_median_income_by_xy.add_census_median_hh_income(df)
#df = findNearByPlaces.getNumTransitStops(df)
