from fuzzywuzzy import fuzz
import pandas as pd 

data_dir = "./data/"

agency_names = pd.read_csv(data_dir + "agency_names.csv", header=None)
dataset = pd.read_csv(data_dir + "sample.csv")
dataset.dropna() #Bug: NA values are not being dropped

standardized_agency_names = agency_names[0].tolist()

owners = dataset["owner_name"].dropna().tolist() #DROPPING NA VALS ON SERIES ONLY

for i in range(len(standardized_agency_names)):
    current_agency_standardized_name = standardized_agency_names[i]
    print(current_agency_standardized_name)
    for j in range(len(owners)):
            diff = fuzz.partial_ratio(current_agency_standardized_name.lower(), owners[j].lower())
            print("Comparing " + current_agency_standardized_name.lower() + " to " + owners[j].lower() + " - score: "  + str(diff))
            if(diff > 60):
                print(owners[j] + " transforming to " + current_agency_standardized_name + " - score: " + str(diff))
            
        