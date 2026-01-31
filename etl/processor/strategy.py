# Standard library imports
from abc import ABC, abstractmethod
import json
import re

# Third-party imports
from jsonschema import ValidationError, exceptions
import ollama

# Custom imports
from config.settings import LLMSettings
from utils.logging import setup_logger
from utils.validate import validate_json


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

        self.logger.info("Initialized LLM processing...")

    def process(self, transcript: str):
        """
        Offloads transcript processing to hosted LLM service
        """

        prompt = f"""
        Given the following transcript of a recipe video, extract:

        - recipe_title: string
        - ingredients: list
        - instructions: list

        Provide ingredients without brand names or unnecessary information. 

        Return response in valid JSON format.

        Transcript: {transcript}
        """
        try:
            self.logger.info("Sending payload to Ollama service...")
            output = ollama.generate(model=self.model, prompt=prompt)

            raw = output["response"].strip()
            cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw)

            parsed = json.loads(cleaned)
            validate_json(parsed)

            self.logger.debug(f"Model output: \n\n{json.dumps(parsed, indent=2)}\n")

            return parsed
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON response: {e}")
            self.logger.debug(f"Raw content: \n\n{output['response']}\n")
            raise
        except exceptions.ValidationError as e:
            self.logger.error(f"Schema validation failed: {e.message}")
            self.logger.debug(f"Invalid payload: \n{json.dumps(parsed, indent=2)}")
            raise
        except Exception as e:
            self.logger.error(f"Unhandled error calling LLM: {e}")
            raise


# TODO: implement alternate/manual processing strategy


class CustomProcessingStrategy(BaseStrategy):
    def __init__(self) -> None:
        super().__init__()
        self.logger.info("Initialized custom processing...")

    def process(self, transcript: str):
        pass
