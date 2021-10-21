import requests
import pandas as pd

## API endpoint + details
endpoint = 'https://cloud.iexapis.com/v1/deep?token='
key = 'sk_ebd3172b0d5a4015be8ee12490c6cc70'
symbol = '&symbols='
stock = 'AAPL'

## parse it
url = endpoint + key + symbol + stock

## create the database
conn = sqlite3.connect('orderbook.db')

## create the list to store interim 
tick_data = []

## build the orderbook
def OrderBook(url):
    
    ## get the tick data
    response = requests.get(url)
    response_json = response.json()
    
    ## separate the keys
    ticktime = response_json['lastUpdated']
    bids = response_json['bids']
    asks = response_json['asks']
    trades = response_json['trades']

    ## create dataframes
    bids_df = pd.DataFrame.from_dict(bids, orient='columns')
    bids_df = bids_df.rename(columns={'price':'bid_price', 'size': 'bid_size'})
    
    asks_df = pd.DataFrame.from_dict(asks, orient='columns')
    asks_df = asks_df.rename(columns={'price':'ask_price', 'size': 'ask_size'})
    
    trades_df = pd.DataFrame.from_dict(trades, orient='columns')
    trades_df = trades_df[['price', 'size', 'timestamp']]
    trades_df = trades_df.rename(columns={'price':'trade_price', 'size': 'trade_size'})

    ## assemble the orderbook
    orderbook = pd.concat([bids_df, asks_df, trades_df])
    orderbook['time_of_tick'] = ticktime
    orderbook['timestamp'] = pd.to_datetime(orderbook['timestamp'], unit='ms')
    orderbook['time_of_tick'] = pd.to_datetime(orderbook['time_of_tick'], unit='ms')

    orderbook = orderbook.set_index(pd.DatetimeIndex(orderbook['timestamp']))
    orderbook = orderbook.drop(['timestamp'], axis=1)
    orderbook = orderbook.sort_index(ascending=False)

    return orderbook
   


