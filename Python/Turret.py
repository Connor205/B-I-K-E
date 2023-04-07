from Arduino import Arduino
from typing import *
from Enums import Seat


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
    
    def waitForConfirmation(self):
        # TODO: Blocking call to wait 
        self.logger.debug("Waiting for confirmation")

    def dealToSeat(self, seat: Seat):
        # TODO: Given a seat, deal a card to that seat
        raise NotImplementedError("dealToSeat is not implemented")
    
    def dealCommunityCards(self, cardsToDeal: int):
        # TODO: Deal the given number of community cards
        raise NotImplementedError("dealCommunityCards is not implemented")
    
    def dealDiscard(self, cardsToDiscard: int):
        # TODO: Discard the given number of cards
        raise NotImplementedError("dealDiscard is not implemented")