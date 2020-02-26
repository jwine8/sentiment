# Importing libraries
import numpy as np
import pandas as pd
from pandas.plotting import lag_plot
from pandas import datetime
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
import pickle

# Loading Data
data = pd.read_csv('google-2015-2019.csv', parse_dates=['Date'])
data.set_index('Date', inplace=True)

# Exploring the data
cols = ['High', 'Low', 'Close', 'Adj Close', 'Volume']
data.drop(cols, axis=1, inplace=True)

# Data preproccessing
idx = pd.date_range(data.index.min(), data.index.max())
df_pre = pd.DataFrame(data['Open'].reindex(idx, fill_value=None))
df = df_pre.interpolate(method='linear')
df_new_rows = df[df_pre['Open'].isnull()]

# Splitting dataset (80:20)
ntrain_data, ntest_data = df[0:int(len(df)*0.8)], df[int(len(df)*0.8):]


# Modeling

## Find the Symmetric Mean Absolute Percentage Error
def smape_kun(y_true, y_pred):
    return np.mean((np.abs(y_pred - y_true) * 200 / (np.abs(y_pred) + np.abs(y_true))))


## Build the ARIMA Model
train_ar = ntrain_data.values
test_ar = ntest_data.values
history = [x for x in train_ar]
print(type(history))
predictions = list()
for t in range(len(test_ar)):
    model = ARIMA(history, order=(0, 1, 0))
    model_fit = model.fit(disp=0)
    output = model_fit.forecast()
    yhat = output[0]
    predictions.append(yhat)
    obs = test_ar[t]
    history.append(obs)
error = mean_squared_error(test_ar, predictions)
print('Testing Mean Squared Error: %.3f' % error)
error2 = smape_kun(test_ar, predictions)
print('Symmetric mean absolute percentage error: %.3f' % error2)

## Save the Model
pickle.dump(model_fit, open('ARIMA_Model.plk', 'wb'))

