import csv
import numpy as np
from sklearn.svm import SVR
import requests
import datetime
import scrapeGoogleFinanceNews
import sentimentAnalysis
import math
import json

#Not used.
GOOGLE_URL_1 = 'http://www.google.com/finance/historical?q=NASDAQ%3A'
GOOGLE_URL_2 = '&output=csv'

QUANDL_API_KEY = "TMxqU2KUyqYuAebq9hwG"
QUANDL_URL_1 = "https://www.quandl.com/api/v3/datasets/WIKI/"
QUANDL_URL_2 = "/data.csv?rows=22&api_key="+QUANDL_API_KEY
QUANDL_URL_3 = "/metadata.json?api_key="+QUANDL_API_KEY

def get_data(filename):
    dates = []
    prices = []
    with open(filename, 'r') as csvfile:
        csvFileReader = csv.reader(csvfile)
        next(csvFileReader)  # skipping column names
        for row in csvFileReader:
            dates.append(int(row[0].split('-')[2]))
            prices.append(float(row[2]))
        return dates,prices


def predict_price(dates, prices, x):
    dates = np.reshape(dates, (len(dates), 1))  # converting to matrix of n X 1
    svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)  # defining the support vector regression models
    svr_rbf.fit(dates, prices)  # fitting the data points in the models
    return svr_rbf.predict(x)[0]


def get_historical(quote):
    url = QUANDL_URL_1 + quote + QUANDL_URL_2
    r = requests.get(url, stream=True)
    if r.status_code != 400:
        with open(quote + ".csv", 'wb') as f:
            for chunk in r:
                f.write(chunk)
    return True

def get_company_name(symbol):
    url = QUANDL_URL_1 + symbol + QUANDL_URL_3
    r = requests.get(url, stream=True)
    company_name = ""

    if r.status_code != 400:
        metadata_dict = json.loads(r.text)['dataset']
        company_name = metadata_dict['name'].lower()
        company_name = company_name[0:company_name.index("(" + symbol.lower() + ")")-1].strip()

    return company_name

def main(symbol):
    get_historical(symbol)
    name = get_company_name(symbol)
    dates,prices = get_data(symbol + ".csv")  # calling get_data method by passing the csv file to it

    predicted_price = predict_price(dates, prices, (datetime.datetime.now() + datetime.timedelta(days=1)).day)
    twittedPredictedScore = sentimentAnalysis.tweetAnalysis(symbol, name)
    googleNewsPredictedScore = scrapeGoogleFinanceNews.googleFinance(symbol)
    stockPredictedScore = (predicted_price - prices[0]) / prices[0]

    CombinedComputedValue = ((twittedPredictedScore + googleNewsPredictedScore + stockPredictedScore) / 3) * 100
    CombinedComputedValue = sigmoid(CombinedComputedValue)
    rating = 0

    if CombinedComputedValue > 0.6:
        rating = 3
    elif CombinedComputedValue >= 0.2:
        rating = 2
    else:
        rating = 1

    return (predicted_price, rating)


def sigmoid(val):
    return (1 / (1 + (math.e) ** -val))
