from abc import ABC, abstractmethod 
from utils.logging import setup_logger
import threading
 

class BaseWatcher(threading.Thread, ABC):
    def __init__(self, stop_event : threading.Event):
        super().__init__(name=self.__class__.__name__)
        self.stop_event = stop_event
        self.logger = setup_logger(__name__)
    @abstractmethod 
    def run(self):
        pass
