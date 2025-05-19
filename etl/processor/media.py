import logging
from pydrive2.drive import GoogleDrive
from redis import Redis
from config.settings import app_config 
from utils.client import setup_drive_client

logging.basicConfig(level=app_config.LOG_LEVEL)

class MediaProcessor:
    def __init__(self, file_ids: list[str], drive_client: GoogleDrive, redis_client):
        self.file_ids = file_ids
        self.drive_client = drive_client
        self.redis_client = redis_client
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    def download_media(self):
        # queries drive client to download media by file_id
        self.logger.debug(f"Downloading media...")
        pass

    def process_media(self):
        # planned: transcribe media and extract key data
        self.logger.debug(f"Processing media")
        pass

    def run(self):
        # entry point to download, process, and update
        self.logger.debug(f"Running processor for payload: {self.file_ids}")
        self.download_media()
        self.process_media()



drive_client = setup_drive_client()
redis_client = Redis(host=app_config.REDIS_HOST, port=app_config.REDIS_PORT)


def process_media_job(task_data: dict):
    file_ids = task_data['file_ids']
    processor = MediaProcessor(file_ids, drive_client, redis_client)
    processor.run()
