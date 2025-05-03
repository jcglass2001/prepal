import logging 
from .settings import settings

log_level = getattr(logging, settings.LOG_LEVEL.upper())
logging.basicConfig(
    level=log_level,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logging.debug(
    "\nWorker Configuration",
    f"ID: {settings.WORKER_NAME}",
    f"Kafka Topic: {settings.KAFKA_TOPIC}",
    f"Media Types: {settings.ACCEPTED_MEDIA_TYPES}",
    f"LLM Flag: {settings.USE_LLM}",
    f"DB URL: {settings.DATABASE_URL}"
)
