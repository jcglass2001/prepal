
import os
from dotenv import load_dotenv
import yaml
from string import Template

load_dotenv()

with open('config/config.yml', 'r') as file:
    raw = file.read()
    sub = Template(raw).substitute(os.environ)

CONFIG = yaml.safe_load(sub)

class Settings:
    # Redis
    REDIS_HOST= CONFIG['redis']['host']
    REDIS_PORT= CONFIG['redis']['port']
    REDIS_LIST_NAME = CONFIG['redis']['list_name']
    
    # Google Drive
    TARGET_FOLDER = CONFIG['drive']['target_folder']
    POLLING_INTERVAL = CONFIG['drive']['polling']['interval']

    # App
    LOG_LEVEL = CONFIG['app']['logging']


DRIVE_SETTINGS = {
    "client_config_backend": "service",
    "service_config": {
        "client_json_file_path": "service-secrets.json",
    }
}

app_config = Settings()
