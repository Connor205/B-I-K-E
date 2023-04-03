from Arduino import Arduino
import logging
import time

# Arduino Nano that handles the button panel inputs
class Interface(Arduino):

    def __init__(self, port: str, baud=115200):
        super().__init__(port, baud)
        self.logger = logging.getLogger(__name__)

    def read_handler(self, command: str, value: str):
        if command == 'STATE':
            with self.stateLock:
                self.state = value
            self.logger.debug("Updated Arduino State to: {}".format(value))