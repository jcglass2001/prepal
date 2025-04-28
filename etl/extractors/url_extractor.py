from abc import ABC, abstractmethod 
import httpx

class URLExtractor(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod 
    def fetch_url_content(self, url:str) -> any:
        pass 

    def extract(self, payload: dict) -> dict:
        url = payload['source']
        content = self.fetch_url_content(url)
        return {} # implement way to process content 

class WebsiteExtractor(URLExtractor):
    def __init__(self) -> None:
        super().__init__()
    
    def fetch_url_content(self, url: str) -> any:
        html_content = httpx.get(url)
        return html_content.text # temporary implementation. may change

class VideoExtractor(URLExtractor):
    def __init__(self) -> None:
        super().__init__()

    def fetch_url_content(self, url: str) -> any:
        return None # implement logic related to video data 
