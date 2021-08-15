"""Base service class."""

import signal
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from confluent_kafka import Consumer, KafkaError, KafkaException, Producer


class AbstractService(ABC):
    """AbstractService provides core methods for services."""

    @abstractmethod
    def start(self):
        """Start consumer loop."""

    @abstractmethod
    def stop(self, *args, **kwargs):
        """Stop consumer loop"""

    @abstractmethod
    def produce_message(self, topic, message):
        """Send message to Kafka broker."""

    @abstractmethod
    def process_message(self, message):
        """Process received massage."""


@dataclass  # type: ignore
class Service(AbstractService):
    """Base class for Kafka consumer services."""

    consumer_config: dict = field(default_factory=dict)
    producer_config: dict = field(default_factory=dict)

    consumer_topics: list = field(default_factory=list)
    producer_topics: list = field(default_factory=list)

    consumer: Consumer = field(init=False)
    producer: Producer = field(init=False)

    running: bool = False

    def __post_init__(self):
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

        self.consumer = Consumer(self.consumer_config)
        self.producer = Producer(self.producer_config)

        self.running = True

    def start(self):
        try:
            self.consumer.subscribe(self.consumer_topics)

            while self.running:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:  # noqa
                        sys.stderr.write(
                            f'{msg.topic()} [{msg.partition()}] reached end at '
                            f'offset {msg.offset()}\n'
                        )
                    elif msg.error():
                        raise KafkaException(msg.error())
                else:
                    self.process_message(message=msg)
        finally:
            print(f'\nStopping {self.__class__.__name__} service...')
            self.consumer.close()

    def stop(self, *args, **kwargs):
        self.running = False

    def produce_message(self, topic, message):
        if topic in self.producer_topics:
            self.producer.produce(topic, message)
