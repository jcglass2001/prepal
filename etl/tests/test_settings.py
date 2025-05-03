import pytest
from config.settings import settings

def test_env_variables(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgres://test")
    monkeypatch.setenv("KAFKA_BROKER", "localhost:9092")

    assert settings.DATABASE_URL == "postgres://test"
    assert settings.KAFKA_BROKER == "localhost:9092"

def test_yaml_config_loading():
    assert isinstance(settings.ACCEPTED_MEDIA_TYPES, list)
    assert settings.LOG_LEVEL in ("INFO","DEBUG","WARNING","ERROR")
    assert isinstance(settings.USE_LLM, bool)


