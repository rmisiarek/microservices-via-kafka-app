"""Settings for producer and consumer."""

BROKER = "127.0.0.1:9092"

CONSUMER_CONFIG = {
    'bootstrap.servers': BROKER,
    'group.id': "test-group",
    'session.timeout.ms': 6000,
    'auto.offset.reset': 'latest',
}

PRODUCER_CONFIG = {
    'bootstrap.servers': BROKER,
}
