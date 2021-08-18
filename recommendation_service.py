"""Consumer service, it generate buy/sell recomendations."""

import json
from typing import Final

from base import Service
from settings import PRODUCER_CONFIG, RECOMMENDATION_SERVICE_CONFIG


class RecommendationService(Service):
    """RecommendationService."""

    average_price: float = 0

    _quotes: list[float] = []

    AVERAGE_HOW_MANY_DAYS: Final[int] = 5
    RECOMMENDATION_BUY: Final[str] = "BUY"
    RECOMMENDATION_SELL: Final[str] = "SELL"

    def process_message(self, message):
        """Process message and generate response with recommendation."""

        msg = json.loads(message.value())
        recommendation = self.check_recommendation(close_price=msg['close_price'])
        response = {'recommendation': recommendation}

        self.produce_message(topic='recommendations', message=json.dumps(response))

    def check_recommendation(self, close_price: float) -> str:
        """Generate recommendation."""

        self._quotes.append(close_price)

        if len(self._quotes) == self.AVERAGE_HOW_MANY_DAYS:
            self.average_price = sum(self._quotes) / self.AVERAGE_HOW_MANY_DAYS
            self._quotes.pop()

        if self.average_price:
            if self.average_price >= close_price:
                return self.RECOMMENDATION_BUY

            return self.RECOMMENDATION_SELL

        return "N/A"


def start_service():
    """Run service."""

    service = RecommendationService(
        consumer_config=RECOMMENDATION_SERVICE_CONFIG,
        producer_config=PRODUCER_CONFIG,
        consumer_topics=['stock-quotes'],
        producer_topics=['recommendations'],
    )
    service.start()


start_service()
