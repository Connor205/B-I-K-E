import logging
import sys
import random
from Card import Card
from Enums import Value, Suit

class Deck():
    """Class representing a Deck of Cards in poker"""
    logger: logging.Logger
    cards: list[Card]
    topCardIdx: int

    def __init__(self) -> None:
        """Initializes an unshuffled deck of 52 cards"""
        # init the logger
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.StreamHandler(sys.stdout))

        self.cards = []
        for suit in Suit:
            for value in Value:
                newCard = Card(value, suit)
                self.cards.append(newCard)
        self.topCardIdx = 0

    def getDeck(self) -> list[Card]:
        """Returns the deck"""
        return self.cards
    
    def shuffleDeck(self) -> None:
        """Shuffles this deck of cards"""
        random.shuffle(self.cards)

    def reorderDeck(self, newOrder: list[Card]) -> None:
        """Sets the order of this deck to the given deck"""
        if (len(newOrder) != 52):
            self.logger.error("Tried to reorder deck with incorrect number of cards")
            return
        self.cards = newOrder
    
    def drawCard(self) -> Card:
        """Draws a card from the top of the deck"""
        if (self.topCardIdx < 0 or self.topCardIdx > 52):
            self.logger.error("Tried to draw card from invalid position")
            return None
        card = self.cards[self.topCardIdx]
        self.topCardIdx += 1
        return card
    

if __name__ == "__main__":
    deck = Deck()
    cards = deck.getDeck()
    print("Number of cards in deck: ", len(cards))
    for card in cards:
        print(str(card))
    
    print("Shuffling deck")
    deck.shuffleDeck()
    cards = deck.getDeck()
    print("Number of cards in deck: ", len(cards))
    for card in cards:
        print(str(card))

    print("Drawing 5 cards")
    for i in range(5):
        card = deck.drawCard()
        print("Card drawn: ", str(card))

