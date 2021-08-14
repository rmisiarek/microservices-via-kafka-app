"""Producer service, it generate stock quotes."""

import json
import time
from csv import DictReader
from dataclasses import asdict
from datetime import datetime

from confluent_kafka import Producer

from dto import StockQuote
from settings import PRODUCER_CONFIG


def parse_date(date: str) -> str:
    """Format date."""

    original_dt = datetime.strptime(date, '%m/%d/%Y')
    formatted_dt = original_dt.strftime('%d.%m.%y')
    return formatted_dt


def parse_price(price: str) -> float:
    """Change price from str to float without dollar sign."""

    return float(price.lstrip('$'))


def start_producer(config: dict):
    """Read file with stock quotes and send them to Kafka broker."""

    producer = Producer(config)

    with open('stock-quotes-tesla.csv', newline='') as csv_file:
        dict_reader = DictReader(csv_file)
        for row in dict_reader:
            dto = StockQuote(
                date=parse_date(row['Date']),
                volume=int(row['Volume']),
                open_price=parse_price(row['Open']),
                close_price=parse_price(row['Close']),
                high_price=parse_price(row['High']),
                low_proce=parse_price(row['Low']),
            )

            producer.produce("stock-quotes", json.dumps(asdict(dto)))
            time.sleep(1)

    producer.flush()


start_producer(config=PRODUCER_CONFIG)
