import math
import numpy as np 
import yfinance as yf
import pandas as pd

from sklearn.preprocessing import MinMaxScaler 
from keras.models import Sequential 
from keras.layers import Dense, LSTM
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from .models import btc_30M, btc_1D, btc_1H



def btc_1D_download():
    df = yf.download(tickers='BTC-USD', period = '365d', interval = '1D')
    last_data = df[len(df)-1:]
    update_last_data = btc_1D.objects.filter(Date=last_data.reset_index()['Date'][0])
    update_last_data.update( Open=last_data['Open'].values, High=last_data['High'].values, Low=last_data['Low'].values, Close=last_data['Close'].values, Volume=last_data['Volume'].values)
    #-- save value to db ------------------------------------------------------------------------------------------------------
    for i in range(len(df)-1):
        new_df = df[i+1:i+2]
        Date = (new_df.reset_index()['Date'][0])
        if not btc_1D.objects.filter(Date=Date):
            btc_1D.objects.create(Date = Date, Open=new_df['Open'].values, High=new_df['High'].values, Low=new_df['Low'].values, Close=new_df['Close'].values, Volume=new_df['Volume'].values)
    #-- ------------------------------------------------------------------------------------------------------


def btc_30M_download():
    df = yf.download(tickers='BTC-USD', period = '21600M', interval = '30M')
    print(df)
    last_data = df[len(df)-1:]
    update_last_data = btc_30M.objects.filter(Datetime=last_data.reset_index()['Datetime'][0])
    update_last_data.update( Open=last_data['Open'].values, High=last_data['High'].values, Low=last_data['Low'].values, Close=last_data['Close'].values, Volume=last_data['Volume'].values)
    #-- save value to db ------------------------------------------------------------------------------------------------------
    for i in range(len(df)-1):
        new_df = df[i+1:i+2]
        Datetime = (new_df.reset_index()['Datetime'][0])
        if not btc_30M.objects.filter(Datetime=Datetime):
            btc_30M.objects.create(Datetime = Datetime, Open=new_df['Open'].values, High=new_df['High'].values, Low=new_df['Low'].values, Close=new_df['Close'].values, Volume=new_df['Volume'].values)
    #-- ------------------------------------------------------------------------------------------------------

def btc_1H_download():
    df = yf.download(tickers='BTC-USD', period = '21900M', interval = '60M')
    last_data = df[len(df)-2:len(df)-1]
    print(last_data)
    update_last_data = btc_1H.objects.filter(Datetime=last_data.reset_index()['Datetime'][0])
    print(update_last_data)
    update_last_data.update( Open=last_data['Open'].values, High=last_data['High'].values, Low=last_data['Low'].values, Close=last_data['Close'].values, Volume=last_data['Volume'].values)
    #-- save value to db ------------------------------------------------------------------------------------------------------
    for i in range(len(df)-2):
        new_df = df[i+1:i+2]
        Datetime = (new_df.reset_index()['Datetime'][0])
        if not btc_1H.objects.filter(Datetime=Datetime):
            btc_1H.objects.create(Datetime = Datetime, Open=new_df['Open'].values, High=new_df['High'].values, Low=new_df['Low'].values, Close=new_df['Close'].values, Volume=new_df['Volume'].values)
            
    #-- ------------------------------------------------------------------------------------------------------
    print(len(df)-1)


def btc_30M_LSTM_predict():
    df = yf.download(tickers='BTC-USD', period = '21600M', interval = '30M')

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
        find_btc_30M = btc_30M.objects.filter(Datetime = new_df.reset_index()['Datetime'][0], predict_LSTM = None)
        find_btc_30M.update(predict_LSTM = float(new_df.reset_index()['Predictions'].values-error_value))
    #----------------------------------------------------------------------------

def btc_1H_LSTM_predict():
    df = yf.download(tickers='BTC-USD', period = '33200M', interval = '60M')
    print(df)
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
        find_btc_1H = btc_1H.objects.filter(Datetime = new_df.reset_index()['Datetime'][0], predict_LSTM = None)
        find_btc_1H.update(predict_LSTM = float(new_df.reset_index()['Predictions'].values-error_value))
    #----------------------------------------------------------------------------


def btc_1D_LSTM_predict():
    df = yf.download(tickers='BTC-USD', period = '365d', interval = '1D')

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
        find_btc_1D = btc_1D.objects.filter(Date = new_df.reset_index()['Date'][0], predict_LSTM = None)
        find_btc_1D.update(predict_LSTM = float(new_df.reset_index()['Predictions'].values-error_value))
    #----------------------------------------------------------------------------


def btc_30M_LRG_predict():
    data = yf.download(tickers='BTC-USD', period = '21600M', interval = '30M')
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
        find_btc_30M = btc_30M.objects.filter(Datetime = new_df.reset_index()['Datetime'][0], predict_LRG = None)
        find_btc_30M.update(predict_LRG = float(new_df.reset_index()['Predictions'].values-error_value))
    #----------------------------------------------------------------------------

def btc_1H_LRG_predict():
    data = yf.download(tickers='BTC-USD', period = '33200M', interval = '60M')
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
        find_btc_1H = btc_1H.objects.filter(Datetime = new_df.reset_index()['Datetime'][0], predict_LRG = None)
        find_btc_1H.update(predict_LRG = float(new_df.reset_index()['Predictions'].values-error_value))
    #----------------------------------------------------------------------------

def btc_1D_LRG_predict():
    data = yf.download(tickers='BTC-USD', period = '365d', interval = '1D')
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
        find_btc_1D = btc_1D.objects.filter(Date = new_df.reset_index()['Date'][0], predict_LRG = None)
        find_btc_1D.update(predict_LRG = float(new_df.reset_index()['Predictions'].values-error_value))
    #----------------------------------------------------------------------------




































































def btc_31230M_LSTM_predict():
    df = yf.download(tickers='BTC-USD', period = '37740M', interval = '30M')
    #creating dataframe
    data = df.sort_index(ascending=True, axis=0)
    new_data = pd.DataFrame(index=range(0,len(df)),columns=['Datetime', 'Close'])
    for i in range(0,len(data)):
        new_data['Datetime'][i] = data.reset_index()['Datetime'][i]
        new_data['Close'][i] = data['Close'][i]
    #setting index
    new_data.index = new_data.Datetime
    new_data.drop('Datetime', axis=1, inplace=True)
    new_data
    #creating and split data to train and valid
    dataset = new_data.values

    train = dataset[0:1100,:]
    valid = dataset[1100:,:]
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)

    x_train, y_train = [], []
    for i in range(60,len(train)):
        x_train.append(scaled_data[i-60:i,0])
        y_train.append(scaled_data[i,0])
    x_train, y_train = np.array(x_train), np.array(y_train)

    x_train.shape

    x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))
    x_train.shape
    #create and fit the LSTM network
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1],1)))
    model.add(LSTM(units=50))
    model.add(Dense(1))

    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(x_train, y_train, epochs=10, batch_size=1, verbose=2)

    #predicting 339 values, using past 60 from the train data
    inputs = new_data[len(new_data) - len(valid) - 600:].values
    inputs = inputs.reshape(-1,1)
    inputs  = scaler.transform(inputs)

    X_test = []
    for i in range(600,inputs.shape[0]):
        X_test.append(inputs[i-600:i,0])
    X_test = np.array(X_test)

    X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))
    predictions = model.predict(X_test)
    predictions = scaler.inverse_transform(predictions)
    predict_valid = data[len(data)-len(predictions):]
    predict_valid['Predictions'] = predictions
    print(predict_valid)

    #-- save perdict value to db ------------------------------------------------------------------------------------------------------
    for i in range(len(predict_valid)-1):
        new_df = predict_valid[i+1:i+2]
        find_btc_30M = btc_30M.objects.filter(Datetime = new_df.reset_index()['Datetime'][0], predict_LSTM = None)
        find_btc_30M.update(predict_LSTM = float(new_df.reset_index()['Predictions'].values))
    #----------------------------------------------------------------------------

    rmspe = (np.sqrt(np.mean(np.square((valid - predictions) / valid)))) * 100
    print(f"RMSPE_of_BTC_TF_30M = {rmspe}")

    

def btc_1231D_LSTM_predict():
    df = yf.download(tickers='BTC-USD', period = '1258D', interval = '1D')
    #creating dataframe
    data = df.sort_index(ascending=True, axis=0)
    new_data = pd.DataFrame(index=range(0,len(df)),columns=['Date', 'Close'])
    for i in range(0,len(data)):
        new_data['Date'][i] = data.reset_index()['Date'][i]
        new_data['Close'][i] = data['Close'][i]
    #setting index
    new_data.index = new_data.Date
    new_data.drop('Date', axis=1, inplace=True)
    new_data
    #creating and split data to train and valid
    dataset = new_data.values

    train = dataset[0:919,:]
    valid = dataset[919:,:]
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)

    x_train, y_train = [], []
    for i in range(60,len(train)):
        x_train.append(scaled_data[i-60:i,0])
        y_train.append(scaled_data[i,0])
    x_train, y_train = np.array(x_train), np.array(y_train)

    x_train.shape

    x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))
    x_train.shape
    #create and fit the LSTM network
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1],1)))
    model.add(LSTM(units=50))
    model.add(Dense(1))

    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(x_train, y_train, epochs=10, batch_size=1, verbose=2)

    #predicting 339 values, using past 60 from the train data
    inputs = new_data[len(new_data) - len(valid) - 60:].values
    inputs = inputs.reshape(-1,1)
    inputs  = scaler.transform(inputs)

    X_test = []
    for i in range(60,inputs.shape[0]):
        X_test.append(inputs[i-60:i,0])
    X_test = np.array(X_test)

    X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))
    predictions = model.predict(X_test)
    predictions = scaler.inverse_transform(predictions)
    predict_valid = data[len(data)-len(predictions):]
    predict_valid['Predictions'] = predictions
    print(predict_valid)

    #-- save perdict value to db ------------------------------------------------------------------------------------------------------
    for i in range(len(predict_valid)-1):
        new_df = predict_valid[i+1:i+2]
        find_btc_1D = btc_1D.objects.filter(Date = new_df.reset_index()['Date'][0])
        find_btc_1D.update(predict_LSTM = float(new_df.reset_index()['Predictions'].values))
    #----------------------------------------------------------------------------

    rmspe = (np.sqrt(np.mean(np.square((valid - predictions) / valid)))) * 100
    print(f"RMSPE_of_BTC_TF_1D = {rmspe}")