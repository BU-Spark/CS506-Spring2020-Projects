import pandas as pd



#filters mapc dataset by land use code, poly-type, and lots with buildings

df = pd.read_csv('./result/MatchWithAgencyNames.csv')


def filter_luc(df):
  """filters by land use codes affiliated with MA state agencies
  """
  accepted_codes = ['910','911','912','913','914','915','916','917','918','919','920','921','922',
         '923','924','925','926','927','928','929','970','971','972','973','974','975']
  
  return df[df['luc_1'].isin(accepted_codes) | df['luc_2'].isin(accepted_codes) | \
          df['luc_adj_1'].isin(accepted_codes)| \
          df['luc_adj_2'].isin(accepted_codes)]


def filter_poly_typ(dataframe):
  # filter out data only with poly_typ equal to FEE or TAX
  accepted_codes = ['FEE', 'TAX']
  #dataframe = dataframe[dataframe['poly_typ']].isin(accepted_codes)
  return dataframe[dataframe['poly_typ'].isin(accepted_codes)]


def filter_bldg(dataframe):
  '''
  Filter on related columns that indicate whether building(s) are present on the land parcel.
  Removes rows that correspond to land parcels that do not contain buildings.
  Ziba specified:
      bldg_value - for condos, generally includes land value
      bldg_area - may include garages, stairwells, basements, and other uninhabitable areas.
      bldgv_psf - building value $ per sq foot
  Additional:
      sqm_bldg - parcel area estimated to be covered by a building (sq meters)
      pct_bldg - % parcel area estimated to be covered by a building
  '''
  return dataframe[dataframe['bldg_value']>0 | \
                   dataframe['bldg_area']> 0 | \
                   dataframe['bldgv_psf']> 0 | \
                   dataframe['sqm_bldg'] > 0 | \
                   dataframe['pct_bldg'] > 0 & \
                   dataframe['luc_1'] & \
                   dataframe['luc_2'] & \
                   dataframe['luc_adj_1']&\
                   dataframe['luc_adj_2']&\
                   dataframe['poly_typ']]
                   

df= filter_luc(df)
df = filter_poly_typ(df)
#df = filter_bldg(df)
print(df.head(15))

df.to_csv('./data/usable_state_land.csv')
print(df.shape)
