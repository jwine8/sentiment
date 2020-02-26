import numpy as np 
import pandas as pd 
import pmdarima as pm
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.statespace.sarimax import SARIMAX
import pickle

# Import Data
data = pd.read_csv('google-2015-2019.csv',parse_dates=['Date'])
data.set_index('Date', inplace=True)

data=pd.DataFrame(data['Adj Close'])
date_orig = data.index

# Get the index and fill in missing values
idx = pd.date_range(data.index.min(), data.index.max())
df_pre= pd.DataFrame(data['Adj Close'].reindex(idx, fill_value=None))
df = df_pre.interpolate(method='linear')
df_new_rows = df[df_pre['Adj Close'].isnull()]

y = df['Adj Close']

# fitting a stepwise model:
stepwise_fit = pm.auto_arima(df, start_p=1, start_q=1, max_p=3, max_q=3, m=12,
                            start_P=0, seasonal=True, d=1, D=1, trace=True,
                             error_action='ignore', suppress_warnings=True, stepwise=True)

#stepwise_fit.summary()

# Building the SARIMAX Model
model = SARIMAX(df, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
results =model.fit()

# Save the model
pickle.dump(results, open('SARIMA_Model.plk', 'wb'), protocol=2)