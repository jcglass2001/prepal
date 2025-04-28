from utils.kafka_consumer import create_kafka_consumer 
from config.settings import SUBMISSION_TOPIC
import logging


logging.basicConfig(level=logging.INFO)
GROUP_ID = 'URL_WORKER'

def main():
    consumer = create_kafka_consumer(
        topic=SUBMISSION_TOPIC,
        group_id=GROUP_ID
    )

    logging.info(f"{GROUP_ID} is running listeneing on topic {consumer.subscription()}")

    try:
     for message in consumer:
        payload = message.value
        if payload.get('media_type') == 'website_url':
            logging.info(f"Received submission: {payload['source']}")
            try:
                logging.info("Processing payload...")
                # process_video_payload(payload)
            except Exception as e:
                logging.error(f"Failed to process payload: {e}")
    except KeyboardInterrupt:
        logging.warn(f"KeyboardInterrupt: {GROUP_ID} no longer listening on topic {consumer.subscription()}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
    
