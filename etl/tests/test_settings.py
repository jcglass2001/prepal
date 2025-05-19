def test_settings_load():
    from .config.settings import app_config

    assert app_config.REDIS_HOST
    assert app_config.REDIS_PORT
    assert app_config.REDIS_LIST_NAME

    assert app_config.TARGET_FOLDER
    assert app_config.POLLING_INTERVAL

    assert app_config.LOG_LEVEL
