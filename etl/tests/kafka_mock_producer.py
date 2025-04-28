from kafka import KafkaProducer
from config.settings import KAFKA_BOOTSTRAP_SERVERS, SUBMISSION_TOPIC
import json
import logging

logging.basicConfig(level=logging.INFO)

def main():

    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    topic = SUBMISSION_TOPIC

    mock_submissions = [
        {
            "media_type": "website_url",
            "source": "https://downshiftology.com/reciper/shashuka",
            "submitted_by": "mock_user_1"
        },
        {
            "media_type": "video_url",
            "source": "https://www.youtube.com/shorts/pccoa!LeZwg",
            "submitted_by": "mock_user_2"
        },
        {
            "media_type": "video_file",
            "source": "filepath/example.mp4",
            "submitted_by": "mock_user_3"
        },
    ]

    for submission in mock_submissions:
        logging.info(f"Sending: {submission['media_type']} from {submission['source']}")
        producer.send(topic, value=submission)

    logging.info("All mock messages sent.")
    producer.flush()
        

if __name__ == "__main__":
    main()

