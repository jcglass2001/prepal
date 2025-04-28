
from abc import ABC, abstractmethod


class FileExtractor(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod 
    def fetch_file_content(self, filepath: str) -> any: 
        pass 

    def extract(self, payload: dict) -> dict: 
        filepath = payload['source']
        content = self.fetch_file_content(filepath)
        return {} # implement way to process file content 

class VideoFileExtractor(FileExtractor):
    def fetch_file_content(self, filepath: str) -> any:
        return None # implement later
