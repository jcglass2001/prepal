
from abc import ABC, abstractmethod
from typing import Any
from strategies.processing_strategy import ProcessingStrategy


class FileExtractor(ABC):
    def __init__(self, strategy: ProcessingStrategy) -> None:
        self.strategy = strategy

    @abstractmethod 
    def fetch_file_content(self, filepath: str) -> Any: 
        pass 

    def extract(self, payload: dict) -> dict: 
        filepath = payload['source']
        content = self.fetch_file_content(filepath)
        return self.strategy.process(content, payload['media_type']) # implement way to process file content 

class VideoFileExtractor(FileExtractor):
    
    def __init__(self, strategy: ProcessingStrategy) -> None:
        super().__init__(strategy)
    def fetch_file_content(self, filepath: str) -> Any:
        return None # implement later
