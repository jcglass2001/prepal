from abc import ABC, abstractmethod
import json

from utils.logging import setup_logger
from config.settings import LLMSettings
import ollama

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
        self.provider = LLMSettings.PROVIDER
        self.model = LLMSettings.MODEL
        self.host = LLMSettings.HOST 

    def process(self, transcript: str):
        """
        Offloads transcript processing to hosted LLM service
        """
        prompt = f"""
        Given the following transcript of a recipe video, extract:

        - Recipe Title
        - Ingredients: list
        - Instructions: list

        Output as JSON. Avoid brand names.

        Transcript: {transcript}
        """
        try:
            self.logger.info("Sending payload...")
            response = ollama.generate(model=self.model, prompt=prompt)
            self.logger.info("Response received.")

            parsed = json.loads(response['response'])
            self.logger.debug(f"Parsed response: {json.dumps(parsed)}")

            return parsed
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON response: {e}")
            self.logger.debug(f"Raw content: {response}")
            return None 
        except Exception as e:
            self.logger.error(f"Unhandled error calling LLM: {e}")
            return None
