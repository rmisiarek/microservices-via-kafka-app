"""Consumer service, it generate buy/sell recomendations."""

import json
from typing import Final

from base import Service
from settings import CONSUMER_CONFIG, PRODUCER_CONFIG


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
        print(
            f'recommendation: {recommendation} for {msg["close_price"]} '
            f'price with {self.average_price} average price.'
        )

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


if __name__ == "__main__":
    service = RecommendationService(
        consumer_config=CONSUMER_CONFIG,
        producer_config=PRODUCER_CONFIG,
        consumer_topics=['stock-quotes'],
        producer_topics=[''],
    )
    service.start()
