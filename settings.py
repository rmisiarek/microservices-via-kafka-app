"""Settings for producer and consumer."""

BROKER = "127.0.0.1:9092"

RECOMMENDATION_SERVICE_CONFIG = {
    'bootstrap.servers': BROKER,
    'group.id': "recommendation-group",
    'session.timeout.ms': 6000,
    'auto.offset.reset': 'latest',
}

PRODUCER_CONFIG = {
    'bootstrap.servers': BROKER,
}

STOCK_QUOTES_TOPIC = 'stock-quotes'
RECOMMENDATION_TOPIC = 'recommendations'
DASHBOARD_TOPICS = [STOCK_QUOTES_TOPIC, RECOMMENDATION_TOPIC]
