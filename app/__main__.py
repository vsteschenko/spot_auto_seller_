from src.config import Settings
from src.binance_talker import get_tickers_price
from dotenv import load_dotenv


def main():
    load_dotenv()
    Settings()

    print(get_tickers_price(["BTCUSDT", "BNBUSDT"]))  # Testing purposes TODO: remove


if __name__ == "__main__":
    main()
