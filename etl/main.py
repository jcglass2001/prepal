import logging
import signal
import sys
from watcher.drive_watcher import DriveWatcher
from watcher.manager import WatcherManager



def main():
    manager = WatcherManager()

    def shutdown_handler(signum, frame):
        logging.info(f"Received shutdown signal ({signum}). Stopping watchers...")
        manager.stop_all()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)


    manager.start_watcher(DriveWatcher)
    # manager.start_watcher(...)
    logging.info("All watchers running...")
    
    signal.pause()
             


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
