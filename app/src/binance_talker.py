from binance import Client
from os import environ

from .static.constant import MinimumToDisplay


def create_connection() -> Client:
    api_public = environ.get("BINANCE_API_PUBLIC")
    api_secret = environ.get("BINANCE_API_SECRET")
    return Client(api_public, api_secret)


def get_spot_balance() -> list:
    c = create_connection()
    assets_that_cost_more_than_x = []

    for asset in c.get_user_asset():
        free_amount_of_asset = float(asset.get("free"))
        asset_btc_valuation = float(asset.get("btcValuation"))

        if free_amount_of_asset > 0 and asset_btc_valuation > MinimumToDisplay.minimum_asset_btc_cost.value:
            assets_that_cost_more_than_x.append(asset)

    return assets_that_cost_more_than_x


def get_tickers_price(tickers_to_search: list[str]):
    c = create_connection()
    pairs = []

    for symbol in tickers_to_search:
        ticker = c.get_ticker(symbol=symbol)
        pairs.append(ticker)

    return pairs
