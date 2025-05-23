from config.settings import app_config
from redis import Redis
from rq import Queue
from processor.media import process_media_job
from utils.logging import setup_logger

class QueueService:
    def __init__(self) -> None:
        self.connection = Redis(host=app_config.REDIS_HOST, port=app_config.REDIS_PORT)
        self.queue = Queue(name=app_config.REDIS_LIST_NAME, connection=self.connection)
        self.logger = setup_logger(__name__)
    def enqueue_task(self, task_data: dict):
        # enqueue a processing task or class reference and pass file_id as an argument
        self.queue.enqueue(process_media_job, task_data)
        self.logger.debug(f"Enqueueing {task_data}")
        pass

    def is_processed(self, file_id: str):
        # check processing history  
        pass

