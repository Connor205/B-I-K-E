from Arduino import Arduino
from typing import *


class Turret(Arduino):

    def __init__(self, port: str, baud=9600):
        super().__init__(port, baud)

    def read_handler(self, command: str, value: str):
        if command == 'STATE':
            with self.stateLock:
                self.state = value
            self.logger.debug("Updated Arduino State to: {}".format(value))

    def turn_to_angle(self, angle: int):
        self.sendCommand("TURN", values=[angle])

    def shoot_card(self, distance: int):
        self.sendCommand("FIRE", [distance])

    def activateFlywheel(self):
        self.sendCommand("flywheelOn")

    def deactivateFlywheel(self):
        self.sendCommand("flywheelOff")

    def activateIndexer(self):
        self.sendCommand("indexerOn")

    def deactivateIndexer(self):
        self.sendCommand("indexerOff")

    def return_cards(self):
        raise NotImplementedError("return_cards is not implemented")
