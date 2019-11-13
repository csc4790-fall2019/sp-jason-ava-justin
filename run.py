from flask import Flask, request, render_template, jsonify, abort, make_response, request, url_for
from textblob import TextBlob
import requests
import re
import logging
import json
import calendar
import datetime as dt
from datetime import datetime

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

    return dictionary

#looking into other uses of the alphavantage api
def monthly_stock_data_json(ticker):
    api_key = 'DJWUA73FEMJVIPST'
    url_base = "https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={}&outputsize=full&apikey={}"
    final_url = (url_base.format(ticker,api_key))
    response = requests.get(final_url)
    data = response.json()
    #logging.warning(data)
    return data

def get_polarity():
    test_phrase = "Tesla may have more bad news on the horizon analyst: Analyst"
    test_phrase = TextBlob(test_phrase);
    print("Polarity Score:")
    print(test_phrase.sentiment.polarity);


def get_title_guardian(company, startDate, endDate):
    api_key = '0c02b6f1-c863-430b-99c2-568f0ab32aa9'
    company = company
    start_date = startDate
    end_date = endDate

    url_base = "https://content.guardianapis.com/search?q={}&from-date={}&to-date={}&page={}&api-key={}"

    final_url = (url_base.format(company, start_date, end_date, 1, api_key))
    response = requests.get(final_url)
    data = response.json()

    total_pages = int(data['response']['pages'])
    #total_pages = 1  #TEMPORARY, USE THE ONE ABOVE

    page_counter = 1
    guardian_dictionary = {} #key = date string, value = title

    while page_counter <= total_pages:
        final_url = (url_base.format(company, start_date, end_date, page_counter, api_key))
        response = requests.get(final_url)
        data = response.json()

        for items in data['response']['results']:
            guardian_date_time = datetime.strptime(items['webPublicationDate'], "%Y-%m-%dT%H:%M:%SZ") # unicode --> datetime object
            guardian_date = guardian_date_time.date()  #datetime --> date object
            guardian_date = guardian_date.strftime("%b %d, %Y") #date object --> string (optional for now)
            title = items['webTitle']
            # print(title)

            if company in title:
                if guardian_date not in guardian_dictionary:
                    guardian_dictionary[guardian_date] = []

                if title not in guardian_dictionary[guardian_date]:
                    guardian_dictionary[guardian_date].append(title)

        #Format of keys: Example guardian_dictionary['October 25, 2019'])
        page_counter += 1

    '''
    for date in sorted(guardian_dictionary):
        print '---'
        print date
        for title in guardian_dictionary[date]:
            print title
    '''

    return guardian_dictionary

#only works for queries within the past 2 months wtffffffff
def news_api(ticker, startDate, endDate):
    api_key = '9d9f82a5686443d19a2116e137024848'
    company = ticker
    start_date = startDate
    end_date = endDate

    #q - Keywords or a phrase to search for.
    #qInTitle - Keywords or phrases to search for in the article title only.
    url_base = ( 'https://newsapi.org/v2/everything?'
                 'q={}&'
                 'qInTitle={}&'
                 'from={}&'
                 'to={}&'
                 'sortBy=popularity&'
                 'language=en&'
                 'apiKey={}' )

    final_url = (url_base.format(company, company, start_date,end_date, api_key))

    response = requests.get(final_url)
    f= open("test.txt","w+")
    json.dump(response.json(), f)

#news_api('Telsa', '2019-10-13', '2019-11-08' )

#eventuall we will not need this
# @app.route('/')
# def home():
#     stockdata = get_price(8, "TSLA")
#     company = "TSLA"
#     get_polarity();
#     get_title_guardian()
#     get_json(company)
#     return render_template('graph.html', stockdata=stockdata, company=company)

# APIs
#a user would call this API and ask for stock data about a given company for a given month
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

    stockary.sort()

    return jsonify({'Stock': ticker,
                    'month': month,
                    'Stockdata': stockary})

#iterates through a dictionary d, for each element of a specific key in d, it runs sentiment analysis on that element,
#then averages the polarity scores for each element
def run_avg_sentiment( news_dict ):
    polarity_scores = {}
    for key in news_dict.keys():
        total_polarity = 0.0
        for item in news_dict[key]:
            test_phrase = item
            test_phrase = TextBlob(test_phrase);
            polarity = test_phrase.sentiment.polarity
            total_polarity += polarity
        avg_polarity = total_polarity/(len(news_dict[key]))
        polarity_scores[key] = avg_polarity

    return( polarity_scores )

tickers = {'TSLA': 'Tesla',
           'AAPL': 'Apple',
           'GOOGL': 'Google',
           'MSFT': 'Microsoft',
           'FB' : 'Facebook', }

#a user would call this API and ask for the polarity data for a given company
#this data will be plotted on the same graph as the stock data
#we will need to run sentiment analysis on news information from each day. Or at least the same time frame as the stock data, which is every day for a month rn
@app.route('/api/polarity/<string:company_ticker>', methods=['GET'])
def apiPolarity(company_ticker):
    ticker = company_ticker
    company = ''
    start_date = startDate
    end_date = endDate

    if len(ticker) == 0:
        abort(404)

    #look up ticker in the dictionary
    for key in tickers.keys():
        if ticker == key:
            company = tickers[key]

    if  len(company)== 0:
        abort(404)

    daily_news = get_title_guardian(company, '2019-10-01', '2019-10-25' )
    polarity_scores = run_avg_sentiment( daily_news )

    return jsonify({ 'Stock': company,
                     'Polarity Scores': polarity_scores })

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run()(debug=True, host='0.0.0.0')
