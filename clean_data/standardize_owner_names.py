import pandas as pd


# pre-clean the user names in the raw data
def pre_clean(raw_data):
    raw_df = pd.DataFrame(raw_data)

    # make all user names uppercase
    raw_df['user_name']

    # remove punctuation
    #