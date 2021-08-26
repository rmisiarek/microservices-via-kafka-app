"""Base Data Transer Objects."""

from dataclasses import dataclass


@dataclass
class StockQuote:
    """DTO for stock quote."""

    date_string: str = ""
    date_milliseconds: float = 0
    volume: int = 0
    open_price: float = 0
    high_price: float = 0
    low_price: float = 0
    close_price: float = 0
