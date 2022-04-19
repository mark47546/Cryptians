from django.db import models
from django.contrib.auth.models import User

class demoAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=100000)
    btc = models.FloatField(default=0)
    eth = models.FloatField(default=0)
    bnb = models.FloatField(default=0)
    ada = models.FloatField(default=0)
    ltc = models.FloatField(default=0)

    def __str__(self):
        return self.user.username + "-" + str(self.user.id)

option_choices = (
        ('buy', 'buy'),
        ('sell', 'sell')
        )

coin_choices = (
        ('btc', 'btc'),
        ('eth', 'eth'),
        ('bnb', 'bnb'),
        ('ada', 'ada'),
        ('ltc', 'ltc')
    )
class Trade(models.Model):
    trade_at = models.DateTimeField(auto_now_add=True, null=True)
    account = models.ForeignKey(demoAccount, on_delete=models.CASCADE, related_name='AccountTrade')
    option = models.CharField(max_length=4, choices=option_choices)
    coin = models.CharField(max_length=3, choices=coin_choices)
    price = models.FloatField(null=True, blank=True)
    sell_amount = models.FloatField(null=True,default=0)
    buy_amount = models.IntegerField(null=True,default=0)

    class Meta:
        ordering = ['-trade_at']

    def __str__(self):
        return self.account.user.username + "-" + str(self.account.user.id) + " | " + self.option + " - " + self.coin