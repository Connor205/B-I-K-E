from Arduino import Arduino
import logging
import time
import random
import cv2
from Card import Card, Value, Suit
import pickle
import tensorflow as tf
import numpy as np


class Shuffler(Arduino):

    def __init__(self, port: str, baud=9600):
        super().__init__(port, baud)

    def read_handler(self, command: str, value: str):
        if command == 'STATE':
            with self.stateLock:
                self.state = value

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


def convert_suit_string(suit: str) -> Suit:
    if suit == "hearts":
        return Suit.HEART
    elif suit == "clubs":
        return Suit.CLUB
    elif suit == "diamonds":
        return Suit.DIAMOND
    elif suit == "spades":
        return Suit.SPADE
    else:
        raise ValueError("Invalid suit string")


def convert_value_string(value: str) -> Value:
    if value == "ace":
        return Value.ACE
    elif value == "2":
        return Value.TWO
    elif value == "3":
        return Value.THREE
    elif value == "4":
        return Value.FOUR
    elif value == "5":
        return Value.FIVE
    elif value == "6":
        return Value.SIX
    elif value == "7":
        return Value.SEVEN
    elif value == "8":
        return Value.EIGHT
    elif value == "9":
        return Value.NINE
    elif value == "10":
        return Value.TEN
    elif value == "jack":
        return Value.JACK
    elif value == "queen":
        return Value.QUEEN
    elif value == "king":
        return Value.KING
    else:
        raise ValueError("Invalid value string")


# Lets load the models
suit_model = tf.keras.models.load_model("suit_model.h5")
suit_classes = ['clubs', 'diamonds', 'hearts', 'spades']
value_model = tf.keras.models.load_model("val_model.h5")
value_classes = [
    '10', '2', '3', '4', '5', '6', '7', '8', '9', 'ace', 'jack', 'king',
    'queen'
]


def classify_card(frame) -> Card:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # rotate the image 15 degrees counter clockwise
    image_center = tuple(np.array(frame.shape[1::-1]) / 2)

    rot_mat = cv2.getRotationMatrix2D(image_center, -15 - 90, 1.0)
    result = cv2.warpAffine(gray,
                            rot_mat,
                            frame.shape[1::-1],
                            flags=cv2.INTER_LINEAR)

    # Crop the image
    cropped_number = result[100:475, 750:1050]

    # resize to 100 by 100
    cropped_number = cv2.resize(cropped_number, (100, 100))

    cropped_suit = result[450:725, 750:1000]

    # resize to 100 by 100
    cropped_suit = cv2.resize(cropped_suit, (100, 100))

    # Now lets classify the card
    # First lets classify the suit
    suit = suit_model.predict(cropped_suit.reshape(1, 100, 100, 1))
    suit_index = np.argmax(suit)
    suit = suit_classes[suit_index]
    suit = convert_suit_string(suit)

    # Now lets classify the value
    value = value_model.predict(cropped_number.reshape(1, 100, 100, 1))
    value_index = np.argmax(value)
    value = value_classes[value_index]
    value = convert_value_string(value)

    accuracy = np.max(suit) * np.max(value)

    ret = Card(value, suit)

    cv2.imshow("Number", cropped_number)
    cv2.imshow("Suit", cropped_suit)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return ret, accuracy


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
        # Create a blank list of 52 cards
        cards = [None] * 52
        # now for each slot in the list, put a card in it
        for i in range(52):
            # First we want to take a photo and identify the card
            # Read the image from the camera
            ret, frame = cap.read()
            # Convert the image to grayscale
            identified_card, confidence = classify_card(frame)
            shuffler.logger.debug(
                "Identified card: {} with confidence: {}".format(
                    identified_card, confidence))
            if confidence < 0.9:
                # put the card as far back as possible
                slot = 51
                while cards[slot] is not None:
                    slot -= 1
            else:
                # Randomly select a slot of the remaining slots
                possible_slots = [i for i, x in enumerate(cards) if x is None]
                slot = random.choice(possible_slots)
            cards[slot] = identified_card
            # Now we want to put the card in the slot
            shuffler.dispense()
            time.sleep(0.25)
            # Wait for the shuffler to be ready
            shuffler.waitForReady()
            # Wait for enter
            input("Press enter to continue")

        # Now we want to export the cards
        # shuffler.exportCards()

        # Now we want to reset the conveyor
        # shuffler.resetConveyor()

        # Now lets save the list of cards to a file using pickle
        with open("cards.txt", "w") as f:
            f.write(pickle.dumps(cards))


if __name__ == "__main__":
    main()