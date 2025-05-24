from abc import ABC, abstractmethod
import json

from utils.logging import setup_logger
from config.settings import app_config
import requests

class BaseStrategy(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.logger = setup_logger(self.__class__.__name__)

    @abstractmethod 
    def process(self, transcript: str):
        """
        Processes a transcript and returns structured data
        """
        pass

class LLMProcessingStrategy(BaseStrategy):
    def __init__(self) -> None:
        super().__init__()
        self.llm_provider = app_config.LLM_PROVIDER
        self.llm_model = app_config.LLM_MODEL
        self.llm_host = app_config.LLM_HOST 

    def process(self, transcript: str):
        """
        Offloads transcript processing to hosted LLM service
        """
        prompt = f"""
        Given the following transcript of a recipe video, extract:

        - Recipe Title
        - Ingredients (as a list)
        - Instructions (as a step-by-step list)

        Output as JSON.

        Transcript: {transcript}
        """
        try:
            self.logger.info("Sending payload...")
            response = requests.post(
                f"{self.llm_host}/api/generate",
                json={
                    "model": self.llm_model, 
                    "prompt": prompt,
                    "stream": False 
                } 
            )
            try:
                data = response.json()
                content = data.get("response","")
                parsed = json.loads(content)
                self.logger.debug(f"Parsed response: {parsed}")
            except json.JSONDecodeError as e:
                self.logger.error(f"Invalid JSON response: {e}")
                self.logger.debug(f"Raw content: {response.text}")
        except requests.RequestException as e:
            self.logger.error(f"Error in making request to service: {e}")

