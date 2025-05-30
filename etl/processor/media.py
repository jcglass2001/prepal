# Standard library imports
import os
import json
from os.path import exists
from typing import Any
from concurrent.futures import ThreadPoolExecutor, as_completed 

# Third part library imports
import whisper
from pydrive2.files import ApiRequestError
from redis import Redis


# Custom moudle imports
from config.settings import AppSettings, RedisSettings
from processor.strategy import LLMProcessingStrategy
from utils.client import setup_drive_client
from utils.logging import setup_logger 

class MediaProcessor:
    def __init__(self, file_ids: list[str]):
        self.file_ids = file_ids
        self.drive_client = setup_drive_client()
        self.redis_client = Redis(host=RedisSettings.HOST, port=RedisSettings.PORT)
        self.whisper_model = whisper.load_model(AppSettings.WHISPER_MODEL)
        self.logger = setup_logger(self.__class__.__name__)
            

    def _download_file(self, working_dir: str, file_id:str):
        """
        Queries API for file download based on file_id and returns path of downloaded file
        """

        file_path = os.path.join(working_dir, f"{file_id}.mp4")
        if not os.path.exists(file_path):
            try:
                self.logger.info(f"Attempting to download file: {file_id}")
                file = self.drive_client.CreateFile({'id' : file_id})
                file.GetContentFile(file_path)
                self.logger.debug(f"Successfully downloaded file to: {file_path}")
                return file_path
            except ApiRequestError:
                self.logger.error(f"Request error while downloading: {file_id}")
            except Exception as e:
                self.logger.error(f"Unhandled exception downloading: {file_id}: {e}")
        else:
            return file_path
            
    def _transcribe_file(self, file_path: str) -> str | list[Any]:
        """
        Converts audio/video to text
        """
        result = self.whisper_model.transcribe(file_path)
        self.logger.debug(f"Model output: {result['text']}")

        return result['text'] 

    def download_media(self, max_workers=2)-> list[str]:
        """
        Launches batch download using thread pool
        """
        TMP_DIR = "tmp/media"
        os.makedirs(TMP_DIR, exist_ok=True)

        self.logger.debug(f"Starting batch download for files: {self.file_ids}")
        output_list = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_dict = {
                executor.submit(self._download_file, TMP_DIR, file_id): file_id 
                for file_id in self.file_ids
            } # dict(Future, file_id)
            
            for future in as_completed(future_dict):
                file_id = future_dict[future]
                try:
                    result = future.result()
                    if result:
                        self.logger.info(f"Successfully downloaded {file_id}")
                        self.logger.debug(f"Result: {result}")
                        output_list.append(result)
                    else:
                        self.logger.warning(f"Download failed for {file_id}")
                except Exception as e:
                    self.logger.error(f"Error in thread for {file_id}: {e}")

        return output_list

    def process_media(self, file_path_list: list[str]):
        """
        Processes data based off strategy and pushes structured data to redis queue
        """
        strategy = LLMProcessingStrategy()
        for file_path in file_path_list:
            try:
                self.logger.info(f"Transcribing file: {file_path}")
                transcript = self._transcribe_file(file_path)
                structured_data = strategy.process(transcript)
                    
                serialized = json.dumps(structured_data)
                queue_name = RedisSettings.NOTION_QUEUE
                self.redis_client.rpush(queue_name, serialized)

                self.logger.info(f"Sent structured data to queue:{queue_name}")
                self.logger.debug(f"Payload sent: {serialized}")
            except Exception as e:
                self.logger.error(f"Unhandled exception while transcribing: {e}")

    def run(self):
        # entry point to download, process, and update
        self.logger.debug(f"Running processor for payload: {self.file_ids}")
        path_list = self.download_media(max_workers=len(self.file_ids))
        self.process_media(path_list)



def process_media_job(task_data: dict):
    file_ids = task_data['file_ids']
    processor = MediaProcessor(file_ids)
    processor.run()


if __name__ == "__main__":
    data = { "file_ids": ["1GlpbJ5wxjXynfzkADdtK867t_O-5yEZw",]}#"1Xt1o0W0sF-z_MUtfXi-e9i3qVuQ9lLBt","1LBG9wz9H1nQsinQSWcHKJFExPKmM_xzU"] }
    process_media_job(data)
