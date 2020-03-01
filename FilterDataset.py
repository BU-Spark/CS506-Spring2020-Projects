import pandas as pd

data_dir = "./data/"

def get_filepath(filename):
    return data_dir + filename

"""
Return only land parcels with the land adjusted codes of 909 and greater
"""
def filterByLucGreaterThan909():
    df = pd.read_csv(get_filepath("original.csv"))
    print("Dataset read complete")
    df = df[df["luc_adj_1"]>909]
    print("Dataset filtered by land use code > 909")
    df.to_csv(get_filepath("original_luc_gt_909.csv"))

filterByLucGreaterThan909()