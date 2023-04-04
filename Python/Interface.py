from Arduino import Arduino
import logging
import time
from typing import Callable


# Arduino Nano that handles the button panel inputs
class Interface(Arduino):

    def __init__(self,
                 port: str,
                 buttonFunction: Callable = None,
                 baud=115200):
        super().__init__(port, baud)
        self.logger = logging.getLogger(__name__)
        self.buttonFunction = buttonFunction

    def read_handler(self, command: str, value: str):
        if not command == 'Button':
            self.logger.error("Unknown Command: {}".format(command))
            return

        # Value is panel, buttonIndex
        panel, buttonIndex = value.split(',')
        self.logger.debug("Panel: {} | Button: {}".format(panel, buttonIndex))
        self.buttonFunction([buttonIndex, panel])
