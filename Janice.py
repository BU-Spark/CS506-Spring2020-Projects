import time
import operator from itemgetter

start_time = time.time()

# Imports data, filters it to just return columns: owner_name and owner_address (concatenated with city and state)
# Output looks like: [['HATCH ROBERT LLC', 'ABINGTON LLC'], ['76 WILBURT ST ABTON MA', '245 CENTRAL ST ABINGTON MA']]
def import_data(filename):
    """ import_data parses data, and replaces ? values with NaN """
    name = []
    address = []
    with open(filename, 'r') as data:
        for line in data:
            line = line.split(',')
            name.append(line[30])
            address.append((line[31] + ' ' + line[32] + ' ' + line[33]).strip())
        name = name[1:] # remove the top header
        address = address[1:] # remove the top header
        return name, address

owner_table = import_data("data/segmentaa.csv")

# Zips the two lists
def pairwise(table):
    return(zip(table[0], table[1]) )

pairwise = pairwise(owner_table)

def sort_by_address(table):
    return(sorted(table, key=lambda x: x[1]) )

sortedlist = sort_by_address(pairwise)

def majority_rule(table): # (name, address)
    temp_dic = {} # key-value => different owner_names per address: count
    offical_dic = {} # key-value => address: majority owner_name
    seen_address_flag = False
    for i in range(len(table)):
        if i > 0 and table[i][1] == table[i-1][1]:
            seen_address_flag = True# check that we are working with owner_names of same address
            if table[i][0] not in temp_dic: # first time seeing owner_name
                temp_dic[table[i][0]] = 1 # count begins at 1 for specific owner_name
            else: # not in official_dic, but address already exists in temp_dic
                temp_dic[table[i][1]] += 1
        else:
            seen_address_flag = False
            official_dic[table[i][1]] = sorted(temp_dic,itemgetter(1))[-1][0] # set official owner-name to the address
            temp_dic = {}



majority_rule(sortedlist)


print("My program took", time.time() - start_time, "seconds to run")
