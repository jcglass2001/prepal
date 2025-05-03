from config.settings import settings  
from kafka import KafkaConsumer
import json

def create_kafka_consumer():
    return KafkaConsumer(
        settings.KAFKA_TOPIC,
        group_id=settings.WORKER_NAME,
        bootstrap_servers=settings.KAFKA_BROKER,
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    )

