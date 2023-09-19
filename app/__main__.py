from src.config import Settings
from src.binance_talker import check_spot_balance
from dotenv import load_dotenv


def main():
    load_dotenv()
    Settings()

    print(check_spot_balance())  # Testing purposes TODO: remove


if __name__ == "__main__":
    main()
