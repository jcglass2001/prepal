
import os
from dotenv import load_dotenv
import yaml
from string import Template

load_dotenv()

with open('config/config.yml', 'r') as file:
    raw = file.read()
    sub = Template(raw).substitute(os.environ)

_config = yaml.safe_load(sub)

class RedisSettings:
    HOST = _config['redis']['host']
    PORT = _config['redis']['port']
    MEDIA_QUEUE = _config['redis']['media_queue']
    NOTION_QUEUE = _config['redis']['notion_queue']

class LLMSettings:
    HOST = _config['llm']['host']
    PROVIDER = _config['llm']['provider']
    MODEL = _config['llm']['model']
    USE_LLM = _config['llm']['enabled']

class DriveSettings:
    TARGET_FOLDER = _config['drive']['target_folder']
    POLLING_INTERVAL = _config['drive']['polling']['interval']
    CLIENT_SETTINGS = {
        "client_config_backend": "service",
        "service_config": {
            "client_json_file_path": "service-secrets.json",
        }
    }

class AppSettings:
    LOG_LEVEL = _config['app']['logging']
    WHISPER_MODEL = _config['whisper']['model']
 

