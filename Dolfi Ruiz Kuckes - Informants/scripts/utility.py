

import json

print("\nimported utility.py\n")

newest_sjc = "../data/new data w right fields/cases_mass_4_9.json"
newer_sjc = "../data/new data w right fields/cases_mass_new_3_21.json"
new_sjc = "../data/new data/cases_mass_new.json"
old_sjc = "../data/data from 2019 teams/cases.json"

sjc_data_as_file = open(newest_sjc)
sjc = json.load(sjc_data_as_file)
sjc_old = json.load(open(old_sjc))

newest_appeals_court =  "../data/new data w right fields/appeal_mass_4_9.json"
newer_appeals_court = "../data/new data w right fields/appeal_mass_new_3_21.json"
old_appeals_court = "../data/data from 2019 teams/cases_appeals.json"

appeals_court_data_as_file = open(newest_appeals_court)
appeals_court = json.load(appeals_court_data_as_file)
appeals_old = json.load(open(old_appeals_court))


#returns all cases, cleaned and grouped into two categories
#Daniel's code
#return all_sjc, all_state_appeals
def combine_cases():
    import pandas as pd

    cases = sjc_old #json.load(j)
    for case in range(len(cases)):
        # Need cases, headnotes, and text as strings not lists
        cases[case]["case"] = " ".join(cases[case]["case"])
        cases[case]["headnote"] = "\n".join(cases[case]["headnote"])
        cases[case]["text"] = "\n".join(cases[case]["text"])
    cases = pd.DataFrame(cases)


    appeals = appeals_old
    for case in range(len(appeals)):
        # Need cases, headnotes, and text as strings not lists
        appeals[case]["case"] = " ".join(appeals[case]["case"])
        appeals[case]["headnote"] = "\n".join(appeals[case]["headnote"])
        appeals[case]["text"] = "\n".join(appeals[case]["text"])
    appeals = pd.DataFrame(appeals)

    new_cases = sjc
    new_cases = pd.DataFrame(new_cases)

    new_appeals = appeals_court
    new_appeals = pd.DataFrame(new_appeals)
    
    # Making two pandas dataframes with all the data, one for sjc cases, one for appeals courts. 
    all_cases = cases.append(new_cases, ignore_index=True)
    all_appeals = appeals.append(new_appeals, ignore_index=True)
    return all_cases, all_appeals

