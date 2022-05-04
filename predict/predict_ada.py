import math
import numpy as np 
import yfinance as yf

from sklearn.preprocessing import MinMaxScaler 
from keras.models import Sequential 
from keras.layers import Dense, LSTM
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from .models import ada_30M, ada_1D, ada_1H



def ada_1D_download():
    df = yf.download(tickers='ADA-USD', period = '365d', interval = '1D')
    last_data = df[len(df)-1:]
    update_last_data = ada_1D.objects.filter(Date=last_data.reset_index()['Date'][0])
    update_last_data.update( Open=last_data['Open'].values, High=last_data['High'].values, Low=last_data['Low'].values, Close=last_data['Close'].values, Volume=last_data['Volume'].values)
    #-- save value to db ------------------------------------------------------------------------------------------------------
    for i in range(len(df)-1):
        new_df = df[i+1:i+2]
        Date = (new_df.reset_index()['Date'][0])
        if not ada_1D.objects.filter(Date=Date):
            ada_1D.objects.create(Date = Date, Open=new_df['Open'].values, High=new_df['High'].values, Low=new_df['Low'].values, Close=new_df['Close'].values, Volume=new_df['Volume'].values)
    #-- ------------------------------------------------------------------------------------------------------


def ada_30M_download():
    df = yf.download(tickers='ada-USD', period = '21600M', interval = '30M')
    last_data = df[len(df)-1:]
    update_last_data = ada_30M.objects.filter(Datetime=last_data.reset_index()['Datetime'][0])
    update_last_data.update( Open=last_data['Open'].values, High=last_data['High'].values, Low=last_data['Low'].values, Close=last_data['Close'].values, Volume=last_data['Volume'].values)
    #-- save value to db ------------------------------------------------------------------------------------------------------
    for i in range(len(df)-1):
        new_df = df[i+1:i+2]
        Datetime = (new_df.reset_index()['Datetime'][0])
        if not ada_30M.objects.filter(Datetime=Datetime):
            ada_30M.objects.create(Datetime = Datetime, Open=new_df['Open'].values, High=new_df['High'].values, Low=new_df['Low'].values, Close=new_df['Close'].values, Volume=new_df['Volume'].values)
    #-- ------------------------------------------------------------------------------------------------------

def ada_1H_download():
    df = yf.download(tickers='ada-USD', period = '21900M', interval = '60M')
    last_data = df[len(df)-2:len(df)-1]
    update_last_data = ada_1H.objects.filter(Datetime=last_data.reset_index()['Datetime'][0])
    update_last_data.update( Open=last_data['Open'].values, High=last_data['High'].values, Low=last_data['Low'].values, Close=last_data['Close'].values, Volume=last_data['Volume'].values)
    #-- save value to db ------------------------------------------------------------------------------------------------------
    for i in range(len(df)-2):
        new_df = df[i+1:i+2]
        Datetime = (new_df.reset_index()['Datetime'][0])
        if not ada_1H.objects.filter(Datetime=Datetime):
            ada_1H.objects.create(Datetime = Datetime, Open=new_df['Open'].values, High=new_df['High'].values, Low=new_df['Low'].values, Close=new_df['Close'].values, Volume=new_df['Volume'].values)       
    #-- ------------------------------------------------------------------------------------------------------


def ada_30M_LSTM_predict():
    df = yf.download(tickers='ADA-USD', period = '21600M', interval = '30M')

    data = df.filter(['Close'])
    #dataframs to a numpy array
    dataset = data.values
    #train 
    training_data_len = math.ceil( len(dataset) * .90 ) 
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(dataset)
    #Create training data set
    train_data = scaled_data[0:training_data_len , :]
    #Split data
    x_train = []
    y_train = []
    for i in range(60, len(train_data)):
        x_train.append(train_data[i-60:i, 0])
        y_train.append(train_data[i,0])
    x_train, y_train = np.array(x_train),np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape = (x_train.shape[1],1)))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))
    model.compile(optimizer = 'adam', loss='mean_squared_error')
    model.fit(x_train, y_train, epochs=10, batch_size=1, verbose=2)

    #Create the testing data set
    test_data = scaled_data[training_data_len - 60: , :]
    #Create the data set x_test and y_test
    x_test = []
    y_test = dataset[training_data_len:, :]
    for i in range(60, len(test_data)):
        x_test.append(test_data[i-60:i, 0])
    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)
    valid = data[len(data)-len(predictions):]
    valid['Predictions'] = predictions

    error_value = 0
    for i in range(len(valid)-1):
        new_df = valid[i+1:i+2]
        error_value += new_df.reset_index()['Predictions'].values-new_df.reset_index()['Close'].values
    error_value = error_value/(len(valid)-1)
    #-- save perdict value to db ------------------------------------------------------------------------------------------------------
    for i in range(len(valid)-1):
        new_df = valid[i+1:i+2]
        find_ada_30M = ada_30M.objects.filter(Datetime = new_df.reset_index()['Datetime'][0], predict_LSTM__isnull=True)
        find_ada_30M.update(predict_LSTM = float(new_df.reset_index()['Predictions'].values-error_value))
    #----------------------------------------------------------------------------

def ada_1H_LSTM_predict():
    df = yf.download(tickers='ADA-USD', period = '33200M', interval = '60M')
    df = df[:-1]
    data = df.filter(['Close'])
    #dataframs to a numpy array
    dataset = data.values
    #train 
    training_data_len = math.ceil( len(dataset) * .90 ) 
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(dataset)
    #Create training data set
    train_data = scaled_data[0:training_data_len , :]
    #Split data
    x_train = []
    y_train = []
    for i in range(60, len(train_data)):
        x_train.append(train_data[i-60:i, 0])
        y_train.append(train_data[i,0])
    x_train, y_train = np.array(x_train),np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape = (x_train.shape[1],1)))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))
    model.compile(optimizer = 'adam', loss='mean_squared_error')

    model.fit(x_train, y_train, epochs=10, batch_size=1, verbose=2)

    #Create the testing data set
    test_data = scaled_data[training_data_len - 60: , :]
    #Create the data set x_test and y_test
    x_test = []
    y_test = dataset[training_data_len:, :]
    for i in range(60, len(test_data)):
        x_test.append(test_data[i-60:i, 0])
    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)
    valid = data[len(data)-len(predictions):]
    valid['Predictions'] = predictions

    error_value = 0
    for i in range(len(valid)-1):
        new_df = valid[i+1:i+2]
        error_value += new_df.reset_index()['Predictions'].values-new_df.reset_index()['Close'].values
    error_value = error_value/(len(valid)-1)
    #-- save perdict value to db ------------------------------------------------------------------------------------------------------
    for i in range(len(valid)-1):
        new_df = valid[i+1:i+2]
        find_ada_1H = ada_1H.objects.filter(Datetime = new_df.reset_index()['Datetime'][0], predict_LSTM__isnull=True)
        find_ada_1H.update(predict_LSTM = float(new_df.reset_index()['Predictions'].values-error_value))
    #----------------------------------------------------------------------------


def ada_1D_LSTM_predict():
    df = yf.download(tickers='ADA-USD', period = '365d', interval = '1D')

    data = df.filter(['Close'])
    #dataframs to a numpy array
    dataset = data.values
    #train 
    training_data_len = math.ceil( len(dataset) * .90 ) 
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(dataset)
    #Create training data set
    train_data = scaled_data[0:training_data_len , :]
    #Split data
    x_train = []
    y_train = []
    for i in range(60, len(train_data)):
        x_train.append(train_data[i-60:i, 0])
        y_train.append(train_data[i,0])
    x_train, y_train = np.array(x_train),np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape = (x_train.shape[1],1)))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))
    model.compile(optimizer = 'adam', loss='mean_squared_error')
    model.fit(x_train, y_train, epochs=10, batch_size=1, verbose=2)
    #Create the testing data set
    test_data = scaled_data[training_data_len - 60: , :]
    #Create the data set x_test and y_test
    x_test = []
    y_test = dataset[training_data_len:, :]
    for i in range(60, len(test_data)):
        x_test.append(test_data[i-60:i, 0])
    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)
    valid = data[len(data)-len(predictions):]
    valid['Predictions'] = predictions

    error_value = 0
    for i in range(len(valid)-1):
        new_df = valid[i+1:i+2]
        error_value += new_df.reset_index()['Predictions'].values-new_df.reset_index()['Close'].values
    error_value = error_value/(len(valid)-1)
    #-- save perdict value to db ------------------------------------------------------------------------------------------------------
    for i in range(len(valid)-1):
        new_df = valid[i+1:i+2]
        find_ada_1D = ada_1D.objects.filter(Date = new_df.reset_index()['Date'][0], predict_LSTM__isnull=True)
        find_ada_1D.update(predict_LSTM = float(new_df.reset_index()['Predictions'].values-error_value))
    #----------------------------------------------------------------------------


def ada_30M_LRG_predict():
    data = yf.download(tickers='ADA-USD', period = '21600M', interval = '30M')
    projection = 16
    data["Prediction"] = data[["Close"]].shift(-projection)

    x = np.array(data[['Close']])
    x = x[:-projection]

    y = data['Prediction'].values
    y = y[:-projection]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = .15)
    LRG = LinearRegression()
    LRG.fit(x_train, y_train)

    LRG_score = LRG.score(x_test, y_test)
    print('Lineaer regression confidence:', LRG_score)
    x_projection = np.array(data[["Close"]])[-40:]
    LRG_prediction = LRG.predict(x_projection)

    valid = data[len(data)-40:]
    valid['Predictions'] = LRG_prediction

    error_value = 0
    for i in range(len(valid)-1):
        new_df = valid[i+1:i+2]
        error_value += new_df.reset_index()['Predictions'].values-new_df.reset_index()['Close'].values
    error_value = error_value/(len(valid)-1)
    #-- save perdict value to db ------------------------------------------------------------------------------------------------------
    for i in range(len(valid)-1):
        new_df = valid[i+1:i+2]
        find_ada_30M = ada_30M.objects.filter(Datetime = new_df.reset_index()['Datetime'][0], predict_LRG__isnull=True)
        find_ada_30M.update(predict_LRG = float(new_df.reset_index()['Predictions'].values-error_value))
    #----------------------------------------------------------------------------

def ada_1H_LRG_predict():
    data = yf.download(tickers='ADA-USD', period = '33200M', interval = '60M')
    data = data[:-1]
    projection = 16
    data["Prediction"] = data[["Close"]].shift(-projection)

    x = np.array(data[['Close']])
    x = x[:-projection]

    y = data['Prediction'].values
    y = y[:-projection]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = .15)
    LRG = LinearRegression()
    LRG.fit(x_train, y_train)

    LRG_score = LRG.score(x_test, y_test)
    print('Lineaer regression confidence:', LRG_score)
    x_projection = np.array(data[["Close"]])[-40:]
    LRG_prediction = LRG.predict(x_projection)

    valid = data[len(data)-40:]
    valid['Predictions'] = LRG_prediction

    error_value = 0
    for i in range(len(valid)-1):
        new_df = valid[i+1:i+2]
        error_value += new_df.reset_index()['Predictions'].values-new_df.reset_index()['Close'].values
    error_value = error_value/(len(valid)-1)
    #-- save perdict value to db ------------------------------------------------------------------------------------------------------
    for i in range(len(valid)-1):
        new_df = valid[i+1:i+2]
        find_ada_1H = ada_1H.objects.filter(Datetime = new_df.reset_index()['Datetime'][0], predict_LRG__isnull=True)
        find_ada_1H.update(predict_LRG = float(new_df.reset_index()['Predictions'].values-error_value))
    #----------------------------------------------------------------------------

def ada_1D_LRG_predict():
    data = yf.download(tickers='ada-USD', period = '365d', interval = '1D')
    projection = 14
    data["Prediction"] = data[["Close"]].shift(-projection)

    x = np.array(data[['Close']])
    x = x[:-projection]

    y = data['Prediction'].values
    y = y[:-projection]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = .15)
    LRG = LinearRegression()
    LRG.fit(x_train, y_train)

    LRG_score = LRG.score(x_test, y_test)
    print('Lineaer regression confidence:', LRG_score)
    x_projection = np.array(data[["Close"]])[-40:]
    LRG_prediction = LRG.predict(x_projection)

    valid = data[len(data)-40:]
    valid['Predictions'] = LRG_prediction

    error_value = 0
    for i in range(len(valid)-1):
        new_df = valid[i+1:i+2]
        error_value += new_df.reset_index()['Predictions'].values-new_df.reset_index()['Close'].values
    error_value = error_value/(len(valid)-1)
    #-- save perdict value to db ------------------------------------------------------------------------------------------------------
    for i in range(len(valid)-1):
        new_df = valid[i+1:i+2]
        find_ada_1D = ada_1D.objects.filter(Date = new_df.reset_index()['Date'][0], predict_LRG__isnull=True)
        find_ada_1D.update(predict_LRG = float(new_df.reset_index()['Predictions'].values-error_value))
    #----------------------------------------------------------------------------

def ada_30M_MACD_predict():
    data = yf.download(tickers='ADA-USD', period = '28800M', interval = '30M')
    short_ma13 = data['Close'].rolling(13).mean()
    mid_ma21 = data['Close'].rolling(21).mean()
    long_ma55 = data['Close'].rolling(55).mean()
    data['shortma13'] = short_ma13
    data['midma21'] = mid_ma21
    data['longma55'] = long_ma55
    data = data.dropna()
    for i in range(len(data)):
        new_data = data[i:i+1]
        if (new_data.iloc[0]['shortma13'] > new_data.iloc[0]['midma21'] > new_data.iloc[0]['longma55']):
            predictMACD = "buy"
        elif (new_data.iloc[0]['longma55'] > new_data.iloc[0]['midma21'] > new_data.iloc[0]['shortma13']):
            predictMACD = "sell"
        else:
            predictMACD = "hold"
        Datetime = (new_data.reset_index()['Datetime'][0])
        ada_30M.objects.filter(Datetime=Datetime,predict_MACD__isnull=True).update(predict_MACD=predictMACD)

def ada_1H_MACD_predict():
    data = yf.download(tickers='ADA-USD', period = '72000M', interval = '60M')
    data = data[:-1]
    short_ma13 = data['Close'].rolling(13).mean()
    mid_ma21 = data['Close'].rolling(21).mean()
    long_ma55 = data['Close'].rolling(55).mean()
    data['shortma13'] = short_ma13
    data['midma21'] = mid_ma21
    data['longma55'] = long_ma55
    data = data.dropna()
    for i in range(len(data)):
        new_data = data[i:i+1]
        if (new_data.iloc[0]['shortma13'] > new_data.iloc[0]['midma21'] > new_data.iloc[0]['longma55']):
            predictMACD = "buy"
        elif (new_data.iloc[0]['longma55'] > new_data.iloc[0]['midma21'] > new_data.iloc[0]['shortma13']):
            predictMACD = "sell"
        else:
            predictMACD = "hold"
        Datetime = (new_data.reset_index()['Datetime'][0])
        ada_1H.objects.filter(Datetime=Datetime,predict_MACD__isnull=True).update(predict_MACD=predictMACD)

def ada_1D_MACD_predict():
    data = yf.download(tickers='ADA-USD', period = '960D', interval = '1D')
    short_ma13 = data['Close'].rolling(13).mean()
    mid_ma21 = data['Close'].rolling(21).mean()
    long_ma55 = data['Close'].rolling(55).mean()
    data['shortma13'] = short_ma13
    data['midma21'] = mid_ma21
    data['longma55'] = long_ma55
    data = data.dropna()
    for i in range(len(data)):
        new_data = data[i:i+1]
        if (new_data.iloc[0]['shortma13'] > new_data.iloc[0]['midma21'] > new_data.iloc[0]['longma55']):
            predictMACD = "buy"
        elif (new_data.iloc[0]['longma55'] > new_data.iloc[0]['midma21'] > new_data.iloc[0]['shortma13']):
            predictMACD = "sell"
        else:
            predictMACD = "hold"
        Date = (new_data.reset_index()['Date'][0])
        ada_1D.objects.filter(Date=Date,predict_MACD__isnull=True).update(predict_MACD=predictMACD)