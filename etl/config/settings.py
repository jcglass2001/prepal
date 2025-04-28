from dotenv import load_dotenv
import os

load_dotenv()

db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")
db_host = os.getenv("POSTGRES_HOST")
db_port = os.getenv("POSTGRES_PORT", 5432)

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_SERVERS")
SUBMISSION_TOPIC = os.getenv("KAFKA_TOPIC")
CONSUMER_GROUP_ID = os.getenv("KAFKA_CONSUMER_GROUP")

DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
