import logging
import json
import binance.exceptions

from binance import Client
from os import environ

from .static.constant import MinimumToDisplay, Other
from .static.exceptions import WrongAPIKey
from .calculations import is_more_than_min_order


def _create_connection() -> Client:
    api_public = environ.get("BINANCE_API_PUBLIC")
    api_secret = environ.get("BINANCE_API_SECRET")
    return Client(api_public, api_secret)


class BinanceGetInfoConnector:
    c = None

    def __init__(self):
        self.c = _create_connection()

    def check_if_api_key_is_valid(self):
        logging.info("Started checking is binance api key is valid")
        account, spot_info = {}, {}
        try:
            account = self.c.get_account()
            spot_info = self.c.get_account_api_permissions()
        except binance.exceptions.BinanceAPIException:
            logging.error("Most certainly wrong api key")

        if not account or account.get("canTrade", False) is not True:
            raise WrongAPIKey("Failed to fetch info with this key. Make sure that the key from .env works.")

        if not spot_info or spot_info.get("enableSpotAndMarginTrading", False) is not True:
            raise WrongAPIKey("API key does not have required (spot trade) permissions.")

        logging.info("API key is valid!")

    def get_account_data(self):
        spot_balance = self._get_spot_balance()
        tickers_for_search = self._clean_tickers_list(spot_balance)
        tickers_to_keep = [
            ticker for ticker in tickers_for_search
            if ticker.get('asset') in json.loads(environ.get("LIST_OF_TICKERS_TO_SELL", "[]"))
        ]
        tickers_with_price = self._get_tickers_price(tickers_to_keep)
        tickers_with_exchange_info = self._append_exchange_info_about_ticker(tickers_with_price)
        tickers_calculated_min_order_info = [is_more_than_min_order(x) for x in tickers_with_exchange_info]
        return [x for x in tickers_calculated_min_order_info if x.get("is_more_than_min_order") is True]

    def _get_spot_balance(self) -> list[dict]:
        assets_that_cost_more_than_x = []

        for asset in self.c.get_user_asset():
            free_amount_of_asset = float(asset.get("free"))
            asset_btc_valuation = float(asset.get("btcValuation"))

            if free_amount_of_asset > 0 and \
                    asset_btc_valuation > MinimumToDisplay.minimum_asset_btc_cost.value:
                assets_that_cost_more_than_x.append(asset)

        return assets_that_cost_more_than_x

    def _clean_tickers_list(self, tickers_list: list[dict]):
        spot_pairs = [x.get("symbol") for x in self.c.get_exchange_info().get("symbols")]
        return [x for x in tickers_list if f"{x.get('asset', '')}USDT" in spot_pairs]

    def _append_exchange_info_about_ticker(self, tickers_list: list[dict]):
        def find(lst, key, value):
            for i, dic in enumerate(lst):
                if dic.get(key, "") == value:
                    return i
            return -1

        exchange_info = self.c.get_exchange_info().get("symbols")
        tickers_to_search = [ticker.get("symbol") for ticker in tickers_list]
        return_list = []

        for ticker in exchange_info:
            symbol = ticker.get("symbol")
            if symbol in tickers_to_search:
                index = find(tickers_list, "symbol", symbol)
                return_list.append({**tickers_list[index], **ticker})

        return return_list

    def _get_tickers_price(self, tickers_to_search: list[dict]):
        result_pairs = []
        pairs_to_search = [f"{x.get('asset')}USDT" for x in tickers_to_search]

        for symbol, deposit_info in zip(pairs_to_search, tickers_to_search):
            ticker = self.c.get_ticker(symbol=symbol)
            result_pairs.append({**ticker, **deposit_info})

        return result_pairs


class BinancePostInfoConnector:
    c = None

    def __init__(self):
        self.c = _create_connection()

    @staticmethod
    def _convert_precision_to_integer(precision_string: str) -> int:
        precision_string = precision_string.rstrip('0')
        parts = precision_string.split(".")
        if len(parts) == 2:
            decimal_places = len(parts[1])
            return decimal_places
        else:
            return 0

    def sell_all_spot_coins_with_ticker(self, ticker_info: dict):
        ticker = ticker_info.get("symbol")
        precision_string = ""

        for x in ticker_info.get("filters"):
            if x.get("filterType") == "LOT_SIZE":
                precision_string = x.get("minQty", 0.0)
                break

        precision: int = self._convert_precision_to_integer(precision_string)
        quantity = round(ticker_info.get("available_to_sell_coin") * Other.sell_order_multiplier.value, precision)

        self.c.create_order(
            symbol=ticker,
            side="SELL",
            type="MARKET",
            quantity=quantity
        )
