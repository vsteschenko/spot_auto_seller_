from binance import Client
from os import environ

from .static.constant import MinimumToDisplay


class BinanceConnector:
    c = None

    def __init__(self):
        self.c = self._create_connection()

    def get_account_data(self):
        tickers_for_search = self._get_spot_balance()
        return self._get_tickers_price(tickers_for_search)

    @staticmethod
    def _create_connection() -> Client:
        api_public = environ.get("BINANCE_API_PUBLIC")
        api_secret = environ.get("BINANCE_API_SECRET")
        return Client(api_public, api_secret)

    def _get_spot_balance(self) -> list:
        assets_that_cost_more_than_x = []

        for asset in self.c.get_user_asset():
            free_amount_of_asset = float(asset.get("free"))
            asset_btc_valuation = float(asset.get("btcValuation"))

            if free_amount_of_asset > 0 and \
                    asset_btc_valuation > MinimumToDisplay.minimum_asset_btc_cost.value:
                assets_that_cost_more_than_x.append(asset)

        return assets_that_cost_more_than_x

    def _get_tickers_price(self, tickers_to_search: list[str]):
        pairs = []

        for symbol in tickers_to_search:
            ticker = self.c.get_ticker(symbol=symbol)
            pairs.append(ticker)

        return pairs
