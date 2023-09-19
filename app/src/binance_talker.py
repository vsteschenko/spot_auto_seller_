from binance import Client
from os import environ

from .static.constant import MinimumToDisplay


def check_spot_balance() -> list:
    api_public = environ.get("BINANCE_API_PUBLIC")
    api_secret = environ.get("BINANCE_API_SECRET")
    c = Client(api_public, api_secret)
    del api_public, api_secret

    assets_that_cost_more_than_x = []

    for asset in c.get_user_asset():
        free_amount_of_asset = float(asset.get("free"))
        asset_btc_valuation = float(asset.get("btcValuation"))

        if free_amount_of_asset > 0 and asset_btc_valuation > MinimumToDisplay.minimum_asset_btc_cost.value:
            assets_that_cost_more_than_x.append(asset)

    return assets_that_cost_more_than_x
