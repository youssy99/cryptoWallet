from django.shortcuts import render
from .models import Crypto, ColumnName
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import requests

# Create your views here.
def getPrice(ticker):
	key = "https://api.binance.com/api/v3/ticker/price?symbol="
	url=key+ticker
	data = requests.get(url) 
	data = data.json() 
	return data['price']

def getVariation(price1,price2):
	variation=round(((price2-price1)/price1)*100,2)
	return variation

def getPlot(prices,names,tot):
	matplotlib.use('agg')
	res=[]
	explode=[]
	for p in prices:
		explode.append(0)
		res.append(round((p/tot)*100,3))
	return res
	#plt.show(block=False)

def show(request):
    cryptos=Crypto.objects.all()
    columnNames=ColumnName.objects.all()
    names=[]
    prices=[]
    tot=0.00
    for crypto in cryptos:
        names.append(crypto.ticker)
        crypto.avgPrice=round(float(crypto.buyValue)/float(crypto.quantity),3)
        actualPrice=float(getPrice(crypto.ticker))
        crypto.actualPrice=round(actualPrice,3)
        if(crypto.currencyType==False):
             usdteur=float(getPrice("EURUSDT"))
             actualPrice=actualPrice/usdteur
             crypto.actualPrice=round(actualPrice,3)
        crypto.variation=float(getVariation(crypto.buyValue,actualPrice*crypto.quantity))
        prices.append(actualPrice*crypto.quantity)
        tot+=actualPrice*crypto.quantity
        crypto.actualValue=round(crypto.quantity*actualPrice,3)
        crypto.save()
    percentuage=getPlot(prices,names,tot)
    return render(request,'crypto_wallet/statement.html',{'cryptos':cryptos,'columnNames':columnNames,'names':names,'perc':percentuage})