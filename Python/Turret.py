from Arduino import Arduino
from typing import *
from Enums import Seat
import time


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

    def waitForConfirmation(self):
        self.logger.debug("Waiting for confirmation")
        self.sendCommand("waitForConfirmation")
        time.sleep(0.25)
        self.waitForReady()

    def dealToSeat(self, seat: Seat):
        self.sendCommand("player", [seat.value])
        self.logger.debug("Dealing to seat: {}".format(seat))

    def dealRiver(self):
        self.logger.debug("Dealing river")
        self.sendCommand("river")

    def dealFlop(self):
        self.logger.debug("Dealing flop")
        self.sendCommand("flop")

    def dealTurn(self):
        self.logger.debug("Dealing turn")
        self.sendCommand("turn")

    def dealDiscard(self, cardsToDiscard: int):
        self.logger.debug("Dealing {} discard cards".format(cardsToDiscard))
        if cardsToDiscard > 3:
            self.sendCommand("eject")
            self.waitForReady()
        else:
            for i in range(cardsToDiscard):
                self.sendCommand("discard")
                time.sleep(0.25)
