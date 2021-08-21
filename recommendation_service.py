"""Consumer service, it generate buy/sell recomendations."""

import json
import logging
from typing import Any, Dict, Final

from base import Service
from settings import PRODUCER_CONFIG, RECOMMENDATION_SERVICE_CONFIG

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RecommendationService(Service):
    """RecommendationService."""

    average_price: float = 0

    _quotes: list[float] = []

    AVERAGE_HOW_MANY_DAYS: Final[int] = 5
    RECOMMENDATION_BUY: Dict[str, Any] = {'y': 1, 'color': 'green'}
    RECOMMENDATION_SELL: Dict[str, Any] = {'y': -1, 'color': 'red'}

    def process_message(self, message):
        """Process message and generate response with recommendation."""

        msg = json.loads(message.value())
        recommendation = self.check_recommendation(close_price=msg['close_price'])

        if recommendation:
            logger.debug(recommendation)
            self.produce_message(
                topic='recommendations',
                message=json.dumps({'recommendation': recommendation})
            )

    def check_recommendation(self, close_price: float) -> dict:
        """Generate recommendation."""

        self._quotes.append(close_price)

        if len(self._quotes) == self.AVERAGE_HOW_MANY_DAYS:
            self.average_price = sum(self._quotes) / self.AVERAGE_HOW_MANY_DAYS
            self._quotes.pop()

        if self.average_price:
            if close_price >= self.average_price:
                return self.RECOMMENDATION_BUY

            return self.RECOMMENDATION_SELL

        return {}


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
