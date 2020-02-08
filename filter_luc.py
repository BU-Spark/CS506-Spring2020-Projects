import pandas as pd 

accepted_codes = ['910','911','912','913','914','915','916','917','918','919','920','921','922',
				 '923','924','925','926','927','928','929','970','971','972','973','974','975']

#df = pd.read_pickle('mapc.pkl'), pickle used on pc
df = pd.read_csv('mapc.ma_parcels_metrofuture.csv',dtype=object)

def filter_luc(dataframe):
  """filters by land use codes affiliated with MA state agencies
  """
	return df[df['luc_1'].isin(accepted_codes) | df['luc_2'].isin(accepted_codes) | 
		      df['luc_adj_1'].isin(accepted_codes)|
		      df['luc_adj_2'].isin(accepted_codes)]
