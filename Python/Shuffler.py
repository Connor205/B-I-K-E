from Arduino import Arduino
import logging
import time
import random
import cv2
from Card import Card, Value, Suit
import pickle


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
        self.sendCommand("move", [slot])

    def dispense(self):
        self.sendCommand("dispense")

    def putCard(self, slot: int):
        self.moveToSlot(slot)
        self.dispense()

    def exportCards(self):
        self.sendCommand("export")

    def resetConveyor(self):
        self.sendCommand("reset")

    def waitForConfirm(self):
        self.sendCommand("wait")
        time.sleep(0.25)
        self.waitForReady()


def classify_card(image) -> Card:
    return Card(Value.ACE, Suit.HEART)


def main():
    logging.basicConfig(level=logging.DEBUG)
    # Get the port from the user
    port = input("Enter the port for the shuffler: ")
    shuffler = Shuffler(port)

    # Start video capture
    cap = cv2.VideoCapture(0)

    while (True):
        shuffler.waitForConfirm()
        shuffler.logger.debug("Shuffling")
        # Generate a list of slots to put the cards in, 1-> 52
        slots = list(range(1, 53))
        # Shuffle the list
        random.shuffle(slots)
        # Create a blank list of 52 cards
        cards = [None] * 52
        # now for each slot in the list, put a card in it
        for i, slot in enumerate(slots):
            shuffler.logger.debug("Putting card {} in slot {}".format(i, slot))
            # First we want to take a photo and identify the card
            # Read the image from the camera
            ret, frame = cap.read()
            # Convert the image to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            identified_card = classify_card(gray)
            cards[slot] = identified_card
            # Now we want to put the card in the slot
            shuffler.putCard(slot)
            time.sleep(0.25)
            # Wait for the shuffler to be ready
            shuffler.waitForReady()

        # Now we want to export the cards
        shuffler.exportCards()

        # Now we want to reset the conveyor
        shuffler.resetConveyor()

        # Now lets save the list of cards to a file using pickle
        with open("cards.txt", "w") as f:
            f.write(pickle.dumps(cards))