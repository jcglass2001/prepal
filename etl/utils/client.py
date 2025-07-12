from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from redis import Redis
from rq import Queue
from config.settings import DriveSettings, RedisSettings

def setup_drive_client() -> GoogleDrive:
    """Creates GoogleDrive instance"""
    gauth = GoogleAuth(settings=DriveSettings.CLIENT_SETTINGS)
    gauth.ServiceAuth()
    return GoogleDrive(gauth) 

def setup_redis_client() -> Redis:
    """Creates Redis connection"""
    return Redis(host=RedisSettings.HOST, port=RedisSettings.PORT)

def setup_rq(queue_name: str) -> Queue:
    """Creates Redis connection and returns rq Queue object"""
    redis_conn = Redis(host=RedisSettings.HOST, port=RedisSettings.PORT)
    queue = Queue(name=queue_name, connection=redis_conn)
    return queue
