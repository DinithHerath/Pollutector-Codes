import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
from pmdarima.arima import auto_arima
# from plotly.plotly import plot_mpl
from statsmodels.tsa.seasonal import seasonal_decompose

data_raw = pd.read_csv('weather_full.csv')
data_raw['Year'] = data_raw['YEAR'].astype(int)
data_raw['Month'] = data_raw['MO'].astype(int)
data_raw['Day'] = data_raw['DY'].astype(int)

index = ['Date', 'Relative Humidity', 'Temp Range', 'EarthSkin Temp', 'Dew Point', 'Wet Bulb Temp', 'Max Temp', 'Min Temp', 'Temp']
temp_date = []
temp_date_format = []
for i in range(len(data_raw['Year'])):
    yr = data_raw['Year'][i]
    mo = data_raw['Month'][i]
    dy = data_raw['Day'][i]
    temp_date.append(datetime.date(yr, mo, dy))
    temp_date_format.append(str(yr) + "-" + str(mo) + "-" + str(dy))
data_raw['Date'] = temp_date
data_raw['date'] = temp_date_format

#Final data for calculation
data = data_raw.loc[:, index]
data.info()
temp = data_raw.loc[:, ['date', 'Temp']]
temp.to_csv('weather_temp.csv', index=False)
data_temp = pd.read_csv('weather_temp.csv' , parse_dates=['date'], index_col='date')
# result = seasonal_decompose(data, model='multiplicative')
# fig = result.plot()
data_temp_predict = pd.read_csv('weather_temp_predict.csv' , parse_dates=['date'], index_col='date')
# ARIMA model

# Seasonal - fit stepwise auto-ARIMA
smodel = auto_arima(data_temp, start_p=1, start_q=1,
                         test='adf',
                         max_p=3, max_q=3, m=12,
                         start_P=0, seasonal=True,
                         d=None, D=1, trace=True,
                         error_action='ignore',  
                         suppress_warnings=True, 
                         stepwise=True)

smodel.summary()

# Forecast
n_periods = 8
fitted, confint = smodel.predict(n_periods=n_periods, return_conf_int=True)
index_of_fc = pd.date_range(data_temp.index[-1], periods = n_periods, freq='D')

# make series for plotting purpose
fitted_series = pd.Series(fitted, index=index_of_fc)
lower_series = pd.Series(confint[:, 0], index=index_of_fc)
upper_series = pd.Series(confint[:, 1], index=index_of_fc)

# Plot
plt.plot(data_temp[7140:])
plt.plot(fitted_series, color='darkgreen')
plt.plot(data_temp_predict, color='red')
plt.fill_between(lower_series.index, 
                 lower_series, 
                 upper_series, 
                 color='k', alpha=.15)

plt.title("SARIMA - Final Forecast of Temperature")
plt.show()