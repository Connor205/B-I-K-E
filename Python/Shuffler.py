from Arduino import Arduino
import logging
import time
import random


class Shuffler(Arduino):

    def __init__(self, port: str, baud=9600):
        super().__init__(port, baud)
        self.logger = logging.getLogger(__name__)

    def read_handler(self, command: str, value: str):
        if command == 'STATE':
            with self.stateLock:
                self.state = value
            self.logger.debug("Updated Arduino State to: {}".format(value))

    def moveToSlot(self, slot: int):
        self.sendCommand("MOVE", [slot])

    def dispense(self):
        self.sendCommand("DISPENSE")

    def putCard(self, slot: int):
        self.moveToSlot(slot)
        self.dispense()

    def shuffle(self):
        # generate a list of numbers 1 to 52 and then shuffle them
        # then we can just iterate through the list and put the cards in the slots
        # and then dispense them
        slots = list(range(1, 53))
        random.shuffle(slots)
        for slot in slots:
            self.putCard(slot)

        return slots

    def exportCards(self):
        self.sendCommand("EXPORT")

    def resetConveyor(self):
        self.sendCommand("RESET")
