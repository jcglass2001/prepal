# Standard library imports
import os
import json
from typing import Any, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

# Third part library imports
import whisper
from pydrive2.files import ApiRequestError
# from redis import Redis


# Custom moudle imports
from config.settings import AppSettings, RedisSettings
from processor.strategy import LLMProcessingStrategy
from utils.client import setup_drive_client, setup_redis_client
from utils.logging import setup_logger


class MediaProcessor:
    def __init__(
        self,
        file_ids: list[str],
        drive_client,
        redis_client,
        whisper_model,
        output_queue,
    ):
        self.file_ids = file_ids
        self.drive_client = drive_client
        self.redis_client = redis_client
        self.whisper_model = whisper_model
        self.output_queue = output_queue
        self.logger = setup_logger(self.__class__.__name__)

    def _download_file(self, working_dir: str, file_id: str) -> Tuple[str, bool]:
        """
        Queries API for file download based on file_id and returns path of downloaded file
        """

        self.logger.debug(f"Working directory: {working_dir}\t File ID: {file_id}")

        file_path = os.path.join(working_dir, f"{file_id}.mp4")
        if not os.path.exists(file_path):
            try:
                self.logger.info(f"Downloading file: {file_id}")
                file = self.drive_client.CreateFile({"id": file_id})
                file.GetContentFile(file_path)
                self.logger.debug(f"Successfully downloaded file to: {file_path}")
                return file_path, True
            except ApiRequestError:
                self.logger.error(f"Request error while downloading: {file_id}")
                return file_path, False
            except Exception as e:
                self.logger.error(f"Unhandled exception downloading: {file_id}: {e}")
                raise
        else:
            self.logger.info("File exists...")  # TODO: better log message
            return file_path, True

    def _transcribe_file(self, file_path: str) -> Tuple[str, str, str | None]:
        """
        Converts audio/video to text
        """
        try:
            self.logger.info(f"Transcribing file: {file_path} ...")
            output = self.whisper_model.transcribe(file_path)["text"]

            if len(output) == 0:
                return file_path, output, "Model returned empty transcription"
            if len(output) < 20:  # TODO: refactor hardcoded validation
                return file_path, output, "Possible malfomed transcription"

            self.logger.debug(f"Transcription: \n***\n{output}\n***")
            return file_path, output, None
        except Exception as e:
            self.logger.error(f"Error transcribing file: {e}")
            raise

    def download_media(self, worker_size=2) -> Tuple[list, list]:
        """
        Launches batch download using thread pool. Returns tuple containing lists of successful and failed downloads.
        """
        TMP_DIR = "tmp/media"
        os.makedirs(TMP_DIR, exist_ok=True)

        self.logger.debug(f"Starting batch download for files: {self.file_ids}")
        succeeded, failed = [], []
        with ThreadPoolExecutor(
            max_workers=min(len(self.file_ids), worker_size)
        ) as executor:
            future_dict = {
                executor.submit(self._download_file, TMP_DIR, file_id): file_id
                for file_id in self.file_ids
            }  # dict(Future, file_id)

            for future in as_completed(future_dict):
                file_id = future_dict[future]
                try:
                    result, isDownloaded = future.result()
                    if isDownloaded:
                        self.logger.info(f"Successfully downloaded {file_id}")
                        self.logger.debug(f"Result: {result}")
                        succeeded.append(result)
                    else:
                        self.logger.warning(f"Download failed for {file_id}")
                        failed.append(result)
                except Exception as e:
                    self.logger.error(f"Error in thread for {file_id}: {e}")

        return succeeded, failed

    def transcribe(self, file_path_list: list[str]) -> Tuple[list, list]:
        result_list = [self._transcribe_file(file) for file in file_path_list]
        successful = [
            (file_path, output)
            for file_path, output, reason in result_list
            if reason is None
        ]
        failed = [
            (file_path, output, reason)
            for file_path, output, reason in result_list
            if reason is not None
        ]

        return successful, failed

    def process(self, transcript_list: list[Tuple]):
        """
        Processes data based off strategy and pushes structured data to redis queue
        """
        strategy = LLMProcessingStrategy()
        results = {}

        for file_path, transcript in transcript_list:
            try:
                self.logger.info(f"Proccessing transcript of media file {file_path}...")
                structured_data = strategy.process(transcript)
                serialized = json.dumps(structured_data)
                results[file_path] = serialized

            except Exception as e:
                self.logger.error(f"Unhandled exception while processing: {e}")
                raise

        return results

    def run(self):
        """
        Orchestrates download, transcription, processing, queueing, and cleanup
        """
        self.logger.info("Running processor...")
        succeeded_paths, failed_paths = self.download_media()
        valid_transcripts, invalid_transcripts = self.transcribe(succeeded_paths)
        path_data_pair = self.process(valid_transcripts)

        self.redis_client.rpush(self.output_queue, json.dumps(path_data_pair))

        # TODO: handle failed downloads.
        # TODO: handle failed transcriptions. (Write to file for review)
        # TODO: handle cleanup


def process_media_job(task_data: dict):
    """RQ Job function to start media processing."""
    file_ids = task_data["file_ids"]

    drive_client = setup_drive_client()
    redis_client = setup_redis_client()
    whisper_model = whisper.load_model(AppSettings.WHISPER_MODEL)
    egress = RedisSettings.NOTION_QUEUE

    processor = MediaProcessor(
        file_ids, drive_client, redis_client, whisper_model, egress
    )
    processor.run()


if __name__ == "__main__":
    data = {
        "file_ids": [
            "1GlpbJ5wxjXynfzkADdtK867t_O-5yEZw",
            "1Xt1o0W0sF-z_MUtfXi-e9i3qVuQ9lLBt",
            "1LBG9wz9H1nQsinQSWcHKJFExPKmM_xzU",
        ]
    }
    process_media_job(data)
