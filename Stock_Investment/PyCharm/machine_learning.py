from collections import Counter
import numpy as np
import pandas as pd

def process_data_for_labels(ticker):
    hm_days = 7
    df = pd.read_csv('sp500_joined_closes.csv',index_col = 0)
    tickers = df.columns.values.tolist()
    df.fillna(0,inplace=True)

    for i in range(1,hm_days+1):
        df['{}_{}d'.format(ticker,i)] = (df[ticker].shift(-i) - df[ticker]) / df[ticker]

    df.fillna(0, inplace = True)

    return tickers, df

def buy_sell_hold(*args):
    cols = [c for c in args]
    requirement = .02
    for col in cols:
        if col > requirement:
            return 1
        if col < -requirement:
            return -1
    return 0

def extract_featuresets(ticker):
    tickers, df = process_data_for_labels(ticker)

    # Adds a new column with values return by the function map. Map will use the buy_sell_hold function where 7 arguments are passed and each value of the new column will be 1,-1, or 0
    df['{}_target'.format(ticker)] = list(map(buy_sell_hold,
                                              df['{}_1d'.format(ticker)],
                                              df['{}_2d'.format(ticker)],
                                              df['{}_3d'.format(ticker)],
                                              df['{}_4d'.format(ticker)],
                                              df['{}_5d'.format(ticker)],
                                              df['{}_6d'.format(ticker)],
                                              df['{}_7d'.format(ticker)],
                                              ))

    vals = df['{}_target'.format(ticker)].values.tolist()
    # Counts every string inside the {}_target column
    str_vals = [str(i) for i in vals]
    # Counter counts number of values for each group(1,-1, 0)
    print('Data spread:', Counter(str_vals))
    # Replace empty entries with 0
    df.fillna(0, inplace = True)
    # Replaces all negative and positive infinity values with NAN(No Availale Number) because on line 13, dividing by zero can happen
    df = df.replace([np.inf, -np.inf],np.nan)
    df.dropna(inplace=True)

    # [ticker for ticker in tickers] is called list comprehension. It creates a list much faster than using a for loop to add elements to a list
    # Don't confuse ticker with the parameter. Any variable name could be used as long as it replaces both ticker names
    # pct_change() calculates percentage change from previous to current element for all ticker columns in the list
    df_vals = df[[ticker for ticker in tickers]].pct_change()
    df_vals = df_vals.replace([np.inf, -np.inf],0)
    df_vals.fillna(0, inplace = True)

    X = df_vals.values
    y = df['{}_target'.format(ticker)].values

    # df.to_csv('extract_featuresets.csv')
    print([ticker for ticker in tickers])

    return  X,y,df

# extract_featuresets('ATVI')
# process_data_for_labels('ATVI')