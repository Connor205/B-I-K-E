from Card import Card

class Deck():
    """Class representing a Deck of Cards in poker"""
    cards: Card = []

    def __init__(self) -> None:
        """Initializes an unshuffled deck of 52 cards"""
        for suit in suit:
            for value in value:
                newCard = Card(value, suit)
                self.cards.append(newCard)
    
    def shuffleDeck(self):
        """Shuffles this deck of cards"""
        self.cards.shuffle()

    def reorderDeck(self, newOrder: Card[52]):
        """Sets the order of this deck to the given deck"""
        self.cards = newOrder
