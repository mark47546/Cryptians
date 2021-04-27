from django.shortcuts import render
from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from pusher import Pusher
import requests, json, atexit, time, plotly, plotly.graph_objs as go

app = Flask(__name__)

pusher = Pusher(
    app_id='1195196',
    key='625a73db17ed3f2a2abf',
    secret='02041080918b6106a057',
    cluster='ap1',
    ssl=True
    )

times = []
currencies = ["BTC"]
prices = {"BTC": []}


def index(request):
    return render(request, 'index.html')

def retrieve_data():
        # create dictionary for saving current prices
        current_prices = {}
        for currency in currencies:
            current_prices[currency] = []
        # append new time to list of times
        times.append(time.strftime('%H:%M:%S'))

        # make request to API and get response as object
        api_url = "https://min-api.cryptocompare.com/data/pricemulti?fsyms={}&tsyms=USD".format(",".join(currencies))
        response = json.loads(requests.get(api_url).content)

        # append new price to list of prices for graph
        # and set current price for bar chart
        for currency in currencies:
            price = response[currency]['USD']
            current_prices[currency] = price
            prices[currency].append(price)

        # create an array of traces for graph data
        graph_data = [go.Scatter(
            x=times,
            y=prices.get(currency),
            name="{} Prices".format(currency)
        ) for currency in currencies]

        # create an array of traces for bar chart data
        bar_chart_data = [go.Bar(
            x=currencies,
            y=list(current_prices.values())
        )]

        data = {
            'graph': json.dumps(list(graph_data), cls=plotly.utils.PlotlyJSONEncoder),
            'bar_chart': json.dumps(list(bar_chart_data), cls=plotly.utils.PlotlyJSONEncoder)
        }

        # trigger event
        pusher.trigger("crypto", "data-updated", data)

        scheduler = BackgroundScheduler()
        scheduler.start()
        scheduler.add_job(
        func=retrieve_data,
        trigger=IntervalTrigger(seconds=10),
        id='prices_retrieval_job',
        name='Retrieve prices every 10 seconds',
        replace_existing=True)
        # Shut down the scheduler when exiting the app
        atexit.register(lambda: scheduler.shutdown())

        app.run(debug=True, use_reloader=False)