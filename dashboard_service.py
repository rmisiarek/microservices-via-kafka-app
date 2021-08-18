"""Dashboard service, it present stock quotes and recommendations."""

import json

from base import Service
from settings import DASHBOARD_SERVICE_CONFIG, PRODUCER_CONFIG


class DashboardService(Service):
    """DashboardService."""

    def process_message(self, message):
        msg = json.loads(message.value())

        if message.topic() == 'stock-quotes':
            self.process_stock_quotes(message=msg)

        if message.topic() == 'recommendations':
            self.process_recommendations(message=msg)

    @staticmethod
    def process_stock_quotes(message):
        """Process received stock quotes."""

        print(f'process_stock_quotes = {message}')

    @staticmethod
    def process_recommendations(message):
        """Process received recommendation."""

        print(f'process_recommendations = {message}')


if __name__ == "__main__":
    service = DashboardService(
        consumer_config=DASHBOARD_SERVICE_CONFIG,
        producer_config=PRODUCER_CONFIG,
        consumer_topics=['stock-quotes', 'recommendations'],
        producer_topics=[''],
    )
    service.start()
