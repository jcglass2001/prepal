from oauth2client.service_account import time
from config.settings import settings
from pydrive.auth import GoogleAuth 
from pydrive.drive import GoogleDrive
import json
import threading
import logging
from config.settings import settings

POLLING_INTERVAL = 500

class DriveWatcher(threading.Thread):
    def __init__(self) -> None:
        super().__init__()
        self.target_folder = settings.TARGET_FOLDER
        self.drive = self._setup_drive()

    def _setup_drive(self):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        
        return GoogleDrive(gauth)
    
    def _get_target_folder_id(self, file_list):
        for folder in file_list:
            logging.info(f"Locating target folder: {self.target_folder}")
            if folder['title'] == self.target_folder:
                logging.debug(f"Folder '{self.target_folder}' medata: {json.dumps(folder, indent=2)}")
                return folder['id'] 
        raise ValueError(f"Folder {self.target_folder} not found.")

    def run(self):
        while True:
            try:
                #Retrieve list of folders in drive
                drive_file_list = self.drive.ListFile({'q': "mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()

                # Retrieve list of files in target folders
                folder_id = self._get_target_folder_id(drive_file_list)
                folder_list_file = self.drive.ListFile({'q': f"'{folder_id}' in parents"})

                for file in folder_list_file:
                    logging.debug(json.dumps(file, indent=2))
                    # todo: enqueue media metadata along with processing task to redis
                    # - check if media has already been processed
                    # - retrieve metadata and processing task
                    # - push to queue
                    
                
                time.sleep(POLLING_INTERVAL)
            except KeyboardInterrupt:
                logging.warning("KeyboardInterrupt: ")
            except Exception as e:
                logging.error(f"Error in DriveWatcher: {e}")
                time.sleep(POLLING_INTERVAL)
