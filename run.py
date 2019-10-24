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
    #logging.warning(data)
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

def get_title_guardian():
    api_key = '0c02b6f1-c863-430b-99c2-568f0ab32aa9'
    url_base = "https://content.guardianapis.com/search?q=Facebook&from-date=2019-01-01&api-key={}"
    final_url = (url_base.format(api_key))
    response = requests.get(final_url)
    data = response.json()

    for items in data['response']['results']:
        print (items['webTitle'])

    return data

#eventuall we will not need this
@app.route('/')
def home():
    stockdata = get_price(8, "TSLA")
    company = "TSLA"
    get_polarity();
    get_title_guardian()
    get_json(company)
    return render_template('graph.html', stockdata=stockdata, company=company)

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

# <<<<<<< Updated upstream
# #APIs
# =======
graphdata = {
    "polScore": .67,
    "data":[
            [1,10],
            [2,11],
            [3,9]
        ]
}

# >>>>>>> Stashed changes
@app.route('/api/test', methods=['GET'])
def apiRequest():
    # return json.dumps(stock)
    return json.dumps(graphdata)

#a user would call this API and ask for stock data about a given company for a given month
#should users have to pass in the company ticker or name?
@app.route('/api/stockdata/<string:company_ticker>/<int:month>', methods=['GET'])
def get_Stock_Data(company_ticker, month):
    ticker = company_ticker
    month = month

    if len(ticker) == 0:
        abort(404)
    if not month in range(1,13):
        abort(404)

    stockdata = get_price(month, ticker)
    jsonify(stockdata)

    stockary = []
    for key in stockdata:
        temp = []
        temp.append(key)
        temp.append(float(stockdata[key]))
        stockary.append(temp)


    #return jsonify({'Stock': ticker },{'month': month },{'Stockdata':stockary})
    return jsonify({'Stock': ticker,'month': month, 'Stockdata': stockary})


#a user would call this API and ask for the polarity score for a given company
@app.route('/api/polarity/<string:company_id>', methods=['GET'])
def apiPolarity(company_id):
    company = company_id

    if len(company) == 0:
        abort(404)

    #call future methods to get data about a company then run polarity analysis on it
    test_phrase = "Tesla may have more bad news on the horizon bad terrible awful analyst: Analyst"
    test_phrase = TextBlob(test_phrase);
    polarity = test_phrase.sentiment.polarity

    return jsonify({'Polarity Score': polarity })

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run()(debug=True, host='0.0.0.0')
