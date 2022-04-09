from django.shortcuts import render
from .models import btc_30M, btc_1H, btc_1D, eth_30M, eth_1H, eth_1D, bnb_30M, bnb_1H, bnb_1D, ada_30M, ada_1H, ada_1D, ltc_30M, ltc_1H, ltc_1D
from django.db.models import Q
from django.shortcuts import render

import yfinance as yf
import plotly.graph_objects as go
from plotly.offline import plot
from .predict_btc import btc_30M_download, btc_1H_download, btc_1D_download, btc_30M_LSTM_predict, btc_1H_LSTM_predict, btc_1D_LSTM_predict, btc_30M_LRG_predict, btc_1H_LRG_predict, btc_1D_LRG_predict
from .predict_eth import eth_30M_download, eth_1H_download, eth_1D_download, eth_30M_LSTM_predict, eth_1H_LSTM_predict, eth_1D_LSTM_predict, eth_30M_LRG_predict, eth_1H_LRG_predict, eth_1D_LRG_predict
from .predict_bnb import bnb_30M_download, bnb_1H_download, bnb_1D_download, bnb_30M_LSTM_predict, bnb_1H_LSTM_predict, bnb_1D_LSTM_predict, bnb_30M_LRG_predict, bnb_1H_LRG_predict, bnb_1D_LRG_predict
from .predict_ada import ada_30M_download, ada_1H_download, ada_1D_download, ada_30M_LSTM_predict, ada_1H_LSTM_predict, ada_1D_LSTM_predict, ada_30M_LRG_predict, ada_1H_LRG_predict, ada_1D_LRG_predict
from .predict_ltc import ltc_30M_download, ltc_1H_download, ltc_1D_download, ltc_30M_LSTM_predict, ltc_1H_LSTM_predict, ltc_1D_LSTM_predict, ltc_30M_LRG_predict, ltc_1H_LRG_predict, ltc_1D_LRG_predict
#--------------------------------------------------------------------------------------------------------
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

def predict_1d():
    print("-----------------------------Start prediction btc tf 1D-----------------------------")
    btc_1D_download()
    eth_1D_download()
    bnb_1D_download()
    ada_1D_download()
    ltc_1D_download()

    btc_1D_LSTM_predict()
    eth_1D_LSTM_predict()
    bnb_1D_LSTM_predict()
    ada_1D_LSTM_predict()
    ltc_1D_LSTM_predict()

    btc_1D_LRG_predict()
    eth_1D_LRG_predict()
    bnb_1D_LRG_predict()
    ada_1D_LRG_predict()
    ltc_1D_LRG_predict()

def predict_1h():
    print("-----------------------------Start prediction btc tf 1H-----------------------------")
    btc_1H_download()
    eth_1H_download()
    bnb_1H_download()
    ada_1H_download()
    ltc_1H_download()

    btc_1H_LSTM_predict()
    eth_1H_LSTM_predict()
    bnb_1H_LSTM_predict()
    ada_1H_LSTM_predict()
    ltc_1H_LSTM_predict()

    btc_1H_LRG_predict()
    eth_1H_LRG_predict()
    bnb_1H_LRG_predict()
    ada_1H_LRG_predict()
    ltc_1H_LRG_predict()

def predict_30min():
    print("-----------------------------Start prediction btc tf 30M-----------------------------")
    btc_30M_download()
    eth_30M_download()
    bnb_30M_download()
    ada_30M_download()
    ltc_30M_download()

    btc_30M_LSTM_predict()
    eth_30M_LSTM_predict()
    bnb_30M_LSTM_predict()
    ada_30M_LSTM_predict()
    ltc_30M_LSTM_predict()


    btc_30M_LRG_predict()
    eth_30M_LRG_predict()
    bnb_30M_LRG_predict()
    ada_30M_LRG_predict()
    ltc_30M_LRG_predict()

scheduler = BackgroundScheduler() 
scheduler.add_job(predict_30min, 'cron', minute='10,35')
scheduler.add_job(predict_1h, 'cron', hour='0-23', minute='5')
scheduler.add_job(predict_1d, 'cron', hour='7', minute='15')
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

def predict(request):
    return render(request,'predict/predict.html' )



#----LSTM----------------------------------------------------------------------------------------------
# BTC
def lstm_btc_30M(request):
    data = yf.download(tickers='BTC-USD', period = '2880M', interval = '30M')
    data = data[:-1]
    fig = go.Figure(data=[go.Candlestick(x=data.reset_index()['Datetime'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                customdata=data.reset_index()['Volume'],
                close=data['Close'],
                name='Real Prices')])

    fig.update_layout(title_text='BTC-USD GRAPH TF 30 MINUTE', title_x=0.5)

    find_btc = btc_30M.objects.filter(~Q(predict_LSTM=None))
    predictDate_list = []
    predict_list = []
    for predict_data in find_btc:
        predictDate_list.append(predict_data.Datetime)
        predict_list.append(predict_data.predict_LSTM)

    predict_list = predict_list[len(predict_list)-96:]
    predictDate_list = predictDate_list[len(predictDate_list)-96:]

    fig.add_trace(go.Scatter(x=predictDate_list, y=predict_list,
                            line=dict(color="#0085ff"),
                            mode='lines+markers',
                            name='Predictions',
                            marker=dict(size=5,color="#0085ff")
                            ))
    lstm_btc_30M = plot(fig, output_type="div", include_plotlyjs=True)

    context={'lstm_btc_30M': lstm_btc_30M}
    return render(request,'predict/lstm/btc/btc-30m.html',context )

def lstm_btc_1H(request):
    data = yf.download(tickers='BTC-USD', period = '7200M', interval = '60M')
    print(data)
    data = data[:-2]
    fig = go.Figure(data=[go.Candlestick(x=data.reset_index()['Datetime'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                customdata=data.reset_index()['Volume'],
                close=data['Close'],
                name='Real Prices')])
    fig.update_layout(title_text='BTC-USD GRAPH TF 1 HOUR', title_x=0.5)
    find_btc = btc_1H.objects.filter(~Q(predict_LSTM=None))
    predictDate_list = []
    predict_list = []
    for predict_data in find_btc:
        predictDate_list.append(predict_data.Datetime)
        predict_list.append(predict_data.predict_LSTM)

    predict_list = predict_list[len(predict_list)-96:]
    predictDate_list = predictDate_list[len(predictDate_list)-96:]
    fig.add_trace(go.Scatter(x=predictDate_list, y=predict_list,
                            line=dict(color="#0085ff"),
                            mode='lines+markers',
                            name='Predictions',
                            marker=dict(size=5,color="#0085ff")
                            ))
    lstm_btc_1H = plot(fig, output_type="div", include_plotlyjs=True)

    context={'lstm_btc_1H': lstm_btc_1H}
    return render(request,'predict/lstm/btc/btc-1h.html',context )

def lstm_btc_1D(request):
    data = yf.download(tickers='BTC-USD', period = '96D', interval = '1D')
    data = data[:-1]
    fig = go.Figure(data=[go.Candlestick(x=data.reset_index()['Date'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                customdata=data.reset_index()['Volume'],
                close=data['Close'],
                name='Real Prices')])
    fig.update_layout(title_text='BTC-USD GRAPH TF 1 DAY', title_x=0.5)
    find_btc = btc_1D.objects.filter(~Q(predict_LSTM=None))
    predictDate_list = []
    predict_list = []
    for predict_data in find_btc:
        predictDate_list.append(predict_data.Date)
        predict_list.append(predict_data.predict_LSTM)
    predict_list = predict_list[len(predict_list)-96:]
    predictDate_list = predictDate_list[len(predictDate_list)-96:]
    fig.add_trace(go.Scatter(x=predictDate_list, y=predict_list,
                            line=dict(color="#0085ff"),
                            mode='lines+markers',
                            name='Predictions',
                            marker=dict(size=5,color="#0085ff")
                            ))
    lstm_btc_1D = plot(fig, output_type="div", include_plotlyjs=True)

    context={'lstm_btc_1D': lstm_btc_1D}
    return render(request,'predict/lstm/btc/btc-1d.html',context )

# ETH
def lstm_eth_30M(request):
    data = yf.download(tickers='ETH-USD', period = '2880M', interval = '30M')
    data = data[:-1]
    fig = go.Figure(data=[go.Candlestick(x=data.reset_index()['Datetime'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                customdata=data.reset_index()['Volume'],
                close=data['Close'],
                name='Real Prices')])

    fig.update_layout(title_text='ETH-USD GRAPH TF 30 MINUTE', title_x=0.5)

    find_eth = eth_30M.objects.filter(~Q(predict_LSTM=None))
    predictDate_list = []
    predict_list = []
    for predict_data in find_eth:
        predictDate_list.append(predict_data.Datetime)
        predict_list.append(predict_data.predict_LSTM)

    predict_list = predict_list[len(predict_list)-96:]
    predictDate_list = predictDate_list[len(predictDate_list)-96:]

    fig.add_trace(go.Scatter(x=predictDate_list, y=predict_list,
                            line=dict(color="#0085ff"),
                            mode='lines+markers',
                            name='Predictions',
                            marker=dict(size=5,color="#0085ff")
                            ))
    lstm_eth_30M = plot(fig, output_type="div", include_plotlyjs=True)

    context={'lstm_eth_30M': lstm_eth_30M}
    return render(request,'predict/lstm/eth/eth-30m.html',context )

def lstm_eth_1H(request):
    data = yf.download(tickers='ETH-USD', period = '7200M', interval = '60M')
    print(data)
    data = data[:-2]
    fig = go.Figure(data=[go.Candlestick(x=data.reset_index()['Datetime'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                customdata=data.reset_index()['Volume'],
                close=data['Close'],
                name='Real Prices')])
    fig.update_layout(title_text='ETH-USD GRAPH TF 1 HOUR', title_x=0.5)
    find_eth = eth_1H.objects.filter(~Q(predict_LSTM=None))
    predictDate_list = []
    predict_list = []
    for predict_data in find_eth:
        predictDate_list.append(predict_data.Datetime)
        predict_list.append(predict_data.predict_LSTM)

    predict_list = predict_list[len(predict_list)-96:]
    predictDate_list = predictDate_list[len(predictDate_list)-96:]
    fig.add_trace(go.Scatter(x=predictDate_list, y=predict_list,
                            line=dict(color="#0085ff"),
                            mode='lines+markers',
                            name='Predictions',
                            marker=dict(size=5,color="#0085ff")
                            ))
    lstm_eth_1H = plot(fig, output_type="div", include_plotlyjs=True)

    context={'lstm_eth_1H': lstm_eth_1H}
    return render(request,'predict/lstm/eth/eth-1h.html',context )

def lstm_eth_1D(request):
    data = yf.download(tickers='ETH-USD', period = '96D', interval = '1D')
    data = data[:-1]
    fig = go.Figure(data=[go.Candlestick(x=data.reset_index()['Date'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                customdata=data.reset_index()['Volume'],
                close=data['Close'],
                name='Real Prices')])
    fig.update_layout(title_text='ETH-USD GRAPH TF 1 DAY', title_x=0.5)
    find_eth = eth_1D.objects.filter(~Q(predict_LSTM=None))
    predictDate_list = []
    predict_list = []
    for predict_data in find_eth:
        predictDate_list.append(predict_data.Date)
        predict_list.append(predict_data.predict_LSTM)
    predict_list = predict_list[len(predict_list)-96:]
    predictDate_list = predictDate_list[len(predictDate_list)-96:]
    fig.add_trace(go.Scatter(x=predictDate_list, y=predict_list,
                            line=dict(color="#0085ff"),
                            mode='lines+markers',
                            name='Predictions',
                            marker=dict(size=5,color="#0085ff")
                            ))
    lstm_eth_1D = plot(fig, output_type="div", include_plotlyjs=True)

    context={'lstm_eth_1D': lstm_eth_1D}
    return render(request,'predict/lstm/eth/eth-1d.html',context )

# BNB
def lstm_bnb_30M(request):
    data = yf.download(tickers='BNB-USD', period = '2880M', interval = '30M')
    data = data[:-1]
    fig = go.Figure(data=[go.Candlestick(x=data.reset_index()['Datetime'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                customdata=data.reset_index()['Volume'],
                close=data['Close'],
                name='Real Prices')])

    fig.update_layout(title_text='BNB-USD GRAPH TF 30 MINUTE', title_x=0.5)

    find_bnb = bnb_30M.objects.filter(~Q(predict_LSTM=None))
    predictDate_list = []
    predict_list = []
    for predict_data in find_bnb:
        predictDate_list.append(predict_data.Datetime)
        predict_list.append(predict_data.predict_LSTM)

    predict_list = predict_list[len(predict_list)-96:]
    predictDate_list = predictDate_list[len(predictDate_list)-96:]

    fig.add_trace(go.Scatter(x=predictDate_list, y=predict_list,
                            line=dict(color="#0085ff"),
                            mode='lines+markers',
                            name='Predictions',
                            marker=dict(size=5,color="#0085ff")
                            ))
    lstm_bnb_30M = plot(fig, output_type="div", include_plotlyjs=True)

    context={'lstm_bnb_30M': lstm_bnb_30M}
    return render(request,'predict/lstm/bnb/bnb-30m.html',context )

def lstm_bnb_1H(request):
    data = yf.download(tickers='BNB-USD', period = '7200M', interval = '60M')
    print(data)
    data = data[:-2]
    fig = go.Figure(data=[go.Candlestick(x=data.reset_index()['Datetime'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                customdata=data.reset_index()['Volume'],
                close=data['Close'],
                name='Real Prices')])
    fig.update_layout(title_text='BNB-USD GRAPH TF 1 HOUR', title_x=0.5)
    find_bnb = bnb_1H.objects.filter(~Q(predict_LSTM=None))
    predictDate_list = []
    predict_list = []
    for predict_data in find_bnb:
        predictDate_list.append(predict_data.Datetime)
        predict_list.append(predict_data.predict_LSTM)

    predict_list = predict_list[len(predict_list)-96:]
    predictDate_list = predictDate_list[len(predictDate_list)-96:]
    fig.add_trace(go.Scatter(x=predictDate_list, y=predict_list,
                            line=dict(color="#0085ff"),
                            mode='lines+markers',
                            name='Predictions',
                            marker=dict(size=5,color="#0085ff")
                            ))
    lstm_bnb_1H = plot(fig, output_type="div", include_plotlyjs=True)

    context={'lstm_bnb_1H': lstm_bnb_1H}
    return render(request,'predict/lstm/bnb/bnb-1h.html',context )

def lstm_bnb_1D(request):
    data = yf.download(tickers='BNB-USD', period = '96D', interval = '1D')
    data = data[:-1]
    fig = go.Figure(data=[go.Candlestick(x=data.reset_index()['Date'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                customdata=data.reset_index()['Volume'],
                close=data['Close'],
                name='Real Prices')])
    fig.update_layout(title_text='BNB-USD GRAPH TF 1 DAY', title_x=0.5)
    find_bnb = bnb_1D.objects.filter(~Q(predict_LSTM=None))
    predictDate_list = []
    predict_list = []
    for predict_data in find_bnb:
        predictDate_list.append(predict_data.Date)
        predict_list.append(predict_data.predict_LSTM)
    predict_list = predict_list[len(predict_list)-96:]
    predictDate_list = predictDate_list[len(predictDate_list)-96:]
    fig.add_trace(go.Scatter(x=predictDate_list, y=predict_list,
                            line=dict(color="#0085ff"),
                            mode='lines+markers',
                            name='Predictions',
                            marker=dict(size=5,color="#0085ff")
                            ))
    lstm_bnb_1D = plot(fig, output_type="div", include_plotlyjs=True)

    context={'lstm_bnb_1D': lstm_bnb_1D}
    return render(request,'predict/lstm/bnb/bnb-1d.html',context )

# ADA
def lstm_ada_30M(request):
    data = yf.download(tickers='ADA-USD', period = '2880M', interval = '30M')
    data = data[:-1]
    fig = go.Figure(data=[go.Candlestick(x=data.reset_index()['Datetime'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                customdata=data.reset_index()['Volume'],
                close=data['Close'],
                name='Real Prices')])

    fig.update_layout(title_text='ADA-USD GRAPH TF 30 MINUTE', title_x=0.5)

    find_ada = ada_30M.objects.filter(~Q(predict_LSTM=None))
    predictDate_list = []
    predict_list = []
    for predict_data in find_ada:
        predictDate_list.append(predict_data.Datetime)
        predict_list.append(predict_data.predict_LSTM)

    predict_list = predict_list[len(predict_list)-96:]
    predictDate_list = predictDate_list[len(predictDate_list)-96:]

    fig.add_trace(go.Scatter(x=predictDate_list, y=predict_list,
                            line=dict(color="#0085ff"),
                            mode='lines+markers',
                            name='Predictions',
                            marker=dict(size=5,color="#0085ff")
                            ))
    lstm_ada_30M = plot(fig, output_type="div", include_plotlyjs=True)

    context={'lstm_ada_30M': lstm_ada_30M}
    return render(request,'predict/lstm/ada/ada-30m.html',context )

def lstm_ada_1H(request):
    data = yf.download(tickers='ADA-USD', period = '7200M', interval = '60M')
    print(data)
    data = data[:-2]
    fig = go.Figure(data=[go.Candlestick(x=data.reset_index()['Datetime'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                customdata=data.reset_index()['Volume'],
                close=data['Close'],
                name='Real Prices')])
    fig.update_layout(title_text='ADA-USD GRAPH TF 1 HOUR', title_x=0.5)
    find_ada = ada_1H.objects.filter(~Q(predict_LSTM=None))
    predictDate_list = []
    predict_list = []
    for predict_data in find_ada:
        predictDate_list.append(predict_data.Datetime)
        predict_list.append(predict_data.predict_LSTM)

    predict_list = predict_list[len(predict_list)-96:]
    predictDate_list = predictDate_list[len(predictDate_list)-96:]
    fig.add_trace(go.Scatter(x=predictDate_list, y=predict_list,
                            line=dict(color="#0085ff"),
                            mode='lines+markers',
                            name='Predictions',
                            marker=dict(size=5,color="#0085ff")
                            ))
    lstm_ada_1H = plot(fig, output_type="div", include_plotlyjs=True)

    context={'lstm_ada_1H': lstm_ada_1H}
    return render(request,'predict/lstm/ada/ada-1h.html',context )

def lstm_ada_1D(request):
    data = yf.download(tickers='ADA-USD', period = '96D', interval = '1D')
    data = data[:-1]
    fig = go.Figure(data=[go.Candlestick(x=data.reset_index()['Date'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                customdata=data.reset_index()['Volume'],
                close=data['Close'],
                name='Real Prices')])
    fig.update_layout(title_text='ADA-USD GRAPH TF 1 DAY', title_x=0.5)
    find_ada = ada_1D.objects.filter(~Q(predict_LSTM=None))
    predictDate_list = []
    predict_list = []
    for predict_data in find_ada:
        predictDate_list.append(predict_data.Date)
        predict_list.append(predict_data.predict_LSTM)
    predict_list = predict_list[len(predict_list)-96:]
    predictDate_list = predictDate_list[len(predictDate_list)-96:]
    fig.add_trace(go.Scatter(x=predictDate_list, y=predict_list,
                            line=dict(color="#0085ff"),
                            mode='lines+markers',
                            name='Predictions',
                            marker=dict(size=5,color="#0085ff")
                            ))
    lstm_ada_1D = plot(fig, output_type="div", include_plotlyjs=True)

    context={'lstm_ada_1D': lstm_ada_1D}
    return render(request,'predict/lstm/ada/ada-1d.html',context )

# LTC
def lstm_ltc_30M(request):
    data = yf.download(tickers='LTC-USD', period = '2880M', interval = '30M')
    data = data[:-1]
    fig = go.Figure(data=[go.Candlestick(x=data.reset_index()['Datetime'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                customdata=data.reset_index()['Volume'],
                close=data['Close'],
                name='Real Prices')])

    fig.update_layout(title_text='LTC-USD GRAPH TF 30 MINUTE', title_x=0.5)

    find_ltc = ltc_30M.objects.filter(~Q(predict_LSTM=None))
    predictDate_list = []
    predict_list = []
    for predict_data in find_ltc:
        predictDate_list.append(predict_data.Datetime)
        predict_list.append(predict_data.predict_LSTM)

    predict_list = predict_list[len(predict_list)-96:]
    predictDate_list = predictDate_list[len(predictDate_list)-96:]

    fig.add_trace(go.Scatter(x=predictDate_list, y=predict_list,
                            line=dict(color="#0085ff"),
                            mode='lines+markers',
                            name='Predictions',
                            marker=dict(size=5,color="#0085ff")
                            ))
    lstm_ltc_30M = plot(fig, output_type="div", include_plotlyjs=True)

    context={'lstm_ltc_30M': lstm_ltc_30M}
    return render(request,'predict/lstm/ltc/ltc-30m.html',context )

def lstm_ltc_1H(request):
    data = yf.download(tickers='LTC-USD', period = '7200M', interval = '60M')
    print(data)
    data = data[:-2]
    fig = go.Figure(data=[go.Candlestick(x=data.reset_index()['Datetime'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                customdata=data.reset_index()['Volume'],
                close=data['Close'],
                name='Real Prices')])
    fig.update_layout(title_text='LTC-USD GRAPH TF 1 HOUR', title_x=0.5)
    find_ltc = ltc_1H.objects.filter(~Q(predict_LSTM=None))
    predictDate_list = []
    predict_list = []
    for predict_data in find_ltc:
        predictDate_list.append(predict_data.Datetime)
        predict_list.append(predict_data.predict_LSTM)

    predict_list = predict_list[len(predict_list)-96:]
    predictDate_list = predictDate_list[len(predictDate_list)-96:]
    fig.add_trace(go.Scatter(x=predictDate_list, y=predict_list,
                            line=dict(color="#0085ff"),
                            mode='lines+markers',
                            name='Predictions',
                            marker=dict(size=5,color="#0085ff")
                            ))
    lstm_ltc_1H = plot(fig, output_type="div", include_plotlyjs=True)

    context={'lstm_ltc_1H': lstm_ada_1H}
    return render(request,'predict/lstm/ltc/ltc-1h.html',context )

def lstm_ltc_1D(request):
    data = yf.download(tickers='LTC-USD', period = '96D', interval = '1D')
    data = data[:-1]
    fig = go.Figure(data=[go.Candlestick(x=data.reset_index()['Date'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                customdata=data.reset_index()['Volume'],
                close=data['Close'],
                name='Real Prices')])
    fig.update_layout(title_text='LTC-USD GRAPH TF 1 DAY', title_x=0.5)
    find_ltc = ltc_1D.objects.filter(~Q(predict_LSTM=None))
    predictDate_list = []
    predict_list = []
    for predict_data in find_ltc:
        predictDate_list.append(predict_data.Date)
        predict_list.append(predict_data.predict_LSTM)
    predict_list = predict_list[len(predict_list)-96:]
    predictDate_list = predictDate_list[len(predictDate_list)-96:]
    fig.add_trace(go.Scatter(x=predictDate_list, y=predict_list,
                            line=dict(color="#0085ff"),
                            mode='lines+markers',
                            name='Predictions',
                            marker=dict(size=5,color="#0085ff")
                            ))
    lstm_ltc_1D = plot(fig, output_type="div", include_plotlyjs=True)

    context={'lstm_ltc_1D': lstm_ltc_1D}
    return render(request,'predict/lstm/ltc/ltc-1d.html',context )


#----LRG----------------------------------------------------------------------------------------------
# BTC
def lrg_btc_30M(request):
    data = yf.download(tickers='BTC-USD', period = '2880M', interval = '30M')
    data = data[:-1]
    fig = go.Figure(data=[go.Candlestick(x=data.reset_index()['Datetime'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                customdata=data.reset_index()['Volume'],
                close=data['Close'],
                name='Real Prices')])
    fig.update_layout(title_text='BTC-USD GRAPH TF 30 MINUTE', title_x=0.5)

    find_btc = btc_30M.objects.filter(~Q(predict_LRG=None))
    predictDate_list = []
    predict_list = []
    for predict_data in find_btc:
        predictDate_list.append(predict_data.Datetime)
        predict_list.append(predict_data.predict_LRG)

    predict_list = predict_list[len(predict_list)-96:]
    predictDate_list = predictDate_list[len(predictDate_list)-96:]

    fig.add_trace(go.Scatter(x=predictDate_list, y=predict_list,
                            line=dict(color="#0085ff"),
                            mode='lines+markers',
                            name='Predictions',
                            marker=dict(size=5,color="#0085ff")
                            ))
    lrg_btc_30M = plot(fig, output_type="div", include_plotlyjs=True)

    context={'lrg_btc_30M': lrg_btc_30M}
    return render(request,'predict/lrg/btc/btc-30m.html',context )

def lrg_btc_1H(request):
    data = yf.download(tickers='BTC-USD', period = '7200M', interval = '60M')
    print(data)
    data = data[:-2]
    fig = go.Figure(data=[go.Candlestick(x=data.reset_index()['Datetime'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                customdata=data.reset_index()['Volume'],
                close=data['Close'],
                name='Real Prices')])
    fig.update_layout(title_text='BTC-USD GRAPH TF 1 HOUR', title_x=0.5)
    find_btc = btc_1H.objects.filter(~Q(predict_LSTM=None))
    predictDate_list = []
    predict_list = []
    for predict_data in find_btc:
        predictDate_list.append(predict_data.Datetime)
        predict_list.append(predict_data.predict_LSTM)

    predict_list = predict_list[len(predict_list)-96:]
    predictDate_list = predictDate_list[len(predictDate_list)-96:]
    fig.add_trace(go.Scatter(x=predictDate_list, y=predict_list,
                            line=dict(color="#0085ff"),
                            mode='lines+markers',
                            name='Predictions',
                            marker=dict(size=5,color="#0085ff")
                            ))
    lrg_btc_1H = plot(fig, output_type="div", include_plotlyjs=True)

    context={'lrg_btc_1H': lrg_btc_1H}
    return render(request,'predict/lrg/btc/btc-1h.html',context )

def lrg_btc_1D(request):
    data = yf.download(tickers='BTC-USD', period = '96D', interval = '1D')
    data = data[:-1]
    fig = go.Figure(data=[go.Candlestick(x=data.reset_index()['Date'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                customdata=data.reset_index()['Volume'],
                close=data['Close'],
                name='Real Prices')])
    fig.update_layout(title_text='BTC-USD GRAPH TF 1 DAY', title_x=0.5)

    find_btc = btc_1D.objects.filter(~Q(predict_LRG=None))
    predictDate_list = []
    predict_list = []
    for predict_data in find_btc:
        predictDate_list.append(predict_data.Date)
        predict_list.append(predict_data.predict_LRG)

    predict_list = predict_list[len(predict_list)-96:]
    predictDate_list = predictDate_list[len(predictDate_list)-96:]
    fig.add_trace(go.Scatter(x=predictDate_list, y=predict_list,
                            line=dict(color="#0085ff"),
                            mode='lines+markers',
                            name='Predictions',
                            marker=dict(size=5,color="#0085ff")
                            ))
    lrg_btc_1D = plot(fig, output_type="div", include_plotlyjs=True)
    context={'lrg_btc_1D': lrg_btc_1D}
    return render(request,'predict/lrg/btc/btc-1d.html',context )

# ETH
def lrg_eth_30M(request):
    data = yf.download(tickers='ETH-USD', period = '2880M', interval = '30M')
    data = data[:-1]
    fig = go.Figure(data=[go.Candlestick(x=data.reset_index()['Datetime'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                customdata=data.reset_index()['Volume'],
                close=data['Close'],
                name='Real Prices')])
    fig.update_layout(title_text='ETH-USD GRAPH TF 30 MINUTE', title_x=0.5)

    find_eth = eth_30M.objects.filter(~Q(predict_LRG=None))
    predictDate_list = []
    predict_list = []
    for predict_data in find_eth:
        predictDate_list.append(predict_data.Datetime)
        predict_list.append(predict_data.predict_LRG)

    predict_list = predict_list[len(predict_list)-96:]
    predictDate_list = predictDate_list[len(predictDate_list)-96:]

    fig.add_trace(go.Scatter(x=predictDate_list, y=predict_list,
                            line=dict(color="#0085ff"),
                            mode='lines+markers',
                            name='Predictions',
                            marker=dict(size=5,color="#0085ff")
                            ))
    lrg_eth_30M = plot(fig, output_type="div", include_plotlyjs=True)

    context={'lrg_eth_30M': lrg_eth_30M}
    return render(request,'predict/lrg/eth/eth-30m.html',context )

def lrg_eth_1H(request):
    data = yf.download(tickers='ETH-USD', period = '7200M', interval = '60M')
    print(data)
    data = data[:-2]
    fig = go.Figure(data=[go.Candlestick(x=data.reset_index()['Datetime'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                customdata=data.reset_index()['Volume'],
                close=data['Close'],
                name='Real Prices')])
    fig.update_layout(title_text='ETH-USD GRAPH TF 1 HOUR', title_x=0.5)
    find_eth = eth_1H.objects.filter(~Q(predict_LSTM=None))
    predictDate_list = []
    predict_list = []
    for predict_data in find_eth:
        predictDate_list.append(predict_data.Datetime)
        predict_list.append(predict_data.predict_LSTM)

    predict_list = predict_list[len(predict_list)-96:]
    predictDate_list = predictDate_list[len(predictDate_list)-96:]
    fig.add_trace(go.Scatter(x=predictDate_list, y=predict_list,
                            line=dict(color="#0085ff"),
                            mode='lines+markers',
                            name='Predictions',
                            marker=dict(size=5,color="#0085ff")
                            ))
    lrg_eth_1H = plot(fig, output_type="div", include_plotlyjs=True)

    context={'lrg_eth_1H': lrg_eth_1H}
    return render(request,'predict/lrg/eth/eth-1h.html',context )

def lrg_eth_1D(request):
    data = yf.download(tickers='ETH-USD', period = '96D', interval = '1D')
    data = data[:-1]
    fig = go.Figure(data=[go.Candlestick(x=data.reset_index()['Date'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                customdata=data.reset_index()['Volume'],
                close=data['Close'],
                name='Real Prices')])
    fig.update_layout(title_text='ETH-USD GRAPH TF 1 DAY', title_x=0.5)

    find_eth = eth_1D.objects.filter(~Q(predict_LRG=None))
    predictDate_list = []
    predict_list = []
    for predict_data in find_eth:
        predictDate_list.append(predict_data.Date)
        predict_list.append(predict_data.predict_LRG)

    predict_list = predict_list[len(predict_list)-96:]
    predictDate_list = predictDate_list[len(predictDate_list)-96:]
    fig.add_trace(go.Scatter(x=predictDate_list, y=predict_list,
                            line=dict(color="#0085ff"),
                            mode='lines+markers',
                            name='Predictions',
                            marker=dict(size=5,color="#0085ff")
                            ))
    lrg_eth_1D = plot(fig, output_type="div", include_plotlyjs=True)
    context={'lrg_eth_1D': lrg_eth_1D}
    return render(request,'predict/lrg/eth/eth-1d.html',context )

# BNB
def lrg_bnb_30M(request):
    data = yf.download(tickers='BNB-USD', period = '2880M', interval = '30M')
    data = data[:-1]
    fig = go.Figure(data=[go.Candlestick(x=data.reset_index()['Datetime'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                customdata=data.reset_index()['Volume'],
                close=data['Close'],
                name='Real Prices')])
    fig.update_layout(title_text='BNB-USD GRAPH TF 30 MINUTE', title_x=0.5)

    find_bnb = bnb_30M.objects.filter(~Q(predict_LRG=None))
    predictDate_list = []
    predict_list = []
    for predict_data in find_bnb:
        predictDate_list.append(predict_data.Datetime)
        predict_list.append(predict_data.predict_LRG)

    predict_list = predict_list[len(predict_list)-96:]
    predictDate_list = predictDate_list[len(predictDate_list)-96:]

    fig.add_trace(go.Scatter(x=predictDate_list, y=predict_list,
                            line=dict(color="#0085ff"),
                            mode='lines+markers',
                            name='Predictions',
                            marker=dict(size=5,color="#0085ff")
                            ))
    lrg_bnb_30M = plot(fig, output_type="div", include_plotlyjs=True)

    context={'lrg_bnb_30M': lrg_bnb_30M}
    return render(request,'predict/lrg/bnb/bnb-30m.html',context )

def lrg_bnb_1H(request):
    data = yf.download(tickers='BNB-USD', period = '7200M', interval = '60M')
    print(data)
    data = data[:-2]
    fig = go.Figure(data=[go.Candlestick(x=data.reset_index()['Datetime'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                customdata=data.reset_index()['Volume'],
                close=data['Close'],
                name='Real Prices')])
    fig.update_layout(title_text='BNB-USD GRAPH TF 1 HOUR', title_x=0.5)
    find_bnb = bnb_1H.objects.filter(~Q(predict_LSTM=None))
    predictDate_list = []
    predict_list = []
    for predict_data in find_bnb:
        predictDate_list.append(predict_data.Datetime)
        predict_list.append(predict_data.predict_LSTM)

    predict_list = predict_list[len(predict_list)-96:]
    predictDate_list = predictDate_list[len(predictDate_list)-96:]
    fig.add_trace(go.Scatter(x=predictDate_list, y=predict_list,
                            line=dict(color="#0085ff"),
                            mode='lines+markers',
                            name='Predictions',
                            marker=dict(size=5,color="#0085ff")
                            ))
    lrg_bnb_1H = plot(fig, output_type="div", include_plotlyjs=True)

    context={'lrg_bnb_1H': lrg_bnb_1H}
    return render(request,'predict/lrg/bnb/bnb-1h.html',context )

def lrg_bnb_1D(request):
    data = yf.download(tickers='BNB-USD', period = '96D', interval = '1D')
    data = data[:-1]
    fig = go.Figure(data=[go.Candlestick(x=data.reset_index()['Date'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                customdata=data.reset_index()['Volume'],
                close=data['Close'],
                name='Real Prices')])
    fig.update_layout(title_text='BNB-USD GRAPH TF 1 DAY', title_x=0.5)

    find_bnb = bnb_1D.objects.filter(~Q(predict_LRG=None))
    predictDate_list = []
    predict_list = []
    for predict_data in find_bnb:
        predictDate_list.append(predict_data.Date)
        predict_list.append(predict_data.predict_LRG)

    predict_list = predict_list[len(predict_list)-96:]
    predictDate_list = predictDate_list[len(predictDate_list)-96:]
    fig.add_trace(go.Scatter(x=predictDate_list, y=predict_list,
                            line=dict(color="#0085ff"),
                            mode='lines+markers',
                            name='Predictions',
                            marker=dict(size=5,color="#0085ff")
                            ))
    lrg_bnb_1D = plot(fig, output_type="div", include_plotlyjs=True)
    context={'lrg_bnb_1D': lrg_bnb_1D}
    return render(request,'predict/lrg/bnb/bnb-1d.html',context )

# ADA
def lrg_ada_30M(request):
    data = yf.download(tickers='ADA-USD', period = '2880M', interval = '30M')
    data = data[:-1]
    fig = go.Figure(data=[go.Candlestick(x=data.reset_index()['Datetime'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                customdata=data.reset_index()['Volume'],
                close=data['Close'],
                name='Real Prices')])
    fig.update_layout(title_text='ADA-USD GRAPH TF 30 MINUTE', title_x=0.5)

    find_ada = ada_30M.objects.filter(~Q(predict_LRG=None))
    predictDate_list = []
    predict_list = []
    for predict_data in find_ada:
        predictDate_list.append(predict_data.Datetime)
        predict_list.append(predict_data.predict_LRG)

    predict_list = predict_list[len(predict_list)-96:]
    predictDate_list = predictDate_list[len(predictDate_list)-96:]

    fig.add_trace(go.Scatter(x=predictDate_list, y=predict_list,
                            line=dict(color="#0085ff"),
                            mode='lines+markers',
                            name='Predictions',
                            marker=dict(size=5,color="#0085ff")
                            ))
    lrg_ada_30M = plot(fig, output_type="div", include_plotlyjs=True)

    context={'lrg_ada_30M': lrg_ada_30M}
    return render(request,'predict/lrg/ada/ada-30m.html',context )

def lrg_ada_1H(request):
    data = yf.download(tickers='ADA-USD', period = '7200M', interval = '60M')
    print(data)
    data = data[:-2]
    fig = go.Figure(data=[go.Candlestick(x=data.reset_index()['Datetime'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                customdata=data.reset_index()['Volume'],
                close=data['Close'],
                name='Real Prices')])
    fig.update_layout(title_text='ADA-USD GRAPH TF 1 HOUR', title_x=0.5)
    find_ada = ada_1H.objects.filter(~Q(predict_LSTM=None))
    predictDate_list = []
    predict_list = []
    for predict_data in find_ada:
        predictDate_list.append(predict_data.Datetime)
        predict_list.append(predict_data.predict_LSTM)

    predict_list = predict_list[len(predict_list)-96:]
    predictDate_list = predictDate_list[len(predictDate_list)-96:]
    fig.add_trace(go.Scatter(x=predictDate_list, y=predict_list,
                            line=dict(color="#0085ff"),
                            mode='lines+markers',
                            name='Predictions',
                            marker=dict(size=5,color="#0085ff")
                            ))
    lrg_ada_1H = plot(fig, output_type="div", include_plotlyjs=True)

    context={'lrg_ada_1H': lrg_ada_1H}
    return render(request,'predict/lrg/ada/ada-1h.html',context )

def lrg_ada_1D(request):
    data = yf.download(tickers='ADA-USD', period = '96D', interval = '1D')
    data = data[:-1]
    fig = go.Figure(data=[go.Candlestick(x=data.reset_index()['Date'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                customdata=data.reset_index()['Volume'],
                close=data['Close'],
                name='Real Prices')])
    fig.update_layout(title_text='ADA-USD GRAPH TF 1 DAY', title_x=0.5)

    find_ada = ada_1D.objects.filter(~Q(predict_LRG=None))
    predictDate_list = []
    predict_list = []
    for predict_data in find_ada:
        predictDate_list.append(predict_data.Date)
        predict_list.append(predict_data.predict_LRG)

    predict_list = predict_list[len(predict_list)-96:]
    predictDate_list = predictDate_list[len(predictDate_list)-96:]
    fig.add_trace(go.Scatter(x=predictDate_list, y=predict_list,
                            line=dict(color="#0085ff"),
                            mode='lines+markers',
                            name='Predictions',
                            marker=dict(size=5,color="#0085ff")
                            ))
    lrg_ada_1D = plot(fig, output_type="div", include_plotlyjs=True)
    context={'lrg_ada_1D': lrg_ada_1D}
    return render(request,'predict/lrg/ada/ada-1d.html',context )


# LTC
def lrg_ltc_30M(request):
    data = yf.download(tickers='LTC-USD', period = '2880M', interval = '30M')
    data = data[:-1]
    fig = go.Figure(data=[go.Candlestick(x=data.reset_index()['Datetime'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                customdata=data.reset_index()['Volume'],
                close=data['Close'],
                name='Real Prices')])
    fig.update_layout(title_text='LTC-USD GRAPH TF 30 MINUTE', title_x=0.5)

    find_ltc = ltc_30M.objects.filter(~Q(predict_LRG=None))
    predictDate_list = []
    predict_list = []
    for predict_data in find_ltc:
        predictDate_list.append(predict_data.Datetime)
        predict_list.append(predict_data.predict_LRG)

    predict_list = predict_list[len(predict_list)-96:]
    predictDate_list = predictDate_list[len(predictDate_list)-96:]

    fig.add_trace(go.Scatter(x=predictDate_list, y=predict_list,
                            line=dict(color="#0085ff"),
                            mode='lines+markers',
                            name='Predictions',
                            marker=dict(size=5,color="#0085ff")
                            ))
    lrg_ltc_30M = plot(fig, output_type="div", include_plotlyjs=True)

    context={'lrg_ltc_30M': lrg_ltc_30M}
    return render(request,'predict/lrg/ltc/ltc-30m.html',context )

def lrg_ltc_1H(request):
    data = yf.download(tickers='LTC-USD', period = '7200M', interval = '60M')
    print(data)
    data = data[:-2]
    fig = go.Figure(data=[go.Candlestick(x=data.reset_index()['Datetime'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                customdata=data.reset_index()['Volume'],
                close=data['Close'],
                name='Real Prices')])
    fig.update_layout(title_text='LTC-USD GRAPH TF 1 HOUR', title_x=0.5)
    find_ltc = ltc_1H.objects.filter(~Q(predict_LSTM=None))
    predictDate_list = []
    predict_list = []
    for predict_data in find_ltc:
        predictDate_list.append(predict_data.Datetime)
        predict_list.append(predict_data.predict_LSTM)

    predict_list = predict_list[len(predict_list)-96:]
    predictDate_list = predictDate_list[len(predictDate_list)-96:]
    fig.add_trace(go.Scatter(x=predictDate_list, y=predict_list,
                            line=dict(color="#0085ff"),
                            mode='lines+markers',
                            name='Predictions',
                            marker=dict(size=5,color="#0085ff")
                            ))
    lrg_ltc_1H = plot(fig, output_type="div", include_plotlyjs=True)

    context={'lrg_ltc_1H': lrg_ltc_1H}
    return render(request,'predict/lrg/ltc/ltc-1h.html',context )

def lrg_ltc_1D(request):
    data = yf.download(tickers='LTC-USD', period = '96D', interval = '1D')
    data = data[:-1]
    fig = go.Figure(data=[go.Candlestick(x=data.reset_index()['Date'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                customdata=data.reset_index()['Volume'],
                close=data['Close'],
                name='Real Prices')])
    fig.update_layout(title_text='LTC-USD GRAPH TF 1 DAY', title_x=0.5)

    find_ltc = ltc_1D.objects.filter(~Q(predict_LRG=None))
    predictDate_list = []
    predict_list = []
    for predict_data in find_ltc:
        predictDate_list.append(predict_data.Date)
        predict_list.append(predict_data.predict_LRG)

    predict_list = predict_list[len(predict_list)-96:]
    predictDate_list = predictDate_list[len(predictDate_list)-96:]
    fig.add_trace(go.Scatter(x=predictDate_list, y=predict_list,
                            line=dict(color="#0085ff"),
                            mode='lines+markers',
                            name='Predictions',
                            marker=dict(size=5,color="#0085ff")
                            ))
    lrg_ltc_1D = plot(fig, output_type="div", include_plotlyjs=True)
    context={'lrg_ltc_1D': lrg_ltc_1D}
    return render(request,'predict/lrg/ltc/ltc-1d.html',context )