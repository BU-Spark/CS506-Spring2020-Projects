import pandas as pd

# read Land Parcel data (csv) in as a pandas dataframe
land_parcel_df = pd.read_csv(filename)

def filter_poly_typ(filename):
    # filter out data only with poly_typ equal to FEE or TAX
    accepted_codes = ['FEE', 'TAX']
    land_parcel_df = land_parcel_df['poly_typ'].isin(accepted_codes)
    return land_parcel_df
