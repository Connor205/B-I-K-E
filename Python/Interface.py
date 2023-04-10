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
        self.logger.info("Interface Initialized")
        self.buttonFunction = buttonFunction

    def read_handler(self, command: str, value: str):
        if not command == 'Button':
            self.logger.error("Unknown Command: {}".format(command))
            return

        # Panels are labeled 0-3 from left to right while facing the table (and screen)
        # 0 is the one closest to the shuffler, 3 is the one closest to the estop
        # Buttons are labels right to left (0 -> 7) for each panel
        # From 0->7 we have: Black, Red, Blue, White, Fold, Bet, Check, Call

        # Value is panel, buttonIndex
        panel, buttonIndex = value.split(',')
        self.logger.debug("Panel: {} | Button: {}".format(panel, buttonIndex))
        self.buttonFunction([buttonIndex, panel])
