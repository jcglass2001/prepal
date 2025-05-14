from pydrive.auth import GoogleAuth 
from pydrive.drive import GoogleDrive
import json
import threading
import time
from config.settings import settings
from .base import BaseWatcher 



class DriveWatcher(BaseWatcher):
    def __init__(self, stop_event: threading.Event):
        super().__init__(stop_event)
        self.drive = self._setup_drive()
        self.target_folder_id = self._get_target_folder_id(settings.TARGET_FOLDER)
        self.polling_interval = 500

    def _setup_drive(self):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        
        return GoogleDrive(gauth)
    
    def _get_target_folder_id(self, folder_name : str):
        # Query DriveAPI to retrieve list of folders in drive
        folder_list = self.drive.ListFile({'q': "mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()

        for folder in folder_list:
            self.logger.info(f"Locating target folder: {folder_name}")
            if folder['title'] == folder_name:
                id = folder['id']
                self.logger.info(f"Target folder found with ID: {id}.")
                self.logger.debug(f"Folder '{folder_name}' metadata: {json.dumps(folder, indent=2)}")
                return id

        # Raise error if folder not found 
        raise ValueError(f"Folder {folder_name} not found.")

    def run(self):

        while not self.stop_event.is_set():
            try:
                
                # Query DriveAPI to retrieve list of files in target folder 
                folder_list_file = self.drive.ListFile({'q': f"'{self.target_folder_id}' in parents"})

                for file in folder_list_file:
                    self.logger.debug(json.dumps(file, indent=2))
                    # todo: enqueue media metadata along with processing task to redis
                    # - check if media has already been processed
                    # - retrieve metadata and processing task
                    # - push to queue

            except Exception as e:
                self.logger.exception(f"Unhandled error in DriveWatcher: {e}")
            finally:
                self.stop_event.wait(self.polling_interval)
