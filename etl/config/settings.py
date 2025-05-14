from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    REDIS_HOST= os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT= os.getenv("REDIS_PORT", "6379")
    REDIS_LIST_NAME = os.getenv("REDIS_LIST_NAME", "")
    
    TARGET_FOLDER = os.getenv("TARGET_FOLDER","")
settings = Settings()
