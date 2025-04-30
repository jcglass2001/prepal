from extractors.factory import ExtractorFactory
from utils.kafka_consumer import create_kafka_consumer 
from config.settings import SUBMISSION_TOPIC
import logging


logging.basicConfig(level=logging.INFO)
GROUP_ID = 'VIDEO_WORKER'

def main():
    consumer = create_kafka_consumer(
        topic=SUBMISSION_TOPIC,
        group_id=GROUP_ID
    )

    logging.info(f"{GROUP_ID} is running listeneing on topic {consumer.subscription()}")

    try:
     for message in consumer:
        payload = message.value
        if payload.get('media_type') == 'video_url':
            logging.info(f"Received submission: {payload['source']}")
            try:
                logging.info("Processing url...")
                process_payload(payload)
            except Exception as e:
                logging.error(f"Failed to process url: {e}")
        elif payload.get('media_type') == 'video_file':
                logging.info(f"Received submission: {payload['source']}")
                try:
                    logging.info("Processing file...")
                    process_payload(payload)
                except Exception as e:
                    logging.error(f"Failed to process file: {e}")
    except KeyboardInterrupt:
        logging.warning(f"KeyboardInterrupt: {GROUP_ID} no longer listening on topic {consumer.subscription()}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        consumer.close()

def process_payload(payload: dict):
    media_type = payload['media_type']
    extractor = ExtractorFactory.get_extractor(media_type)
    result = extractor.extract(payload)

if __name__ == "__main__":
    main()
    
