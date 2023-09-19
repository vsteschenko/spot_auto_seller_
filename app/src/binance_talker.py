from binance import Client
from os import environ


def check_spot_balance():
    api_public = environ.get("BINANCE_API_PUBLIC")
    api_secret = environ.get("BINANCE_API_SECRET")
    c = Client(api_public, api_secret)

    
