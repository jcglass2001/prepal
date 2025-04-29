from .file_extractor import FileExtractor, VideoFileExtractor
from .url_extractor import URLExtractor, VideoExtractor, WebsiteExtractor
from config.settings import USE_LLM
from strategies.processing_strategy import LLMProcessingStrategy, ManualProcessingStrategy, ProcessingStrategy

class ExtractorFactory:
    @staticmethod
    def get_extractor(media_type: str) -> URLExtractor | FileExtractor:
        """
        Returns an extractor instance based on the media type.
        """

        strategy = ExtractorFactory._get_strategy()

        if media_type == "website_url":
            return WebsiteExtractor(strategy=strategy)
        elif media_type == "video_url":
            return VideoExtractor(strategy=strategy)
        elif media_type == "video_file":
            return VideoFileExtractor(strategy=strategy)
        else:
            raise ValueError(f"Unknown media type: {media_type}")

    @staticmethod
    def _get_strategy() -> ProcessingStrategy: 
        if USE_LLM:
            return LLMProcessingStrategy()
        else:
            return ManualProcessingStrategy()
