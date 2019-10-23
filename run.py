from flask import Flask, request, render_template, jsonify, abort, make_response, request, url_for
from textblob import TextBlob
import requests
import re
import logging
import json
import calendar

#from flask.ext.cors import CORS, cross_origin
from flask_cors import CORS, cross_origin

app = Flask(__name__, template_folder='templates/')
CORS(app)

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
    get_title_guardian()
    return render_template('graph.html', stockdata=stockdata, company=company)

@app.route('/hello')
def hello():
    testdata = "Test Data"
    return render_template('hello.html', testdata=testdata)

stock = {
    "stock": "TSLA",
    "price": 10.00,
    "polScore": .67,
    "stocks": [
        {
            'stock': 'TSLA',
            'price': '10.00'
        },
        {
            'stock': 'FB',
            'price': '5.00'
        }
    ]
}

def get_title_guardian():
    api_key = '0c02b6f1-c863-430b-99c2-568f0ab32aa9'
    url_base = "https://content.guardianapis.com/search?q=Facebook&from-date=2019-01-01&api-key={}"
    final_url = (url_base.format(api_key))
    response = requests.get(final_url)
    data = response.json()

    for items in data['response']['results']:
        print (items['webTitle'])

    return data

#APIs
@app.route('/api/test', methods=['GET'])
def apiRequest():
    return json.dumps(stock)

@app.route('/api/stockdata', methods=['GET'])
def apiStockData():
    stockdata = get_price(8, "TSLA")
    return('Processing Stock Data')

@app.route('/api/stockdata/<string:company_id>', methods=['GET'])
def get_Stock_Data(company_id):
    company = company_id
    if len(company) == 0:
        abort(404)
    return jsonify({'company': company })

if __name__ == '__main__':
    app.run()(debug=True, host='0.0.0.0')
