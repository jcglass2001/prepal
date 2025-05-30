from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from redis import Redis
from rq import Queue
from config.settings import DriveSettings, RedisSettings

def setup_drive_client() -> GoogleDrive:
    gauth = GoogleAuth(settings=DriveSettings.CLIENT_SETTINGS)
    gauth.ServiceAuth()
    return GoogleDrive(gauth) 

def setup_redis_client(queue_name: str) -> Queue:
    redis_conn = Redis(host=RedisSettings.HOST, port=RedisSettings.PORT)
    queue = Queue(name=queue_name, connection=redis_conn)
    return queue
