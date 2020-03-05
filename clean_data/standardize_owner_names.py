import pandas as pd
import string
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


# pre-clean the owner names in the raw data:
# change user_name to uppercase, remove punctuation, sort in alphabet order
def pre_clean_user_name(raw_data):
    raw_df = pd.DataFrame(raw_data)

    # make all owner names uppercase
    raw_df['owner_name'] = raw_df['owner_name'].str.upper()

    # remove punctuations
    punct = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{}~'  # `|` is not present here
    transtab = str.maketrans(dict.fromkeys(punct, ''))
    raw_df['owner_name'] = '|'.join(raw_df['owner_name'].tolist()).translate(transtab).split('|')

    # sort in alphabet order
    pre_cleaned_df = raw_df.sort_values(by = ['owner_name'])

    return pre_cleaned_df


# receive the pre-cleaned data table and the accurate owner name list
def compare_owner_names(pre_cleaned_df, std_name_list):
    # get a list of user names from the data table and remove duplicates
    raw_name_list = pre_cleaned_df['owner_name']
    uni_raw_name_ist = list(set(raw_name_list))

    ratio_list = []
    cmp_dic = {}
    # calculate the similarity ratio between each unique raw owner name and the standard owner name
    for name in uni_raw_name_ist:
        for std_name in std_name_list:
            ratio_list.append(fuzz.token_sort_ratio(name, std_name))
        cmp_dic[name] = ratio_list

    similar_ratio_matrix = pd.DataFrame(cmp_dic)

    print(similar_ratio_matrix.head())
    return similar_ratio_matrix


# find the most similar owner names to the raw name data
def find_std_names(similar_ratio_matrix, std_name_list):
    name_dic = {}
    # Get the index of the largest ratio in the matrix
    # The name associated with such index in the std_name_list is the most likely one
    for index in similar_ratio_matrix.iteritems():
        print(index)
        index = similar_ratio_matrix[index].idxmax()
        name_dic[index] = std_name_list[index]
    return name_dic


# replace the owner name list in the raw data table with std names
def std_owner_name(raw_df, name_dic):
    std_owner_df = pd.DataFrame(raw_df)
    # add a new column for all the std names to the original table
    std_owner_df['std_owner_name'] = None

    # for each name in the original table, go through the std name list searching for the name
    # then add the corresponding std name in the std name list to the newly added column
    index = 0
    for name in std_owner_df['owner_name']:
        for key in name_dic:
            if name == key:
                std_owner_df['new_name', index] = name_dic[key]
                index += 1
                break

    return std_owner_df




