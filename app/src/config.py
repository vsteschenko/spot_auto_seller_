from pydantic_settings import BaseSettings


class Settings(BaseSettings, case_sensitive=True):
    BINANCE_API_PUBLIC: str
    BINANCE_API_SECRET: str
