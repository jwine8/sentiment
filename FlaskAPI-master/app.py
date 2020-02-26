from flask import Flask, render_template, request, jsonify, url_for
import pickle
import datetime
from datetime import date, timedelta
import pandas as pd 
#import pygal


app = Flask(__name__)


@app.route("/")
def index():
    
    return render_template("index.html")


def get_predict(value):
    model = pickle.load(open('ARIMA_Model.plk', 'rb'))
    predictions = model.forecast(value+1)[0]
    predictions = pd.DataFrame(predictions)
    today = pd.datetime.today().strftime("%Y-%m-%d")
    predictions['Date'] = pd.date_range(start=today, periods=len(predictions), freq='D').strftime("%Y-%m-%d")
    predictions.set_index('Date', inplace=True)
    predictions.rename(columns={0: 'Prediction'}, inplace=True)
    forecast = predictions.iloc[1:].to_dict()
    return forecast

    #arima = pickle.load(open('ARIMA_Model.plk', 'rb'))
    #sarima = pickle.load(open('SARIMA_Model.plk', 'rb'))
    #result_arima =arima.forecast(value)[0]
    #result_sarima = sarima.forecast(value+1)
    #result_sarima = pd.DataFrame(result_sarima)[1:]
    #today = pd.datetime.today().strftime("%Y-%m-%d")
    #result_sarima['Date'] = pd.date_range(start=today, periods=len(result_sarima), freq='D')
    #result_sarima.set_index('Date', inplace=True)
    #result_sarima.rename(columns={0: 'SARIMA'}, inplace=True)
    
    #datetime_col = pd.date_range(start=today, periods=len(result_arima), freq="d")
    #predictions = pd.DataFrame(result_arima,index = datetime_col,columns=['arima'])
    #result_sarima['ARIMA'] = predictions
    #forecast = result_sarima.iloc[1:].to_dict()
    #return forecast
     



#def #plot_prediction(df):
   # graph = #pygal.Line()
   # graph.title = "Trying"
    #pgraph.x_lablels = df.index
    #graph.add(df)
    #graph_data = graph.render_data_uri()
    #return graph_data
def get_sarimax_forecast():

     #arima = pickle.load(open('ARIMA_Model.plk', 'rb'))
    sarima = pickle.load(open('SARIMA_Model.plk', 'rb'))
    #result_arima =arima.forecast(value)[0]
    result_sarima = sarima.forecast(value+1)
    result_sarima = pd.DataFrame(result_sarima)[1:]
    today = pd.datetime.today().strftime("%Y-%m-%d")
    result_sarima['Date'] = pd.date_range(start=today, periods=len(result_sarima), freq='D')
    result_sarima.set_index('Date', inplace=True)
    result_sarima.rename(columns={0: 'SARIMA'}, inplace=True)
    
    #datetime_col = pd.date_range(start=today, periods=len(result_arima), freq="d")
    #predictions = pd.DataFrame(result_arima,index = datetime_col,columns=['arima'])
    #result_sarima['ARIMA'] = predictions
    forecast = result_sarima.iloc[1:].to_dict()
    return forecast


def forecast_date(val_date):

    date_val = datetime.datetime.strptime(val_date, '%Y-%m-%d').date()
    tod = date.today()
    data = date(date_val.year, date_val.month, date_val.day) - tod  

    predict = get_predict(data.days)

    get_date=""
    get_value =0
    
    for key, value in predict.items():
       # for k, v in value.items()
       get_date = list(value.keys()) 
       get_value = list(value.values())
    
    userDate = datetime.fromisoformat(val_date)
    return get_value[get_date.index(userDate)]
    #today = pd.datetime.today().strftime("%Y-%m-%d")
    #startDate = today #userDate - timedelta(days=7)


@app.route("/result", methods=["POST"])
def result():
    d = request.form["Date-predict"]
    date_val = datetime.datetime.strptime(d, '%Y-%m-%d').date()
    tod = date.today()
    data = date(date_val.year, date_val.month, date_val.day) - tod  
    #print(forecast_date(d))
    forecast_date(d)
    return forecast_date(d)


@app.route("/",  methods=["POST"])
def predict():

    weekly = request.form["Weekly-predict"]
    

    #date_val = datetime.datetime.strptime(d, '%Y-%m-%d')
    #dat = date_val.date()
    #tod = date.today() #.strftime("%Y-%m-%d")
    #data = date(date_val.year, date_val.month, date_val.day) - tod  

    #if weekly < 1 | weekly > 30:
       # error = "Your prediction interval should be between 1 and 30."
       # return render_template("error.html", errortext=error)
    #else:






    predict = get_predict(int(weekly))
    
    data =predict['Prediction'].values()
    date =predict['Prediction'].keys()
    bar_labels=date
    bar_values=data
    mx = max(data)
    mn = min(data)

    if int(weekly) > 1:
        heading = "Forcast for the next {} days".format(weekly)
    else:
        heading = "Forcast for the next {} day".format(weekly)


    #graph = pygal.Line()
    #d = [22,43,54,56,67,78,77,88]
    #graph.x_labels = date
    #graph.add("",data)
    #graph = graph.render_data_uri()
    
    val = [1488.53,1489.07,1489.61,1490.02,1486.36,1491.24,1484.85]
    # val = {1:1488.53, 2: 1489.07, 3: 1489.61, 4: 1490.02, 5: 1486.36, 6: 1491.24, 7: 1484.85}


    return render_template("result.html", prediction=predict, values_list=val, forecast_title=heading, min = mn, max = mx, title='Forecast Results', labels=bar_labels, values=bar_values)


@app.route("/team")
def team():

    return render_template("team.html")



if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
