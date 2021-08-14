"""Producer service, it generate stock quotes."""

import json
import time
from csv import DictReader

from confluent_kafka import Producer

from settings import PRODUCER_CONFIG


def start_producer(config: dict):
    """Read file with stock quotes and send them to Kafka broker."""

    producer = Producer(config)

    with open('stock-quotes-tesla.csv', newline='') as csv_file:
        dict_reader = DictReader(csv_file)
        for row in dict_reader:
            producer.produce("stock-quotes", json.dumps(row))
            time.sleep(1)

    producer.flush()


start_producer(config=PRODUCER_CONFIG)
