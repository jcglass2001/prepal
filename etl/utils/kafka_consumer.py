from config.settings import KAFKA_BOOTSTRAP_SERVERS
from kafka import KafkaConsumer
import json

def create_kafka_consumer(topic: str, group_id: str):
    return KafkaConsumer(
        topic,
        group_id=group_id,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    )

