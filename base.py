"""Base service class"""

from abc import ABC, abstractmethod


class AbstractService(ABC):
    """AbstractService provides core methods for services."""

    @abstractmethod
    def start(self):
        """Start consumer loop."""

    @abstractmethod
    def stop(self, *args, **kwargs):
        """Stop consumer loop"""

    @abstractmethod
    def produce_message(self, message):
        """Send message to Kafka broker."""

    @abstractmethod
    def process_message(self, message):
        """Process received massage."""
