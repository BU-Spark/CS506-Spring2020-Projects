import math as m
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import pearsonr
from sklearn import metrics 
from sklearn.preprocessing import normalize
import sklearn as sk
from sklearn.cluster import KMeans


data = pd.read_csv('courtdata.csv', sep=',', encoding='latin-1')

#print(data)

data_val = data.values

plaintiff = data_val[:,3]
attorney = data_val[:,6]
judgment = data_val[:,10]
appear = data_val[:,11]
money = data_val[:,12]

#print(attorney)
#print(judgment)

nan = np.nan

total_cases = len(attorney)

plaintiff_data = np.zeros((total_cases,1))
attorney_data = np.zeros((total_cases,1))
judgment_data = np.zeros((total_cases,1))
appear_data = np.zeros((total_cases,1))
money_data = np.zeros((total_cases,1))

for i in range(total_cases):
    if isinstance(attorney[i], str):
        attorney_data[i] = 0 # with representation
    else:
        attorney_data[i] = 1 # no representation
    if judgment[i] == 'Judgment for Plaintiff for Possession and Rent':
        judgment_data[i] = 1 # conviction 
    else:
        judgment_data[i] = 0 # no conviction
    if appear[i] == 'after defendant(s) failed to appear':
        appear_data[i] = 0 # no show
    else: 
        appear_data[i] = 1 # showed up
    if isinstance(money[i], str):
        money[i] = money[i].replace(',','')
    if isinstance(money[i], float):
        money_data[i] = 0 # no money due
    else:
        money_data[i] = float(money[i]) # money due
    if plaintiff[i] == 'Cambridge Housing Authority':
        plaintiff_data[i] = 1 # cambridge housing authority 
    else:
        plaintiff_data[i] = 0 # other
        
data_total = np.hstack((plaintiff_data,attorney_data,judgment_data,appear_data,money_data))
#print(data_total) 
  
total = data_total/data_total.max(axis=0)
#print(total) 

# USE THIS FOR DELIVERABLE 1
total_pd = pd.DataFrame(total)
total_corr = total_pd.corr()
print(total_corr)

total_13 = np.transpose(np.vstack((total[:,1], total[:,3])))
#print(total_13)

total_0134 = np.transpose(np.vstack((total[:,0],total[:,1],total[:,3],total[:,4])))

kmeans = KMeans(n_clusters = 3)
kmeans.fit(total_13)
y_kmeans = kmeans.predict(total_13)

kmeans_all = KMeans(n_clusters = 3)
kmeans_all.fit(total_0134)
y_kmeans_all = kmeans_all.predict(total_0134)

"""
plt.scatter(total_23[:,0], total_23[:,1], c = y_kmeans, s=50, cmap='viridis')
centers = kmeans.cluster_centers_
plt.scatter(centers[:,0],centers[:,1], c='black', alpha=0.5)
plt.show()
"""

print((y_kmeans))
print(y_kmeans_all)

count_13 = np.count_nonzero(y_kmeans)
count_0134 = np.count_nonzero(y_kmeans_all)

print(count_13)
print(count_0134)
print(len(y_kmeans))

# test if matching 
error13 = np.mean(y_kmeans != judgment_data)
error0134 = np.mean(y_kmeans_all != judgment_data)

print(error13)
print(error0134)

judg1 = np.count_nonzero(judgment_data)
judg_len = len(judgment_data)
percent_judg = judg1/judg_len
print(percent_judg)


gmm13 = sk.mixture.GaussianMixture(n_components=3).fit(total_13)
labels13 = gmm13.predict(total_13)
print(labels13)

gmm0134 = sk.mixture.GaussianMixture(n_components=3).fit(total_0134)
labels0134 = gmm0134.predict(total_0134)
print(labels0134)

error13_gmm = np.mean(labels13 != judgment_data)
error0134_gmm = np.mean(labels0134 != judgment_data)

print(error13_gmm)
print(error0134_gmm)
        
#print(attorney_data)
#print(judgment_data)

#print(type(attorney[0]))

corr, _ = pearsonr(attorney_data,judgment_data)
#print(corr)

num_attorney_neg = np.count_nonzero(attorney_data) # count no representation
num_attorney_pos = (len(attorney_data) - num_attorney_neg) # count lawyer

num_judgment_neg = np.count_nonzero(judgment_data) # count conviction
num_judgment_pos = (len(judgment_data) - num_judgment_neg) # count no conviction

"""
# test - PASS
print(num_attorney_neg)
print(num_attorney_pos)
print(len(attorney_data))

# test - PASS
print(num_judgment_neg)
print(num_judgment_pos)
print(len(judgment_data))
"""

percent_attorney_pos = (num_attorney_pos)/(len(attorney_data))
percent_attorney_neg = 1 - percent_attorney_pos

percent_judgment_neg = (num_judgment_neg)/(len(judgment_data))
percent_judgment_pos = 1 - percent_judgment_neg

"""
# test - PASS 
print(percent_attorney_pos)
print(percent_attorney_neg)

# test - PASS
print(percent_judgment_neg)
print(percent_judgment_pos)
"""

both = np.hstack((attorney_data,judgment_data))
#print(both)
both_sorted = both[both[:,1].argsort()]
#print(both_sorted)

range_judgment_neg = range((num_judgment_pos+1),(num_judgment_neg))
range_judgment_pos = range(1,num_judgment_pos)

"""
# test - PASS
print(range_judgment_neg)
print(range_judgment_pos)
"""

both1 = both_sorted[range_judgment_neg,:]
both2 = both_sorted[range_judgment_pos,:]

both1_sorted = both1[both1[:,0].argsort()]
both2_sorted = both2[both2[:,0].argsort()]

both_final = np.vstack((both1_sorted,both2_sorted)) 

#print(both1_sorted)
#print(both2_sorted)
#print(both_final)


"""
both_sorted2 = both_sorted[both_sorted[range_judgment_pos,0].argsort()]
both_sorted3 = both_sorted[both_sorted[range_judgment_neg,0].argsort()]

print(both_sorted2)
print(both_sorted3)
"""

#fpr, tpr, thresholds = metrics.roc_curve(both_final[:,0], both_final[:,1], pos_label=2)
#metrics.auc(fpr,tpr)
