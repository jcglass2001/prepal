from redis import Redis
from config.settings import app_config 
from utils.client import setup_drive_client


class MediaProcessor:
    def __init__(self, file_id: str, drive_client, redis_client):
        self.file_id = file_id
        self.drive_client = drive_client
        self.redis_client = redis_client

    def download_media(self):
        # queries drive client to download media by file_id
        pass

    def process_media(self):
        # planned: transcribe media and extract key data
        pass

    def run(self):
        # entry point to download, process, and update
        pass



drive_client = setup_drive_client()
redis_client = Redis(host=app_config.REDIS_HOST, port=app_config.REDIS_PORT)


def process_media_job(task_data: dict):
    file_id = task_data['file_id']
    processor = MediaProcessor(file_id, drive_client, redis_client)
    processor.run()
