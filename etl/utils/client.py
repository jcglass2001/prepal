from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from config.settings import DRIVE_SETTINGS


def setup_drive_client():
    gauth = GoogleAuth(settings=DRIVE_SETTINGS)
    gauth.ServiceAuth()
    return GoogleDrive(gauth) 
