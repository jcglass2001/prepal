import logging
import threading 
from .base import BaseWatcher

class WatcherManager:
    def __init__(self) -> None:
        self.watchers: list[BaseWatcher] = []
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    def start_watcher(self, watcher_cls) -> None:
        stop_event = threading.Event()
        watcher = watcher_cls(stop_event)        
        watcher.start()
        
        self.watchers.append(watcher)

    def stop_all(self):
        for watcher in self.watchers:
            watcher.stop_event.set()
            watcher.join()
        logging.info("All watchers stopped.")
        self.watchers.clear()
