
import yfinance as yf
import matplotlib
import requests
import time
import urllib.request
import json
import pprint
import numpy as np
from mainarg import stock,convertlst,goodmood,sigmoid,sigmoidderivative,geo
from flask import Flask, redirect, render_template, url_for, Request,request
import csv


api_key = '82e12f4da82605a5564356a9f44740d5'
msft = yf.Ticker("MSFT")
api_token = 3


x = stock('AAPL')
zzz = stock('MSFT')
xxx = stock('TSLA')
nnn = stock('NFLX')
z = convertlst(x)#AAPL
zz = convertlst(zzz)#MSFT
xx = convertlst(xxx)#TSLA
nn = convertlst(nnn)#NTFLX






x1 =  ((xx['regular market open']- xx['previousclose'])/xx['previousclose'])
if x1 > 0:
    x1 = 1
elif x1 <0:
    x1 = 0



z1 = goodmood()[0]
if z1 == 'clear sky' or 'scattered clouds' or 'few clouds':
    z1 = 1
else: z1 = 0

#addedbias
n1 = 0



m = 0
if xx['previousclose'] < xx['regularmarketprice']:
    m = 1
else: m=0

def ML():
    traininginputs = np.array([[x1,z1,n1]]          
                                    
                                    )

    trainingoutputs = np.array([[m]]).T
   

    np.random.seed(1)

    synapticweights = 2* np.random.random((3,1))-1
    #print('random synaptic weights:')
    #print(synapticweights)


    for iteration in range(100):
        inputlayer = traininginputs
        outputs = sigmoid(np.dot(inputlayer,synapticweights))
        error = trainingoutputs - outputs
        adjustment = error *sigmoidderivative(outputs)
        synapticweights += np.dot(inputlayer.T,adjustment)
    
    #print("outputs after training:")
    #print(outputs)
    return outputs
outputs = ML()

def buysell():
    if outputs > .5 :
        return "buy"
    elif outputs == .5:
        return"hold"
    else: return "sell"






decisions = buysell()



app = Flask(__name__)



@app.route('/', methods=["GET","POST"])
def form():
    if request.method == "POST":
        email = request.form['located']
        fieldnames = ['email']
        with open('data.csv','w') as inFile:
            writer = csv.DictWriter(inFile, fieldnames=fieldnames)
            writer.writerow({'email': email})

            return render_template("display.html",decision = decisions,mlout =outputs) 
    return render_template("website.html")
    

if __name__ == '__main__':
   app.run(debug=True)


