import pandas as pd

def isTransportation(name):
    return any( (x in name.lower()) for x in ['trans','transit','transportation'])

def isHousing(name):
    return any((x in name.lower()) for x in ['house', 'housing'])

dataset = pd.read_csv("./result/usable_state_land.csv")

# 1 for transportation, 0 for housing, and -1 for none
new_column = []
for i in range(len(dataset['std_name'])):
    if isTransportation(dataset['std_name'][i]):
        new_column.append(1)
    elif isHousing(dataset['std_name'][i]):
        new_column.append(0)
    else:
        new_column.append(-1)


dataset['TransportationOrHousing'] = new_column
dataset.to_csv("./result/usable_state_land.csv", index=False)


