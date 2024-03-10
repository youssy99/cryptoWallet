from django.db import models

# Create your models here.

class Crypto(models.Model):
    ticker=models.CharField(max_length=20)
    quantity=models.FloatField()
    buyValue=models.FloatField()
    avgPrice=models.FloatField()
    actualPrice=models.FloatField()
    variation=models.FloatField()
    actualValue=models.FloatField()
    currencyType=models.BooleanField()

    def __str__(self):
        return self.ticker

class ColumnName(models.Model):
    name=models.CharField(max_length=20)
    
    def __str__(self):
        return self.name