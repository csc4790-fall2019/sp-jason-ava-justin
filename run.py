from flask import Flask, request, render_template
from textblob import TextBlob
import requests
import re
import logging
import json
import calendar

app = Flask(__name__, template_folder='templates/')
cal = calendar.Calendar()


LOGGER = logging.getLogger('app')
LOGGER.setLevel(logging.INFO)

def get_json(ticker):
    api_key = 'DJWUA73FEMJVIPST'
    url_base = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&outputsize=full&apikey={}"
    final_url = (url_base.format(ticker,api_key))
    response = requests.get(final_url)
    data = response.json()
    return data

def get_price(month, ticker):
    dictionary = {}
    stocks = get_json(ticker)
    calendar.setfirstweekday(calendar.MONDAY)
    days = calendar.monthrange(2019,month)
    days=(days[1])
    '''days start with zero'''
    for x in range(days):
        if (x+1<10 and "2019-08-0{}".format(x+1) in stocks["Time Series (Daily)"]):
            price = (stocks["Time Series (Daily)"]["2019-08-0{}".format(x+1)]["4. close"])
            dictionary["2019-08-0{}".format(x+1)] = price
        if ((x+1)>=10 and "2019-08-{}".format(x+1) in stocks["Time Series (Daily)"]):
            price = (stocks["Time Series (Daily)"]["2019-08-{}".format(x+1)]["4. close"])
            dictionary["2019-08-{}".format(x+1)] = price
    logging.warning(dictionary)
    return dictionary

def get_polarity():
    test_phrase = "Tesla may have more bad news on the horizon analyst: Analyst"
    test_phrase = TextBlob(test_phrase);
    print("Polarity Score:")
    print(test_phrase.sentiment.polarity);

@app.route('/')
def home():
    stockdata = get_price(8, "TSLA")
    company = "TSLA"
    get_polarity();
    return render_template('graph.html', stockdata=stockdata, company=company)

@app.route('/hello')
def hello():
    return render_template('hello.html')


if __name__ == '__main__':
    app.run()(debug=True, host='0.0.0.0')
