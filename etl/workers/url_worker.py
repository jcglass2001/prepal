from typing import final
from utils.kafka_consumer import create_kafka_consumer 
from config.settings import SUBMISSION_TOPIC
import logging


logging.basicConfig(level=logging.INFO)


def main():
    consumer = create_kafka_consumer(
        topic=SUBMISSION_TOPIC,
        group_id='url-worker'
    )

    logging.info(f"URL Worker is running listeneing on topic {consumer.subscription()}")

    try:
     for message in consumer:
        payload = message.value
        if payload.get('media_type') == 'website_url':
            logging.info(f"Received URL submission: {payload['source']}")
            try:
                logging.info("Processing url payload...")
                # process_url_payload(payload)
            except Exception as e:
                logging.error(f"Failed to process url payload: {e}")
    except KeyboardInterrupt:
        logging.warn(f"KeyboardInterrupt: URL Worker no longer listening on topic {consumer.subscription()}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
    
