from pyexpat import model
from django.shortcuts import render, redirect
from predict.models import btc_1D, eth_1D, bnb_1D, ada_1D, ltc_1D
from .models import Trade, demoAccount
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import TradeForm
import yfinance as yf
from django.contrib.auth.decorators import login_required

@login_required
def DemoAccount(request):
    get_user = request.user
    try:
        account = demoAccount.objects.get(user = get_user.id)
    except:
        account = demoAccount.objects.create(user = get_user)

    btc = yf.download(tickers='BTC-USD', period = '1D', interval = '1D')
    eth = yf.download(tickers='ETH-USD', period = '1D', interval = '1D')
    bnb = yf.download(tickers='BNB-USD', period = '1D', interval = '1D')
    ada = yf.download(tickers='ADA-USD', period = '1D', interval = '1D')
    ltc = yf.download(tickers='LTC-USD', period = '1D', interval = '1D')
    btc_to_usd = account.btc * float(btc.reset_index()['Close'][0])
    eth_to_usd = account.eth * float(eth.reset_index()['Close'][0])
    bnb_to_usd = account.bnb * float(bnb.reset_index()['Close'][0])
    ada_to_usd = account.ada * float(ada.reset_index()['Close'][0])
    ltc_to_usd = account.ltc * float(ltc.reset_index()['Close'][0])

    profit = account.balance + btc_to_usd + eth_to_usd + bnb_to_usd + ada_to_usd + ltc_to_usd - 100000
    percen_profit = profit / 1000

    return render(request,'demo-account/myaccount.html',{'account':account, 'profit':profit, 'percen_profit':percen_profit, 'btc_to_usd':btc_to_usd, 'eth_to_usd':eth_to_usd, 'bnb_to_usd':bnb_to_usd, 'ada_to_usd':ada_to_usd, 'ltc_to_usd':ltc_to_usd})
@login_required
def history(request):
    search = request.GET.get('search')
    get_account = demoAccount.objects.get(user = request.user)
    history = Trade.objects.filter(account = get_account)
    if search:
        history = history.filter(Q(coin__icontains=search) | Q(option__icontains=search))
    else:
        pass
    
    paginator = Paginator(history, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'demo-account/history.html',{'history':page_obj})
@login_required
def tradeBTC(request):
    get_user = request.user
    account = demoAccount.objects.get(user = get_user.id)
    btc_1d = btc_1D.objects.all().order_by('-id')[:2]
    if btc_1d[0].predict_LSTM != None and btc_1d[0].predict_LSTM > btc_1d[1].predict_LSTM:
        lstm = "B U Y"
    else:
        lstm = "S E L L"
    if btc_1d[0].predict_LRG != None and btc_1d[0].predict_LRG > btc_1d[1].predict_LRG:
        lrg = "B U Y"
    else:
        lrg = "S E L L"
    if btc_1d[0].predict_MACD == 'buy':
        macd = "B U Y"
    elif btc_1d[0].predict_MACD == 'sell':
        macd = "S E L L"
    else:
        macd = "H O L D"
    if request.method == "POST":
        form = TradeForm(request.POST)
        data = yf.download(tickers='BTC-USD', period = '1D', interval = '1D')
        if form.is_valid():
            form = form.save(commit=False)
            form.price = float(data.reset_index()['Close'][0])
            if form.option == "buy" and form.buy_amount != 0:
                form.sell_amount = None
                get_btc = (form.buy_amount / form.price)+account.btc
                get_balance = account.balance - form.buy_amount
                account = demoAccount.objects.filter(user = get_user.id).update(balance = get_balance, btc = get_btc)
            elif form.option == "sell" and form.sell_amount != 0:
                form.buy_amount = None
                sell_btc = account.btc - form.sell_amount
                get_balance = account.balance + (form.sell_amount * form.price)
                account = demoAccount.objects.filter(user = get_user.id).update(balance = get_balance, btc = sell_btc)
            else:
                error = "The value should more than 0"
                form = TradeForm(initial={'account':account, 'coin':"btc"})
                return render(request,'demo-account/trade/trade_btc.html', {'form':form, 'account':account, 'error':error, 'lstm':lstm, 'lrg':lrg, 'macd':macd})
            form.save()
            return redirect("/demoaccount")
        
        return render(request,'demo-account/trade/trade_btc.html', {'form':form, 'account':account, 'lstm':lstm, 'lrg':lrg, 'macd':macd})

    else:
        form = TradeForm(initial={'account':account, 'coin':"btc"})
        return render(request,'demo-account/trade/trade_btc.html', {'form':form, 'account':account, 'lstm':lstm, 'lrg':lrg, 'macd':macd})

@login_required
def tradeETH(request):
    get_user = request.user
    account = demoAccount.objects.get(user = get_user.id)
    eth_1d = eth_1D.objects.all().order_by('-id')[:2]
    if eth_1d[0].predict_LSTM != None and eth_1d[0].predict_LSTM > eth_1d[1].predict_LSTM:
        lstm = "B U Y"
    else:
        lstm = "S E L L"
    if eth_1d[0].predict_LSTM != None and eth_1d[0].predict_LRG > eth_1d[1].predict_LRG:
        lrg = "B U Y"
    else:
        lrg = "S E L L"
    if eth_1d[0].predict_MACD == 'buy':
        macd = "B U Y"
    elif eth_1d[0].predict_MACD == 'sell':
        macd = "S E L L"
    else:
        macd = "H O L D"
    if request.method == "POST":
        form = TradeForm(request.POST)
        data = yf.download(tickers='ETH-USD', period = '1D', interval = '1D')
        if form.is_valid():
            form = form.save(commit=False)
            form.price = float(data.reset_index()['Close'][0])
            if form.option == "buy" and form.buy_amount != 0:
                form.sell_amount = None
                get_eth = (form.buy_amount / form.price)+account.eth
                get_balance = account.balance - form.buy_amount
                account = demoAccount.objects.filter(user = get_user.id).update(balance = get_balance, eth = get_eth)
            elif form.option == "sell" and form.sell_amount != 0:
                form.buy_amount = None
                sell_eth = account.eth - form.sell_amount
                get_balance = account.balance + (form.sell_amount * form.price)
                account = demoAccount.objects.filter(user = get_user.id).update(balance = get_balance, eth = sell_eth)
            else:
                error = "The value should more than 0"
                form = TradeForm(initial={'account':account, 'coin':"eth"})
                return render(request,'demo-account/trade/trade_eth.html', {'form':form, 'account':account, 'error':error, 'lstm':lstm, 'lrg':lrg, 'macd':macd})
            form.save()
            return redirect("/demoaccount")
        
        return render(request,'demo-account/trade/trade_eth.html', {'form':form, 'account':account, 'lstm':lstm, 'lrg':lrg, 'macd':macd})

    else:
        form = TradeForm(initial={'account':account, 'coin':"eth"})
        return render(request,'demo-account/trade/trade_eth.html', {'form':form, 'account':account, 'lstm':lstm, 'lrg':lrg, 'macd':macd})
@login_required
def tradeBNB(request):
    get_user = request.user
    account = demoAccount.objects.get(user = get_user.id)
    bnb_1d = bnb_1D.objects.all().order_by('-id')[:2]
    if  bnb_1d[0].predict_LSTM != None and bnb_1d[0].predict_LSTM > bnb_1d[1].predict_LSTM:
        lstm = "B U Y"
    else:
        lstm = "S E L L"
    if bnb_1d[0].predict_LRG != None and bnb_1d[0].predict_LRG > bnb_1d[1].predict_LRG:
        lrg = "B U Y"
    else:
        lrg = "S E L L"
    if bnb_1d[0].predict_MACD == 'buy':
        macd = "B U Y"
    elif bnb_1d[0].predict_MACD == 'sell':
        macd = "S E L L"
    else:
        macd = "H O L D"
    if request.method == "POST":
        form = TradeForm(request.POST)
        data = yf.download(tickers='BNB-USD', period = '1D', interval = '1D')
        if form.is_valid():
            form = form.save(commit=False)
            form.price = float(data.reset_index()['Close'][0])
            if form.option == "buy" and form.buy_amount != 0:
                form.sell_amount = None
                get_bnb = (form.buy_amount / form.price)+account.bnb
                get_balance = account.balance - form.buy_amount
                account = demoAccount.objects.filter(user = get_user.id).update(balance = get_balance, bnb = get_bnb)
            elif form.option == "sell" and form.sell_amount != 0:
                form.buy_amount = None
                sell_bnb = account.bnb - form.sell_amount
                get_balance = account.balance + (form.sell_amount * form.price)
                account = demoAccount.objects.filter(user = get_user.id).update(balance = get_balance, bnb = sell_bnb)
            else:
                error = "The value should more than 0"
                form = TradeForm(initial={'account':account, 'coin':"bnb"})
                return render(request,'demo-account/trade/trade_bnb.html', {'form':form, 'account':account, 'error':error, 'lstm':lstm, 'lrg':lrg, 'macd':macd})
            form.save()
            return redirect("/demoaccount")
        
        return render(request,'demo-account/trade/trade_bnb.html', {'form':form, 'account':account, 'lstm':lstm, 'lrg':lrg, 'macd':macd})

    else:
        form = TradeForm(initial={'account':account, 'coin':"bnb"})
        return render(request,'demo-account/trade/trade_bnb.html', {'form':form, 'account':account, 'lstm':lstm, 'lrg':lrg, 'macd':macd})
@login_required
def tradeADA(request):
    get_user = request.user
    account = demoAccount.objects.get(user = get_user.id)
    ada_1d = ada_1D.objects.all().order_by('-id')[:2]
    if ada_1d[0].predict_LSTM != None and ada_1d[0].predict_LSTM > ada_1d[1].predict_LSTM:
        lstm = "B U Y"
    else:
        lstm = "S E L L"
    if ada_1d[0].predict_LRG != None and ada_1d[0].predict_LRG > ada_1d[1].predict_LRG:
        lrg = "B U Y"
    else:
        lrg = "S E L L"
    if ada_1d[0].predict_MACD == 'buy':
        macd = "B U Y"
    elif ada_1d[0].predict_MACD == 'sell':
        macd = "S E L L"
    else:
        macd = "H O L D"
    if request.method == "POST":
        form = TradeForm(request.POST)
        data = yf.download(tickers='ADA-USD', period = '1D', interval = '1D')
        if form.is_valid():
            form = form.save(commit=False)
            form.price = float(data.reset_index()['Close'][0])
            if form.option == "buy" and form.buy_amount != 0:
                form.sell_amount = None
                get_ada = (form.buy_amount / form.price)+account.ada
                get_balance = account.balance - form.buy_amount
                account = demoAccount.objects.filter(user = get_user.id).update(balance = get_balance, ada = get_ada)
            elif form.option == "sell" and form.sell_amount != 0:
                form.buy_amount = None
                sell_ada = account.ada - form.sell_amount
                get_balance = account.balance + (form.sell_amount * form.price)
                account = demoAccount.objects.filter(user = get_user.id).update(balance = get_balance, ada = sell_ada)
            else:
                error = "The value should more than 0"
                form = TradeForm(initial={'account':account, 'coin':"ada"})
                return render(request,'demo-account/trade/trade_ada.html', {'form':form, 'account':account, 'error':error, 'lstm':lstm, 'lrg':lrg, 'macd':macd})
            form.save()
            return redirect("/demoaccount")
        
        return render(request,'demo-account/trade/trade_ada.html', {'form':form, 'account':account, 'lstm':lstm, 'lrg':lrg, 'macd':macd})

    else:
        form = TradeForm(initial={'account':account, 'coin':"ada"})
        return render(request,'demo-account/trade/trade_ada.html', {'form':form, 'account':account, 'lstm':lstm, 'lrg':lrg, 'macd':macd})


@login_required
def tradeLTC(request):
    get_user = request.user
    account = demoAccount.objects.get(user = get_user.id)
    ltc_1d = ltc_1D.objects.all().order_by('-id')[:2]
    if ltc_1d[0].predict_LSTM != None and ltc_1d[0].predict_LSTM > ltc_1d[1].predict_LSTM:
        lstm = "B U Y"
    else:
        lstm = "S E L L"
    if ltc_1d[0].predict_LRG != None and ltc_1d[0].predict_LRG > ltc_1d[1].predict_LRG:
        lrg = "B U Y"
    else:
        lrg = "S E L L"
    if ltc_1d[0].predict_MACD == 'buy':
        macd = "B U Y"
    elif ltc_1d[0].predict_MACD == 'sell':
        macd = "S E L L"
    else:
        macd = "H O L D"
    if request.method == "POST":
        form = TradeForm(request.POST)
        data = yf.download(tickers='LTC-USD', period = '1D', interval = '1D')
        if form.is_valid():
            form = form.save(commit=False)
            form.price = float(data.reset_index()['Close'][0])
            if form.option == "buy" and form.buy_amount != 0:
                form.sell_amount = None
                get_ltc = (form.buy_amount / form.price)+account.ltc
                get_balance = account.balance - form.buy_amount
                account = demoAccount.objects.filter(user = get_user.id).update(balance = get_balance, ltc = get_ltc)
            elif form.option == "sell" and form.sell_amount != 0:
                form.buy_amount = None
                sell_ltc = account.ltc - form.sell_amount
                get_balance = account.balance + (form.sell_amount * form.price)
                account = demoAccount.objects.filter(user = get_user.id).update(balance = get_balance, ltc = sell_ltc)
            else:
                error = "The value should more than 0"
                form = TradeForm(initial={'account':account, 'coin':"ltc"})
                return render(request,'demo-account/trade/trade_ltc.html', {'form':form, 'account':account, 'error':error, 'lstm':lstm, 'lrg':lrg, 'macd':macd})
            form.save()
            return redirect("/demoaccount")
        
        return render(request,'demo-account/trade/trade_ltc.html', {'form':form, 'account':account, 'lstm':lstm, 'lrg':lrg, 'macd':macd})

    else:
        form = TradeForm(initial={'account':account, 'coin':"ltc"})
        return render(request,'demo-account/trade/trade_ltc.html', {'form':form, 'account':account, 'lstm':lstm, 'lrg':lrg, 'macd':macd})
