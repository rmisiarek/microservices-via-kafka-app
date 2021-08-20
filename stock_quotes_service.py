"""Producer service, it generate stock quotes."""

import json
import logging
import signal
import sys
import time
from csv import DictReader
from dataclasses import asdict
from datetime import datetime
from typing import Tuple

from confluent_kafka import Producer

from dto import StockQuote
from settings import PRODUCER_CONFIG

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

producer = Producer(PRODUCER_CONFIG)


def stop_producer(*_args, **_kwargs):
    """Stop producer."""

    logger.info('Stopping producer...')
    producer.flush()
    sys.exit(0)


signal.signal(signal.SIGINT, stop_producer)
signal.signal(signal.SIGTERM, stop_producer)


def parse_date(date: str) -> Tuple[str, float]:
    """Format date to string and milliseconds since epoch."""

    original_dt = datetime.strptime(date, '%m/%d/%Y')
    date_milliseconds = original_dt.timestamp() * 1000
    date_string = original_dt.strftime('%d.%m.%y')

    return date_string, date_milliseconds


def parse_price(price: str) -> float:
    """Change price from str to float without dollar sign."""

    return float(price.lstrip('$'))


def start_producer():
    """Read file with stock quotes and send them to Kafka broker."""

    with open('stock-quotes-tesla.csv', newline='') as csv_file:
        dict_reader = DictReader(csv_file)
        for row in dict_reader:
            date_string, date_milliseconds = parse_date(row['Date'])
            dto = StockQuote(
                date_string=date_string,
                date_milliseconds=date_milliseconds,
                volume=int(row['Volume']),
                open_price=parse_price(row['Open']),
                close_price=parse_price(row['Close']),
                high_price=parse_price(row['High']),
                low_price=parse_price(row['Low']),
            )

            logger.debug(dto)
            producer.produce("stock-quotes", json.dumps(asdict(dto)))
            time.sleep(1)

    producer.flush()


start_producer()
