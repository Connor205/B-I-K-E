from Enums import Value, Suit


class Card():
    """Class representing a playing card in poker."""
    value: Value = None
    suit: Suit = None

    def __init__(self, value: Value, suit: Suit) -> None:
        self.value = value
        self.suit = suit

    def isSameSuit(self, other: 'Card') -> bool:
        """Given another Card, determines if it is the same suit as this Card.

        Args:
            other (Card): Other Card to compare suit with.

        Returns:
            bool: True if they are the same suit, false if not.
        """
        return self.suit == other.suit

    def compareValue(self, other: 'Card') -> int:
        """Given another Card, compares the value of the Cards.

        Args:
            other (Card): Other Card to compare value with.

        Returns:
            int: Negative value if this Card is of lesser value.
            Positive value if this Card is of greater value.
            0 if the same Card value.
        """
        return self.value.compare(other.value)
    
    def isSameCard(self, other: 'Card') -> bool:
        """Given another Card, determines if it is the same card as this Card.

        Args:
            other (Card): Other Card to compare suit with.

        Returns:
            bool: True if they are the same card, false if not.
        """
        return self.value == other.value and self.suit == other.suit
    
    def __str__(self) -> str:
        return f"{str(self.value)} of {str(self.suit)}"
    

if __name__ == "__main__":
    card1 = Card(Value.ACE, Suit.HEART)
    card2 = Card(Value.ACE, Suit.HEART)
    card3 = Card(Value.FIVE, Suit.SPADE)
    assert card1.isSameCard(card2)
    assert card1.isSameSuit(card2)
    assert card1.compareValue(card2) == 0
    assert not card1.isSameCard(card3)
    assert not card1.isSameSuit(card3)
    assert card1.compareValue(card3) > 0
    print(card1)
    print(card2)
    print(card3)