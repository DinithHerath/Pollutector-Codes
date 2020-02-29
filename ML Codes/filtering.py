import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def filterset(dataset, outlier_idx, rolling_ds):
    filteredset = [0 for i in range(0,130)]
    for i in range(0,130):
        if outlier_idx[i]==True:
            filteredset[i] = rolling_ds[i]
        else:
            filteredset[i] = dataset[i]
    return filteredset

# Importing the dataset
dataset = pd.read_csv('heartrate.csv')
X = dataset['Obs']#make sure X is a matrix
y = dataset['HeartRate']

#plt.scatter(X, y, color='red')
#plt.plot(X, y, color='blue')
kw = dict(marker='o', linestyle='none', color='g', alpha=0.3)
figsize = (7, 2.75)

threshold = 2
P = y.rolling(window=10).median().fillna(method='bfill').fillna(method='ffill')
difference = np.abs(y - P)
outlier_idx = difference > threshold
filteredset = filterset(y, outlier_idx, P)
out = pd.Series(filteredset)
# Calculate the simple average of the data
y_mean = [np.mean(filteredset)]*len(X)
fig, ax = plt.subplots(figsize=figsize)
y.plot(color='blue')
y[outlier_idx].plot(**kw)
out.plot(color='red')
mean_line = ax.plot(X,y_mean, label='Mean', linestyle='--')
_ = ax.set_ylim(45, 95)


