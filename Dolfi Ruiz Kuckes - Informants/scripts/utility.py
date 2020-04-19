

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

