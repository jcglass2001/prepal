import threading

from pydrive2.files import ApiRequestError, FileNotUploadedError
from config.settings import DriveSettings, RedisSettings

# from processor.media import process_media_job
from utils.client import setup_drive_client, setup_rq
from utils.logging import setup_logger
from .base import BaseWatcher


class DriveService:
    """
    Class responsible for Drive API interactions
    """

    def __init__(self) -> None:
        self.logger = setup_logger(__name__)
        self.drive = setup_drive_client()

    def get_folder_id(self, folder_name: str) -> str:
        self.logger.info(f"Retrieving ID for target folder: {folder_name}")
        folder_list = self.drive.ListFile(
            {"q": "mimeType='application/vnd.google-apps.folder' and trashed=false"}
        ).GetList()

        for folder in folder_list:
            if folder["title"] == folder_name:
                id = folder["id"]
                self.logger.debug(f"Found folder {folder_name} with ID: {id}.")
                return id
        raise ValueError(f"Folder '{folder_name}' not found.")

    def list_files_in_folder(self, folder_id: str):
        try:
            list_file = (
                self.drive.ListFile(
                    {"q": f"'{folder_id}' in parents and trashed=false"}
                ).GetList()
            )  # TODO: utilize modifiedDate' or some parameter to optimize query

            self.logger.debug(f"Files in folder: {len(list_file)}")

            return list_file  # TODO: add and update variable to track either datetime for last processed or last polled
        except ApiRequestError as e:
            self.logger.error(
                f"Error occurred requesting files from folder {folder_id}: {e}"
            )
        except Exception as e:
            self.logger.error(
                f"Unhandled error occurred requesting files from folder {folder_id}: {e}"
            )


class DriveWatcher(BaseWatcher):
    """
    Class responsible for polling and enqueueing
    """

    def __init__(self, stop_event: threading.Event):
        super().__init__(stop_event)
        self.drive_service = DriveService()
        self.queue = setup_rq(RedisSettings.MEDIA_QUEUE)
        self.target_folder_id = self.drive_service.get_folder_id(
            DriveSettings.TARGET_FOLDER
        )
        self.polling_interval = DriveSettings.POLLING_INTERVAL

    def run(self):
        while not self.stop_event.is_set():
            try:
                files = self.drive_service.list_files_in_folder(self.target_folder_id)
                file_id_list = [file["id"] for file in files]
                # self.logger.debug(json.dumps(file, indent=2))
                try:
                    # TODO: enqueue media metadata along with processing task to redis
                    # - check if media has already been processed
                    # - retrieve metadata and processing task
                    # - push to queue
                    # self.queue.enqueue(process_media_job, {'file_ids': file_id_list})
                    job = lambda x: print(x)
                    self.queue.enqueue(job, {"file_ids": file_id_list})
                    self.logger.debug(f"Files IDs enqueued: {file_id_list}")

                except Exception as e:
                    self.logger.error(f"Unhandled error in queueing task: {e}")
            except ApiRequestError as e:
                self.logger.error(f"Error in handling request: {e}")
            except FileNotUploadedError as e:
                self.logger.error(f"Error in accessing metadata: {e}")
            except Exception as e:
                self.logger.exception(f"Unhandled error in DriveWatcher: {e}")
            finally:
                self.stop_event.wait(self.polling_interval)
