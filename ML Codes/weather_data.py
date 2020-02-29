import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import calmap

data_raw = pd.read_csv('weather_full.csv')
data_raw['Year'] = data_raw['YEAR'].astype(int)
data_raw['Month'] = data_raw['MO'].astype(int)
data_raw['Day'] = data_raw['DY'].astype(int)

index = ['Date', 'Relative Humidity', 'Temp Range', 'EarthSkin Temp', 'Dew Point', 'Wet Bulb Temp', 'Max Temp', 'Min Temp', 'Temp']
temp_date = []
for i in range(len(data_raw['Year'])):
    yr = data_raw['Year'][i]
    mo = data_raw['Month'][i]
    dy = data_raw['Day'][i]
    temp_date.append(datetime.date(yr, mo, dy))
data_raw['Date'] = temp_date

#Final data for calculation
data = data_raw.loc[:, index]
data.info()
#data_temp = data.loc[:, ['Temperature', 'Date']]
#data_temp.index = pd.DateTimeIndex(data_temp.index)

#Plotting Histograms to detect outliers
#matplotlib inline
plt.figure()
i = 8
plt.rcParams['figure.figsize'] = [14, 8]
data[index[i]].hist()
plt.title('Distribution of ' + str(index[i]))
plt.xlabel(str(index[i]))
plt.show()

data.corr()[['Temp']].sort_values('Temp')
    
plt.figure(0)
figsize = (7, 2.75)
plt.plot(data_final['Date'], data_final['Humidity'], color='blue')
plt.figure(1)
figsize = (7, 2.75)
plt.plot(data_final['Date'], data_final['Temperature'], color='red')
fig, ax = calmap.calendarplot(data_final['Temperature'], fig_kws={"figsize":(15,4)})
plt.title("Temperature Daily")