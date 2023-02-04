from Card import Card
from Enums import Value, Suit

class Deck():
    """Class representing a Deck of Cards in poker"""
    cards: list[Card]

    def __init__(self) -> None:
        """Initializes an unshuffled deck of 52 cards"""
        for suit in Suit:
            for value in Value:
                newCard = Card(value, suit)
                self.cards.append(newCard)
    
    def shuffleDeck(self):
        """Shuffles this deck of cards"""
        self.cards.shuffle()

    def reorderDeck(self, newOrder: list[Card]):
        """Sets the order of this deck to the given deck"""
        if (len(newOrder) == 52):
            self.cards = newOrder
        # TODO Throw error/do nothing
