from binance.client import Client
import pandas as pd
import os
from dotenv import load_dotenv  # Import load_dotenv to load .env file

# Load environment variables from .env file
load_dotenv()

def get_realtime_data(symbol, interval):
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    client = Client(api_key, api_secret)
    klines = client.get_klines(symbol=symbol, interval=interval, limit=100)
    data = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    data.set_index('timestamp', inplace=True)
    data = data.astype(float)
    print(data.head())  # Check the DataFrame structure
    return data


def get_latest_price(symbol):
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')

    client = Client(api_key, api_secret)
    ticker = client.get_symbol_ticker(symbol=symbol)
    return float(ticker['price'])



