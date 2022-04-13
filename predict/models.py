from django.db import models

class btc_30M(models.Model):
    Datetime = models.DateTimeField(unique=True)
    Open = models.FloatField(null=True, blank=True)
    High = models.FloatField(null=True, blank=True)
    Low = models.FloatField(null=True, blank=True)
    Close = models.FloatField(null=True, blank=True)
    Volume = models.FloatField(null=True, blank=True)
    predict_LSTM = models.FloatField(null=True, blank=True)
    predict_LRG = models.FloatField(null=True, blank=True)
    predict_MACD = models.CharField(null=True, blank=True, max_length=4)

    def __str__(self):
        return str(self.Datetime)

class btc_1H(models.Model):
    Datetime = models.DateTimeField(unique=True)
    Open = models.FloatField(null=True, blank=True)
    High = models.FloatField(null=True, blank=True)
    Low = models.FloatField(null=True, blank=True)
    Close = models.FloatField(null=True, blank=True)
    Volume = models.FloatField(null=True, blank=True)
    predict_LSTM = models.FloatField(null=True, blank=True)
    predict_LRG = models.FloatField(null=True, blank=True)
    predict_MACD = models.CharField(null=True, blank=True, max_length=4)

    def __str__(self):
        return str(self.Datetime)

class btc_1D(models.Model):
    Date = models.DateField(unique=True, null=True)
    Open = models.FloatField(null=True, blank=True)
    High = models.FloatField(null=True, blank=True)
    Low = models.FloatField(null=True, blank=True)
    Close = models.FloatField(null=True, blank=True)
    Volume = models.FloatField(null=True, blank=True)
    predict_LSTM = models.FloatField(null=True, blank=True)
    predict_LRG = models.FloatField(null=True, blank=True)
    predict_MACD = models.CharField(null=True, blank=True, max_length=4)

    def __str__(self):
        return str(self.Date)

class eth_30M(models.Model):
    Datetime = models.DateTimeField(unique=True)
    Open = models.FloatField(null=True, blank=True)
    High = models.FloatField(null=True, blank=True)
    Low = models.FloatField(null=True, blank=True)
    Close = models.FloatField(null=True, blank=True)
    Volume = models.FloatField(null=True, blank=True)
    predict_LSTM = models.FloatField(null=True, blank=True)
    predict_LRG = models.FloatField(null=True, blank=True)
    predict_MACD = models.CharField(null=True, blank=True, max_length=4)

    def __str__(self):
        return str(self.Datetime)

class eth_1H(models.Model):
    Datetime = models.DateTimeField(unique=True)
    Open = models.FloatField(null=True, blank=True)
    High = models.FloatField(null=True, blank=True)
    Low = models.FloatField(null=True, blank=True)
    Close = models.FloatField(null=True, blank=True)
    Volume = models.FloatField(null=True, blank=True)
    predict_LSTM = models.FloatField(null=True, blank=True)
    predict_LRG = models.FloatField(null=True, blank=True)
    predict_MACD = models.CharField(null=True, blank=True, max_length=4)

    def __str__(self):
        return str(self.Datetime)

class eth_1D(models.Model):
    Date = models.DateField(unique=True, null=True)
    Open = models.FloatField(null=True, blank=True)
    High = models.FloatField(null=True, blank=True)
    Low = models.FloatField(null=True, blank=True)
    Close = models.FloatField(null=True, blank=True)
    Volume = models.FloatField(null=True, blank=True)
    predict_LSTM = models.FloatField(null=True, blank=True)
    predict_LRG = models.FloatField(null=True, blank=True)
    predict_MACD = models.CharField(null=True, blank=True, max_length=4)

    def __str__(self):
        return str(self.Date)

class bnb_30M(models.Model):
    Datetime = models.DateTimeField(unique=True)
    Open = models.FloatField(null=True, blank=True)
    High = models.FloatField(null=True, blank=True)
    Low = models.FloatField(null=True, blank=True)
    Close = models.FloatField(null=True, blank=True)
    Volume = models.FloatField(null=True, blank=True)
    predict_LSTM = models.FloatField(null=True, blank=True)
    predict_LRG = models.FloatField(null=True, blank=True)
    predict_MACD = models.CharField(null=True, blank=True, max_length=4)

    def __str__(self):
        return str(self.Datetime)

class bnb_1H(models.Model):
    Datetime = models.DateTimeField(unique=True)
    Open = models.FloatField(null=True, blank=True)
    High = models.FloatField(null=True, blank=True)
    Low = models.FloatField(null=True, blank=True)
    Close = models.FloatField(null=True, blank=True)
    Volume = models.FloatField(null=True, blank=True)
    predict_LSTM = models.FloatField(null=True, blank=True)
    predict_LRG = models.FloatField(null=True, blank=True)
    predict_MACD = models.CharField(null=True, blank=True, max_length=4)

    def __str__(self):
        return str(self.Datetime)

class bnb_1D(models.Model):
    Date = models.DateField(unique=True, null=True)
    Open = models.FloatField(null=True, blank=True)
    High = models.FloatField(null=True, blank=True)
    Low = models.FloatField(null=True, blank=True)
    Close = models.FloatField(null=True, blank=True)
    Volume = models.FloatField(null=True, blank=True)
    predict_LSTM = models.FloatField(null=True, blank=True)
    predict_LRG = models.FloatField(null=True, blank=True)
    predict_MACD = models.CharField(null=True, blank=True, max_length=4)

    def __str__(self):
        return str(self.Date)


class ada_30M(models.Model):
    Datetime = models.DateTimeField(unique=True)
    Open = models.FloatField(null=True, blank=True)
    High = models.FloatField(null=True, blank=True)
    Low = models.FloatField(null=True, blank=True)
    Close = models.FloatField(null=True, blank=True)
    Volume = models.FloatField(null=True, blank=True)
    predict_LSTM = models.FloatField(null=True, blank=True)
    predict_LRG = models.FloatField(null=True, blank=True)
    predict_MACD = models.CharField(null=True, blank=True, max_length=4)

    def __str__(self):
        return str(self.Datetime)

class ada_1H(models.Model):
    Datetime = models.DateTimeField(unique=True)
    Open = models.FloatField(null=True, blank=True)
    High = models.FloatField(null=True, blank=True)
    Low = models.FloatField(null=True, blank=True)
    Close = models.FloatField(null=True, blank=True)
    Volume = models.FloatField(null=True, blank=True)
    predict_LSTM = models.FloatField(null=True, blank=True)
    predict_LRG = models.FloatField(null=True, blank=True)
    predict_MACD = models.CharField(null=True, blank=True, max_length=4)

    def __str__(self):
        return str(self.Datetime)

class ada_1D(models.Model):
    Date = models.DateField(unique=True, null=True)
    Open = models.FloatField(null=True, blank=True)
    High = models.FloatField(null=True, blank=True)
    Low = models.FloatField(null=True, blank=True)
    Close = models.FloatField(null=True, blank=True)
    Volume = models.FloatField(null=True, blank=True)
    predict_LSTM = models.FloatField(null=True, blank=True)
    predict_LRG = models.FloatField(null=True, blank=True)
    predict_MACD = models.CharField(null=True, blank=True, max_length=4)

    def __str__(self):
        return str(self.Date)


class ltc_30M(models.Model):
    Datetime = models.DateTimeField(unique=True)
    Open = models.FloatField(null=True, blank=True)
    High = models.FloatField(null=True, blank=True)
    Low = models.FloatField(null=True, blank=True)
    Close = models.FloatField(null=True, blank=True)
    Volume = models.FloatField(null=True, blank=True)
    predict_LSTM = models.FloatField(null=True, blank=True)
    predict_LRG = models.FloatField(null=True, blank=True)
    predict_MACD = models.CharField(null=True, blank=True, max_length=4)

    def __str__(self):
        return str(self.Datetime)

class ltc_1H(models.Model):
    Datetime = models.DateTimeField(unique=True)
    Open = models.FloatField(null=True, blank=True)
    High = models.FloatField(null=True, blank=True)
    Low = models.FloatField(null=True, blank=True)
    Close = models.FloatField(null=True, blank=True)
    Volume = models.FloatField(null=True, blank=True)
    predict_LSTM = models.FloatField(null=True, blank=True)
    predict_LRG = models.FloatField(null=True, blank=True)
    predict_MACD = models.CharField(null=True, blank=True, max_length=4)

    def __str__(self):
        return str(self.Datetime)

class ltc_1D(models.Model):
    Date = models.DateField(unique=True, null=True)
    Open = models.FloatField(null=True, blank=True)
    High = models.FloatField(null=True, blank=True)
    Low = models.FloatField(null=True, blank=True)
    Close = models.FloatField(null=True, blank=True)
    Volume = models.FloatField(null=True, blank=True)
    predict_LSTM = models.FloatField(null=True, blank=True)
    predict_LRG = models.FloatField(null=True, blank=True)
    predict_MACD = models.CharField(null=True, blank=True, max_length=4)

    def __str__(self):
        return str(self.Date)


