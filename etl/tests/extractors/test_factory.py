from typing import Type
import pytest
from extractors.factory import ExtractorFactory
from extractors.file_extractor import VideoFileExtractor
from extractors.url_extractor import VideoUrlExtractor, WebsiteExtractor
from strategies.processing_strategy import LLMProcessingStrategy, ManualProcessingStrategy


@pytest.mark.parametrize("media_type, expected_extractor_type", [
    ("website_url", WebsiteExtractor),
    ("video_url", VideoUrlExtractor),
    ("video_file", VideoFileExtractor), 
])
def test_extractor_factory_returns_correct_extractor(media_type: str, expected_extractor_type: Type):
    extractor = ExtractorFactory.get_extractor(media_type)
    
    # check extractor type
    assert isinstance(extractor, expected_extractor_type), f"Expected {expected_extractor_type}, got {type(extractor)}"

    # check for valid strategy
    assert hasattr(extractor, "strategy"), "Extractor has no strategy attribute"
    assert isinstance(extractor.strategy, (LLMProcessingStrategy, ManualProcessingStrategy)), "Invalid strategy type"

def test_extractor_factory_invalid_media_type():
    with pytest.raises(ValueError, match="Unknown media type: unsupported_media"):
        ExtractorFactory.get_extractor("unsupported_media")

