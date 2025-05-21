import signal
import sys
from config.settings import app_config
from utils.logging import setup_logger
from watcher.drive import DriveWatcher
from watcher.manager import WatcherManager



def main():
    manager = WatcherManager()
    logger = setup_logger(__name__)

    def shutdown_handler(signum, frame):
        logger.warning(f"Received shutdown signal ({signum}). Stopping watchers...")
        manager.stop_all()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)


    manager.start_watcher(DriveWatcher)
    # manager.start_watcher(...)
    logger.info("All watchers running...")
    
    signal.pause()
             


if __name__ == "__main__":
    main()
