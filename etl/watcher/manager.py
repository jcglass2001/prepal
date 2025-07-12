import threading

from utils.logging import setup_logger 
from .base import BaseWatcher

class WatcherManager:
    def __init__(self) -> None:
        self.watchers: list[BaseWatcher] = []
        self.logger = setup_logger(__name__)

    def start_watcher(self, watcher_cls) -> None:
        stop_event = threading.Event()
        watcher: BaseWatcher = watcher_cls(stop_event)        
        watcher.start()
        
        self.watchers.append(watcher)
        self.logger.info(f"Started {watcher.__class__}...")

    def stop_all(self):
        for watcher in self.watchers:
            watcher.stop_event.set()
            watcher.join()
            self.logger.info(f"Stopped {watcher.__class__}...")
        self.logger.info(f"All watchers stopped. Clearing list...")
        self.watchers.clear()
