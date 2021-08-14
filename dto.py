"""Base Data Transer Objects."""

from dataclasses import dataclass


@dataclass
class StockQuote:
    """DTO for stock quote."""

    date: str = ""
    volume: int = 0
    open_price: float = 0
    close_price: float = 0
    high_price: float = 0
    low_proce: float = 0
