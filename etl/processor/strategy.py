# Standard library imports
from abc import ABC, abstractmethod
import json
import re

# Third-party imports
import ollama

# Custom imports
from config.settings import LLMSettings
from utils.logging import setup_logger


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

        Provide ingredients without brand names or unnecessary information. 

        Return response in valid JSON format.

        Transcript: {transcript}
        """
        try:
            self.logger.info("Sending payload...")
            output = ollama.generate(model=self.model, prompt=prompt)
            self.logger.info("Response received.")

            raw = output["response"].strip()
            cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw)

            parsed = json.loads(cleaned)
            self.logger.debug(f"Model output: \n\n{json.dumps(parsed, indent=2)}\n")

            return parsed
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON response: {e}")
            self.logger.debug(f"Raw content: \n\n{output['response']}\n")
            raise
        except Exception as e:
            self.logger.error(f"Unhandled error calling LLM: {e}")
            raise


# TODO create custom processing strategy
