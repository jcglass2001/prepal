import logging
from watcher.drive_watcher import DriveWatcher
def main():
    print("ETL entry-point")
    
    drive_watcher = DriveWatcher()
    drive_watcher.run()


if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")
    main()
