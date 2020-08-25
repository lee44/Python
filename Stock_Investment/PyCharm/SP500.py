import bs4 as bs
import datetime as dt
import os
# Pandas is a library for analyzing data by creating a Python object called dataframe which are rows and columns
import pandas as pd
import pandas_datareader.data as web
import pickle
import requests

def savesp500():
    # returns a response object
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    # Grabs the html code as a text
    soup = bs.BeautifulSoup(resp.text)
    # finds the html tag table with id constituents
    table = soup.find('table', {'id': 'constituents'})
    # Tickers are stock symbols
    tickers = []
    # Loops thru all tr tags starting after the first tr tag because the first is just the columns of table
    for row in table.findAll('tr')[1:]:
        r = row.find('td').text
        # Adds every letter of stock symbol except last character(\n)
        tickers.append(r[:-1])

    # Opens a file called SP500 and dumps the tickers list inside it
    # Reason for pickle is because we don't want to reload all the stock symbols from the website so we save it
    # Python pickle module is used for serializing and deserializing a Python object structure
    # Serialization refers to the process of converting an object in memory to a byte stream that can be stored on disk or sent over a network
    with open("SP500.pickle","wb") as f :
        pickle.dump(tickers,f)

    print(tickers)

    return tickers

def getDataFromYahoo(reload_sp500 = False):
    if reload_sp500 :
        tickers = savesp500()
    else:
        # Open and Read the SP500 pickle file
        with open("SP500.pickle","rb") as f :
            tickers = pickle.load(f)

    if not os.path.exists('stocks_dfs'):
        os.makedirs('stock_dfs')

    start = dt.datetime(2010, 1, 1)
    end = dt.datetime(2019, 12, 31)

    for ticker in tickers[:10]:
        # Check if csv file exists. format(ticker) substitutes the {} for the stock symbol
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            # DataReader returns a dataframe
            df = web.DataReader(ticker,'yahoo',start,end)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already java {}'.format(ticker))

# getDataFromYahoo()

def compile_data():
    with open("SP500.pickle", "rb") as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()

    for count,ticker in enumerate(tickers):
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df.set_index('Date',inplace=True)

        df.rename(columns = {'Adj Close':ticker},inplace=True)
        df.drop(['Open','High','Low','Close','Volume'],1,inplace=True)

        # outer join returns rows from both data frames
        if main_df.empty:
            main_df = df
        else:
            main_df  = main_df.join(df,how = 'outer')

        # if count % 10 == 0:
        #     print(count)

        # print(main_df.head())
        main_df.to_csv('sp500_joined_closes.csv')

compile_data()
