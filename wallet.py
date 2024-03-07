# Import libraries 
import csv
import sys
import pandas as pd
import requests 
from colorama import Fore
import matplotlib.pyplot as plt
import numpy as np
fields=["Ticker","quantity","Price","AVG price","Currency"]
#Read json file
def getCSV():
	rows=[]
	try:
		file1=open("sample.csv","r")
	except:
		with open("sample.csv", "w") as outfile:
			csvwriter=csv.writer(outfile)
			csvwriter.writerow(fields)
			outfile.close()
		file1=open("sample.csv","r")
	with file1 as csvFile:
		csvreader=csv.reader(csvFile)
		next(csvreader)
		for row in csvreader:
			rows.append(row)
	return rows

#Write json file 
def putCSV(row):
	with open("sample.csv", "a") as outfile:
		csvwriter=csv.writer(outfile)
		csvwriter.writerow(row)
		outfile.close()
	return 200

def newFile():
	putCSV(fields)
#Add a cripto
def add(nome,quantita,prezzo,avgPrice,currency):
	row =[nome,quantita,prezzo,avgPrice,currency]
	return putCSV(row)

def getPrice(ticker):
	key = "https://api.binance.com/api/v3/ticker/price?symbol="
	url=key+ticker
	data = requests.get(url) 
	data = data.json() 
	return data['price']

def findID(ticker):
	rows=getCSV()
	i=0
	for row in rows:
		if(row[0]==ticker):
			return i
		i+=1

def removeRow(id):
	df=pd.read_csv('sample.csv')
	df=df.drop(id)
	df.to_csv('sample.csv',index=False)
	return "Cripto cancellata\n"

def getVariation(price1,price2):
	variation=round(((price2-price1)/price1)*100,2)
	return variation

def getPlot(prices,names,tot):
	res=[]
	explode=[]
	for p in prices:
		explode.append(0)
		res.append(round((p/tot)*100,2))
	y=np.array(res)
	plt.figure("Crypto pie")
	plt.title("Crypto pie distribution",fontdict={'fontsize':30})
	plt.pie(y,labels=names,explode=explode,startangle=90,autopct='%1.1f%%')
	plt.axis('equal')
	plt.show(block=False)

def printMenu():
	print("Benvenuto, quale operazione vuoi effettuare?\n 1)Stato delle cripto\n 2)Aggiungere una cripto\n 3)Modificare una cripto\n 4)Rimuovere una cripto\n 5)Termina il programma\n\n")
	scelta=int(input("Scelta:"))
	return scelta

def program(scelta):
	if(scelta==1):
		prices=[]
		names=[]
		totAct=0.00
		totOld=0.00
		data=getCSV()
		for row in data:
			price=float(getPrice(row[0]))
			actualPrice=round(price*float(row[1]),2)
			if(int(row[4])==2):
				usdteur=float(getPrice("EURUSDT"))
				actualPrice=round(actualPrice/usdteur,2)
			variazione=getVariation(float(row[2]),actualPrice)
			if(variazione>0):
				variazione=Fore.GREEN+f"{variazione}%"+Fore.RESET
			else:
				variazione=Fore.RED+f"{variazione}%"+Fore.RESET
			print(f"{row[0]}:\n\tquantita:{row[1]}\n\tvalore all'acquisto acquisto: {row[2]}€\n\tvalore corrente: {actualPrice}€\n\tVariazione:{variazione}")
			names.append(row[0])
			prices.append(actualPrice)
			totOld+=float(row[2])
			totAct+=actualPrice
		totOld=round(totOld,2)
		totAct=round(totAct,2)
		getPlot(prices,names,totAct)
		differenza=round(totAct-totOld,2)
		if(totAct>totOld):
			totAct=Fore.GREEN+f"{totAct}€"+Fore.RESET
		else:
			totAct=Fore.RED+f"{totAct}€"+Fore.RESET
		if(differenza>0):
			differenza=Fore.GREEN+f"{differenza}€"+Fore.RESET
		else:
			differenza=Fore.RED+f"{differenza*(-1)}€"+Fore.RESET
		print(f"Valore totale: {totOld}€\nValore al momento: {totAct}\nDifferenza: {differenza}")
	elif(scelta==2):
		ticker=input("Inserisci il ticker della cripto: ")
		quantita=float(input("Inserisci la quantita' di cripto che hai acquistato: "))
		prezzo=float(input("Inserisci il prezzo d'acquisto: "))
		avgPrice=(prezzo/quantita)
		print("Currency?\n1)EUR\n2)USDT")
		currency=int(input())
		if(add(ticker,quantita,prezzo,avgPrice,currency)==200):
			print("Cripto aggiunta")
		else:
			print("Cripto non aggiunta, riprovare")
	elif(scelta==3):
		rows=getCSV()
		i=1
		scelta=-1
		while scelta>len(rows) or scelta<1:
			print("Scegli la cripto che vuoi modificare\n")
			for row in rows:
				print(f"{i}){row[0]}\n")
				i+=1
			scelta=int(input("Scelta:"))
		scelta=scelta-1
		row=rows[scelta]
		print("Vuoi modificare il ticker?")
		risposta=input("Risposta:")
		if 	(risposta=="Si" or risposta=="si"):
			row[0]=input("Inserisci il nuovo ticker:")
		print("Vuoi modificare la quantita' acquistata?")
		risposta=input("Risposta:")
		if	(risposta=="Si" or risposta=="si"):
			row[1]=float(input("Inserisci la nuova quantita':"))
		print("Vuoi modificare il prezzo di acquisto?")
		risposta=input("Risposta:")
		if 	(risposta=="Si" or risposta=="si"):
			row[2]=float(input("Inserisci il nuovo prezzo di acquisto:"))
		row[3]=(float(row[2])/float(row[1]))
		if(add(row[0],row[1],row[2],row[3],int(row[4]))==200):
			print("Cripto Modificata")
		else:
			print("Cripto non modificata, riprovare")
		removeRow(scelta)
	elif(scelta==4):
		print("Inserisci il ticker della cripto che vuoi rimuovere: ")
		ticker=input()
		id=findID(ticker)
		risposta=removeRow(id)
		print(f"{risposta}")

choice=0		
while choice != 5:
	choice=printMenu()
	program(choice)
