
from abc import ABC, abstractmethod
from config.settings import LLM_MODEL, LLM_HOST
import logging
import requests

class ProcessingStrategy(ABC):
    @abstractmethod 
    def process(self, content, media_type: str) -> dict:
        """
        Processes the extracted content depending on media_type.
        """
        pass 

class LLMProcessingStrategy(ProcessingStrategy):
    def __init__(self) -> None:
        self.llm_url = LLM_HOST
        self.llm_model = LLM_MODEL

    def process(self, content, media_type: str) -> dict:
        if media_type == "website_url":
            logging.info("LLM processing website content...")
            # implement processing logic
            return {}
        elif media_type == "video_url":
            logging.info("LLM processing video transcript...")
            # implement processing logic
            return {}
        elif media_type == "video_file":
            logging.info("LLM processing extracted audio/text from file...")
            # implement processing logic
            return {}
        else:
            raise ValueError(f"Unsupported media type for LLM strategy: {media_type}")


class ManualProcessingStrategy(ProcessingStrategy):
    
    def process(self, content, media_type: str) -> dict:
        if media_type == "website_url":
            logging.info("Custom processing website content...")
            # implement processing logic
            return {}
        elif media_type == "video_url":
            logging.info("Manually processing video transcript...")
            # implement logic
            return {}
        elif media_type == "video_file":
            logging.info("Manually processing extracted audio/text from file...")
            # implement logic 
            return {}
        else:
            raise ValueError(f"Unsupported media type for Manual strategy: {media_type}")

