import pandas as pd

data = pd.read_csv('./csv/cleanData.csv')

income = pd.read_csv('.csv/American_Community_Survey_2013_-_17_Estimates_by_Neighborhood__Median_Income.csv')

def getIncome(Nhood):
    if Nhood == '0':
        return
    if Nhood == 'Area 2/MIT':
        Nhood = 'MIT'
    household = income[income['Neighborhood '] == Nhood]['Median Household Income']
    return household.iloc[0]

data = data.assign(median_income=lambda df: df.DISTRICT.apply(getIncome))

data.to_csv('data_with_median_income.csv')