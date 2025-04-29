from abc import ABC, abstractmethod
from typing import Any 
import httpx
from strategies.processing_strategy import ProcessingStrategy

class URLExtractor(ABC):
    def __init__(self, strategy: ProcessingStrategy) -> None:
        self.strategy = strategy

    @abstractmethod 
    def fetch_url_content(self, url:str) -> Any:
        pass 

    def extract(self, payload: dict) -> dict:
        url = payload['source']
        content = self.fetch_url_content(url)
        return self.strategy.process(content, media_type=payload['media_type']) # implement way to process content 

class WebsiteExtractor(URLExtractor):
    
    def __init__(self, strategy: ProcessingStrategy) -> None:
        super().__init__(strategy)

    def fetch_url_content(self, url: str) -> Any:
        html_content = httpx.get(url)
        return html_content.text # temporary implementation. may change

class VideoExtractor(URLExtractor):
    
    def __init__(self, strategy: ProcessingStrategy) -> None:
        super().__init__(strategy)

    def fetch_url_content(self, url: str) -> Any:
        return None # implement logic related to video data 
