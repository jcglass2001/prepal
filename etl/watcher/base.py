from abc import ABC, abstractmethod 
import threading
import logging 

class BaseWatcher(threading.Thread, ABC):
    def __init__(self, stop_event : threading.Event):
        super().__init__(name=self.__class__.__name__)
        self.stop_event = stop_event
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    @abstractmethod 
    def run(self):
        pass
