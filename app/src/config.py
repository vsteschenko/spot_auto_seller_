from pydantic_settings import BaseSettings


class Settings(BaseSettings, case_sensitive=True):
    binance_api_public: str
    binance_api_secret: str
