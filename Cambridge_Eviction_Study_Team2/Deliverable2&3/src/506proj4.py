import numpy as np
import csv
import pandas as pd

court = list(csv.reader(open("data_with_median_income_kp1.csv",'r')))

#court = np.array(court)
#print(court)

df = pd.DataFrame(court)
new_header = df.iloc[0]
df = df[1:]
df.columns = new_header
#print(df)

total = np.array(df)


median_income = np.array(df['median_income'])
u_median_income, i_median_income, count_median_income = np.unique(median_income,return_inverse=True,return_counts=True)
#print(np.sort(count_median_income))
district = np.array(df['DISTRICT'])
u_district, i_district, count_district = np.unique(district,return_inverse=True,return_counts=True)
#print(np.sort(count_district))
#print(district)
#print(i_district)
#print(u_district)

import nltk
from nltk.corpus import stopwords
s = set(stopwords.words('english'))


plaintiff = np.array(df['Plaintiff'])
plaintiff_short = []
for i in range(len(plaintiff)):
    filter(lambda w: not w in s,plaintiff[i].split())
    plaintiff_short.append(plaintiff[i].split(' ')[:1])
plaintiff_short = np.array([plaintiff_short])
#plaintiff_short = np.char.lower(plaintiff_short)
u_plaintiff, i_plaintiff, count_plaintiff = np.unique(plaintiff_short,return_inverse=True, return_counts=True)
u_plaintiff = np.array(u_plaintiff)
i_plaintiff = np.array(i_plaintiff)

#print(plaintiff)
#print(i_plaintiff)
#print(u_plaintiff)
#print(len(u_plaintiff))
#print(count_plaintiff)

p_attorney = np.array(df['P-Attorney'])
u_p_attorney, i_p_attorney, count_p_attorney = np.unique(p_attorney,return_inverse=True,return_counts=True)
#print(i_p_attorney)
#print(count_p_attorney)

judgment_type = np.array(df['Judgement Type'])
u_judgment_type, i_judgment_type, count_judgment_type = np.unique(judgment_type, return_inverse=True, return_counts=True)
#print(i_judgment_type)
#print(count_judgment_type)

judgment_method = np.array(df['JudgeMent Method'])
u_judgment_method, i_judgment_method, count_judgment_method = np.unique(judgment_method, return_inverse=True,return_counts = True)
#print(i_judgment_method)
#print(count_judgment_method)

d_attorney = np.array(df['D-Attorney'])
u_d_attorney, i_d_attorney, count_d_attorney = np.unique(d_attorney, return_inverse=True,return_counts=True)
#print(i_d_attorney)
#print(count_d_attorney)

d_a = []
for j in range(len(d_attorney)):
    if d_attorney[j] == '':
        d_a.append(0)
    else:
        d_a.append(1)

u_d_a, i_d_a, count_d_a = np.unique(d_a,return_inverse=True, return_counts = True)
#print(d_a)
#print(i_d_a)
#print(count_d_a)

#********************************************************************************


import math as m

j_total = np.array(df['Judgement Total'])
j_total_hist = []
for k in range(len(j_total)):
    try:
        j_total[k] = float(j_total[k])
        j_total_hist.append(float(j_total[k]))
    except ValueError:
        j_total[k] = 0
#j_total.astype(float)
j_total_hist = np.array(j_total_hist)
#print(j_total)
#print(max(j_total))
#print(min(j_total))
#print(np.mean(j_total))

#j_total_final = np.delete(j_total_hist, j_total_hist.argmin())
j_total_final = np.delete(j_total_hist, j_total_hist.argmax())
#j_total_final = np.delete(j_total_final, j_total_final.argmax())

import matplotlib.pyplot as plt

plt.hist(j_total_final, bins=100)
plt.xlabel('Judgment Total ($)')
plt.ylabel('Number of Cases')
plt.show()

e_total = np.array(df['Execution Total'])
e_total_hist = []
for l in range(len(e_total)):
    try:
        e_total[l] = float(e_total[l])
        e_total_hist.append(float(e_total[l]))
    except ValueError:
        e_total[l] = 0
e_total_hist = np.array(e_total_hist)
#print(e_total)

plt.hist(e_total_hist, bins=100)
plt.xlabel('Execution Total ($)')
plt.ylabel('Number of Cases')
plt.show()

bins = np.array([0, 5000, 10000, 15000, 20000, 25000, 30000, 35000])
e_bins = np.digitize(e_total_hist,bins,right=False)
#print(e_bins)
j_bins = np.digitize(j_total_hist,bins,right=False)
#print(j_bins)




#********************************************************
import matplotlib.pyplot as plt

units = np.array(df['units'])
#print(len(units))
units_hist = []
for m in range(len(units)):
    try: 
        units[m] = float(units[m])
        units_hist.append(units[m])
    except ValueError:
        units[m] = 0
units_hist = np.array(units_hist)
plt.hist(units_hist, bins= 20)
plt.xlabel('Number of Units')
plt.ylabel('Number of Cases')
plt.show()
#print(len(units_hist))
#********************************************************


public_housing = ['Port Landing', 'Harwell', 'Harwell Homes', 'Cambridge Housing Authority',
        'Cambridge Affordable Housing', 'Cambridge Affordable Housing Corporation',
        'Rindge', 'Rindge Apartments', 'Cast II', 'Cast II Apartments', 
        'Fresh Pond Apartments', 'Fresh Pond', 'Magazine House', 'Magazine', 
        'Walden Square', 'Walden Square Apartments', 'Portland Marcella', 
        'Memorial Drive 808', '808 Memorial', 'Inman', 'Inman Square Apartments', 
        'Close Building', 'Close', 'Briston Arms', 'Roosevelt Towers', 
        'Putnam School', 'Franklin St', 'Harvard Place', 'Brookline Pl', '131 Harvard',
        '243 Broadway', 'Cambridge Housing Authority', '241 Garden', '273 Harvard', 
        '49 Columbia', '675 Massachusetts', '411 Franklin', '77 Magazine', 
        '8 Marcella', '21 Walden', '14 Roosevelt', '86 Otis', '402 Rindge', 
        '8 Museum', '1221 Cambridge', '1 Citizen', '364 Rindge']
affordable_housing = ['Port Landing', 'Harwell', 'Harwell Homes', 'Cambridge Housing Authority',
        'Cambridge Affordable Housing', 'Cambridge Affordable Housing Corporation',
        'Rindge', 'Rindge Apartments', 'Cast II', 'Cast II Apartments', 
        'Fresh Pond Apartments', 'Fresh Pond', 'Magazine House', 'Magazine', 
        'Walden Square', 'Walden Square Apartments', 'Portland Marcella', 
        'Memorial Drive 808', '808 Memorial', 'Inman', 'Inman Square Apartments', 
        'Close Building', 'Close', 'Briston Arms', 'Roosevelt Towers', 
        'Putnam School', 'Franklin St', 'Harvard Place', 'Brookline Pl', '131 Harvard',
        '243 Broadway', 'Cambridge Housing Authority', '241 Garden', '273 Harvard', 
        '49 Columbia', '675 Massachusetts', '411 Franklin', '77 Magazine', 
        '8 Marcella', '21 Walden', '14 Roosevelt', '86 Otis', '402 Rindge', 
        '8 Museum', '1221 Cambridge', '1 Citizen', '364 Rindge', 
        '50 Churchill', '150 Erie', 'Auburn Court', '240 Green', '810 Memorial', 
        '265 Harvard', '411 Franklin', '157 6', '402 Rindge', '15 Lambert', '64 Magee', 
        '1 Jackson', '259 Harvard', '129 Franklin', '14 Roosevelt', '11 Corcoran', 
        '131 Washington', '1 Lincoln', '273 Harvard', '4 University', '1066 Cambridge', 
        '625 Putnam', '2505 Massachusetts', '1165 Cambridge', '21 Walden', '140 Franklin',
        '100 Harvard', '650 Concord', '17 Boardman', 'Squirrel', '55 Columbia', 
        '8 Lancaster', '55 Essex', 'Swartz', '2401 Massachusetts', 'Scouting Way', 
        '10 Magazine', '20 Chestnut', '2535 Massachusetts', '9 Woodrow', '26 York', 
        '820 Massachusetts', '210 Otis', '260 Putnam', '19 Market', '80 Auburn', 
        '51 Norfolk']
housing = []
meme = df['Plaintiff'] + ' ' + df['Property Address'] + ' ' + df['Address']
meme = np.array(meme)
for r in range(len(meme)):
    meme[r] = str(np.char.lower(meme[r])) 
#for s in range(len(public_housing)):
#    public_housing[s] = str(np.char.lower(public_housing[s]))
for s in range(len(affordable_housing)):
    affordable_housing[s] = str(np.char.lower(affordable_housing[s]))
######print(meme)
######print(meme.dtype)
#meme = np.char.lower(meme)
#public_housing = np.char.lower(public_housing)
"""
for n in range(len(meme)):
    for q in range(len(public_housing)):
        if public_housing[q] in meme[n]:
            housing.append(public_housing[q])
"""
housing_binary = []
"""
for n in range(len(meme)):
    for q in range(len(affordable_housing)):
        if affordable_housing[q] in meme[n]:
            housing.append(affordable_housing[q])
            housing_binary.append(1)
        else:
            housing_binary.append(0)
"""
h_b = np.zeros((len(meme),len(affordable_housing)))
for n in range(len(meme)):
    for q in range(len(affordable_housing)):
        if affordable_housing[q] in meme[n]:
            h_b[n,q] = 1
        else: 
            h_b[n,q] = 0
h_b_1 = np.nonzero(h_b)
h_b_1_unique = np.unique(h_b_1[0])
#print(h_b_1_unique)
low = np.zeros((1406,1))
for a in h_b_1_unique:
    low[a] = 1
#print(low)
#print(len(low))
#print(h_b_1)
"""
for n in range(len(meme)):
    if affordable_housing in meme[n]:
        housing_binary.append(1)
    else:
        housing_binary.append(0)
"""
#print(housing)
#print(len(housing))
#print(len(meme))
"""
u_housing, i_housing, count_housing = np.unique(housing,return_inverse=True, return_counts=True)
"""

# GENDER ***************************************************************

import gender_guesser.detector as gender

d = gender.Detector(case_sensitive=False)

p = r'\,'
x = df['Deffendant'].str.split(r'[,\s]\s*',expand=True)
#print(x)
x.columns = ['Last','First','nan1','nan2','nan3','nan4','nan5','nan6','nan7','nan8','nan9']
#print(x)
#print(x.iloc[8])
#print(x.iloc[8])
first = np.array(x['First'])
last = np.array(x['Last'])
#print(first)
#print(last)

genders = []
for i in range(len(first)):
    if first[i] is None:
        first[i] = ''
    genders.append(d.get_gender(first[i]))

g_num = []
g_male = []
g_female = []
g_unknown = []
for j in range(len(genders)):
    if genders[j] == 'male' or genders[j] == 'mostly_male':
        g_num.append(1)
        g_male.append(first[j])
    elif genders[j] == 'female' or genders[j] == 'mostly_female':
        g_num.append(0)
        g_female.append(first[j])
    else:
        g_num.append(2)
        g_unknown.append(first[j])

#print(genders)
#print(g_num)
#print(len(g_num))
#print(g_num.count(2)/len(g_num))
#print(g_num.count(0))
#print(g_num.count(1))
#print(g_num.count(0)+g_num.count(1)+g_num.count(2))
#print(g_male)
#print(g_female)
#print(g_unknown)

#print(g_num)

# RACE *****************************************************************
# DO
# **********************************************************************

# get defendants as categorical data

defendant = np.array(df['Deffendant'])
u_defendant, i_defendant, count_defendant = np.unique(defendant, return_inverse=True, return_counts = True)

# GET ALL DATA AS CATEGORICAL DATA**************************************

#print(i_plaintiff) 
#print(i_p_attorney)
#print(d_a)
#print(i_judgment_type)
#print(i_judgment_method)

from sklearn.cluster import KMeans
from kmodes.kmodes import KModes

latitude = np.array(df['latitude']).astype(float)
longitude = np.array(df['longitude']).astype(float)

#print(housing_binary)
#print(len(housing_binary))
#print(u_housing[i_housing])
#print(len(u_housing[i_housing]))


# LIFT

km = KModes(n_clusters = 5)
#kmeans = KMeans(n_clusters = 5)
X = np.vstack((i_plaintiff,i_judgment_type, i_judgment_method,d_a, g_num))
X = np.transpose(X)
X = np.hstack((X,low))
#print(X)
km.fit(X)
y_km = km.predict(X)
#print(X[0,:])
#print(X[1,:])
plt.scatter(latitude, longitude, c = y_km, s = 50, cmap='winter')
plt.xlabel('Latitude')
plt.ylabel('Longitude')
plt.show()

#print(y_km)


units = np.array(df['units'])
number = np.nonzero(df['units'])
number = np.array(number)
units_final = units[number]
units_final = np.transpose(units_final.astype(int))
#print(number)
#print(units_final)

i_plaintiff_num = i_plaintiff[number]
i_judgment_type_num = i_judgment_type[number]
i_judgment_method_num = i_judgment_method[number]
d_a = np.array(d_a)
d_a_num = np.transpose(d_a[number])
g_num = np.array(g_num)
g_num_num = np.transpose(g_num[number])
#print(g_num_num)


"""
print(len(d_a_num))
print(len(g_num_num))
print(len(units_final))
print(len(np.transpose(i_plaintiff[number])))
print(len(i_judgment_type[number]))
print(len(i_judgment_method[number]))
"""

# LIFT

km = KModes(n_clusters = 5)
#kmeans = KMeans(n_clusters = 5)
X = np.hstack((np.transpose(i_plaintiff[number]),np.transpose(i_judgment_type[number]), np.transpose(i_judgment_method[number]),d_a_num, g_num_num))
#X = np.transpose(X)
#print(len(units_final))
#print(len(X))
#print(len(X[0]))
X = np.hstack((X,units_final))
#print(X)
km.fit(X)
y_km = [km.predict(X)]
#print(X[0,:])
#print(X[1,:])
#print(latitude[number])
#print(longitude[number])
#print(y_km)
plt.scatter(latitude[number], longitude[number], c = y_km, s = 50, cmap='winter')
plt.xlabel('Latitude')
plt.ylabel('Longitude')
plt.show()

#print(y_km)



#************************************************************8
# CASES BY GENDER
# bar graph
#print(g_num)

u_g_num, i_g_num, count_g_num = np.unique(g_num,return_inverse=True, return_counts=True)
outcome_gender = np.transpose(np.array((u_judgment_type[i_judgment_type],g_num)))
#print(outcome_gender)
outcome_gender = pd.DataFrame(outcome_gender)
outcome_gender.columns = ('outcome', 'gender')
#print(outcome_gender)
male = outcome_gender.loc[outcome_gender['gender'] == 1]
female = outcome_gender.loc[outcome_gender['gender'] == 0]
male = np.array(male)
female = np.array(female)
#print(male)
#print(female)
#print(len(male))
#print(len(female))

fig, ax = plt.subplots()
o_m = male[:,0]
u_m, count_m = np.unique(male[:,0], return_counts = True)
u_m_len = np.arange(len(u_m))
ax.barh(u_m_len, count_m)
ax.set_yticks(u_m_len)
ax.set_yticklabels(u_m)
ax.invert_yaxis()
ax.set_xlabel('Number of Cases')
ax.set_title('Male Outcomes')
plt.gcf().subplots_adjust(left=0.55)
plt.show()

fig, ax = plt.subplots()
o_f = female[:,0]
u_f, count_f = np.unique(female[:,0], return_counts = True)
u_f_len = np.arange(len(u_f))
ax.barh(u_f_len, count_f)
ax.set_yticks(u_f_len)
ax.set_yticklabels(u_f)
ax.invert_yaxis()
ax.set_xlabel('Number of Cases')
ax.set_title('Female Outcomes')
plt.gcf().subplots_adjust(left=0.55)
plt.show()



# CASES BY AFFORDABLE HOUSING 
# bar graph
#print(np.array(u_judgment_type[i_judgment_type]))
#print(np.transpose(low.flatten()))

outcome_low = np.transpose(np.array((u_judgment_type[i_judgment_type],low.flatten())))
outcome_low = pd.DataFrame(outcome_low)
outcome_low.columns = ('outcome', 'low')
#print(outcome_low)
low = outcome_low.loc[outcome_low['low'] == 1]
not_low = outcome_low.loc[outcome_low['low'] == 0]
low = np.array(low)
not_low = np.array(not_low)

fig, ax = plt.subplots()
o_l = low[:,0]
u_l, count_l = np.unique(low[:,0], return_counts = True)
u_l_len = np.arange(len(u_l))
ax.barh(u_l_len, count_l)
ax.set_yticks(u_l_len)
ax.set_yticklabels(u_l)
ax.invert_yaxis()
ax.set_xlabel('Number of Cases')
ax.set_title('Affordable Housing Outcomes')
plt.gcf().subplots_adjust(left=0.55)
plt.show()

fig, ax = plt.subplots()
o_nl = not_low[:,0]
u_nl, count_nl = np.unique(not_low[:,0], return_counts = True)
u_nl_len = np.arange(len(u_nl))
ax.barh(u_nl_len, count_nl)
ax.set_yticks(u_nl_len)
ax.set_yticklabels(u_nl)
ax.invert_yaxis()
ax.set_xlabel('Number of Cases')
ax.set_title('Non-Affordable Housing Outcomes')
plt.gcf().subplots_adjust(left=0.55)
plt.show()



# CASES BY NUMBER OF UNITS
# bar graph 
#print(len(units_final))
#print(number)
#print(len(np.transpose(number)))
#print(judgment_type)
#print(len(judgment_type[number]))

judge_final = ([judgment_type[iii] for iii in number])
judge_final = np.array(judge_final).flatten()
units_final = units_final.flatten()
#print(judge_final)
#print(units_final)
#print(len(judge_final))
#print(len(units_final))

#print(len(np.transpose(judge_final)))


outcome_units = np.transpose(np.array((judge_final,units_final)))
#print(outcome_units)

outcome_units = pd.DataFrame(outcome_units)
outcome_units.columns = ('outcome','units')

few = outcome_units.loc[outcome_units['units'] < 100]
lots = outcome_units.loc[outcome_units['units'] >= 100]
few = np.array(few)
lots = np.array(lots)
#print(few)
#print(lots)

fig, ax = plt.subplots()
o_few = few[:,0]
u_few, count_few = np.unique(few[:,0], return_counts = True)
u_few_len = np.arange(len(u_few))
ax.barh(u_few_len, count_few)
ax.set_yticks(u_few_len)
ax.set_yticklabels(u_few)
ax.invert_yaxis()
ax.set_xlabel('Number of Cases')
ax.set_title('Few Units Outcomes')
plt.gcf().subplots_adjust(left=0.55)
plt.show()

fig, ax = plt.subplots()
o_lots = lots[:,0]
u_lots, count_lots = np.unique(lots[:,0], return_counts = True)
u_lots_len = np.arange(len(u_lots))
ax.barh(u_lots_len, count_lots)
ax.set_yticks(u_lots_len)
ax.set_yticklabels(u_lots)
ax.invert_yaxis()
ax.set_xlabel('Number of Cases')
ax.set_title('Many Units Outcomes')
plt.gcf().subplots_adjust(left=0.55)
plt.show()
















