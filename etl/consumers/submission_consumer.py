from config.settings import KAFKA_BOOTSTRAP_SERVERS, CONSUMER_GROUP_ID, MEDIA_SUBMISSION_TOPIC
from kafka import KafkaConsumer

def start_submission_consumer():
    consumer = KafkaConsumer(
        MEDIA_SUBMISSION_TOPIC,
        group_id=CONSUMER_GROUP_ID,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS
    )
    
    print(f'Listening on topic: {MEDIA_SUBMISSION_TOPIC}')

    try:
        for message in consumer:
            submission = message.value
            print(f'Routing job for submission: {submission}')
    except KeyboardInterrupt:
        print(f'KeyboardInterrupt: No longer listening on topic: {MEDIA_SUBMISSION_TOPIC}')
    except Exception as e:
        print(f'An error occurred: {e}')
    finally:
        consumer.close()
