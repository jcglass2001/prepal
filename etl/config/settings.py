from dotenv import load_dotenv
from utils.loader import load_yaml_config, get_config_path
import os

load_dotenv()

_yaml_config = load_yaml_config(get_config_path())

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")
    KAFKA_BROKER = os.getenv("KAFKA_BROKER")
    LLM_HOST = os.getenv("LLM_HOST", "http://localhost:11434/api/chat")
    CONSUMER_GROUP_ID = os.getenv("KAFKA_CONSUMER_GROUP", "null")

    ACCEPTED_MEDIA_TYPES = _yaml_config.get("accepted_media_types", [])
    KAFKA_TOPIC = _yaml_config["kafka"]["topic"]
    LLM_PROVIDER = _yaml_config["llm"]["provider"]
    LLM_MODEL = _yaml_config["llm"]["model"]
    USE_LLM = _yaml_config["llm"]["enabled"]
    LOG_LEVEL = _yaml_config.get("log_level", "INFO")
    WORKER_NAME = _yaml_config.get("worker_name","default_worker")

settings = Settings()
