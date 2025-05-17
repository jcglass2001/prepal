import json
import threading
import logging
from config.settings import app_config
from utils.client import setup_drive_client
from watcher.queue import QueueService
from .base import BaseWatcher 

class DriveService:
    """
    Class responsible for Drive API interactions
    """
    def __init__(self) -> None:
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.drive = setup_drive_client()

    def get_folder_id(self, folder_name: str) -> str:
        self.logger.info(f"Retrieving ID for target folder: {folder_name}")
        folder_list = self.drive.ListFile({'q': "mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()

        for folder in folder_list:
            if folder['title'] == folder_name:
                id = folder['id']
                self.logger.info(f"Found folder {folder_name} with ID: {id}.")
                return id
        raise ValueError(f"Folder '{folder_name}' not found.")
    
    def list_files_in_folder(self, folder_id: str):
        list_file = self.drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList() # TODO: utilize modifiedDate' or some parameter to optimize query
        return list_file 


class DriveWatcher(BaseWatcher):
    """
    Class responsible for polling and enqueueing
    """
    def __init__(self, stop_event: threading.Event):
        super().__init__(stop_event)
        self.drive_service = DriveService()
        self.queue_service = QueueService()
        self.target_folder_id = self.drive_service.get_folder_id(app_config.TARGET_FOLDER)
        self.polling_interval = app_config.POLLING_INTERVAL
        
    def run(self):

        while not self.stop_event.is_set():
            try:
                files = self.drive_service.list_files_in_folder(self.target_folder_id)                
                for file in files:
                    self.logger.debug(json.dumps(file, indent=2))
                    try:
                        # TODO: enqueue media metadata along with processing task to redis
                        # - check if media has already been processed
                        # - retrieve metadata and processing task
                        # - push to queue
                        self.queue_service.enqueue_task({'file_id': file['id']})
                    except Exception as e:
                        self.logger.error(f"Unhandled error in queueing task: {e}")

            except Exception as e:
                self.logger.exception(f"Unhandled error in DriveWatcher: {e}")
            finally:
                self.stop_event.wait(self.polling_interval)
