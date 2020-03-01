import pandas as pd
import requests

def getAddress(agency):
    params = {
        'input': agency,
        'inputtype': 'textquery',
        'fields': 'formatted_address',
        'key': ''
    }
    ret = requests.get('https://maps.googleapis.com/maps/api/place/findplacefromtext/json', params=params).json()
    if len(ret["candidates"]) > 0:
        if "formatted_address" in ret["candidates"][0]:
            return ret["candidates"][0]["formatted_address"]
    else:
        return "Address not found"

def main():
    df = pd.read_csv("./data/massgov.csv")
    df = df.dropna(how='all', axis=1)
    #null_addresses = df[df["Address"].isnull()]
    for i in range(len(df)):
        currentAddress = df.loc[i]["Address"]
        if not isinstance(currentAddress, str):
            agency = df.loc[i]["Agency"]
            agencyAddress = getAddress(agency)
            print(agencyAddress)
            df.at[i, "Address"] = agencyAddress
    
    print("Address lookup for null addresses complete.")
    df.to_csv("./data/massgov_nonnull.csv")
    print("Write complete")

main()

