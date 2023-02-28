from enum import Enum


class Seat(Enum):
    """An Enum representing a seat number at the poker table."""
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4

    def compare(self, other: 'Seat') -> int:
        """Compares another Seat with this Seat.

        Args:
            other (Seat): Other Seat to compare

        Returns:
            int: Negative value if this Seat is of lesser value.
            Positive value if this Seat is of greater value.
            0 if the same Seat value.
        """
        return self.value - other.value


class Suit(Enum):
    """An Enum representing a card suit."""
    HEART = 1
    SPADE = 2
    CLUB = 3
    DIAMOND = 4

    def compare(self, other: 'Suit') -> int:
        """Compares another Suit with this Suit.

        Args:
            other (Suit): Other Suit to compare

        Returns:
            int: Negative value if this Suit is of lesser value.
            Positive value if this Suit is of greater value.
            0 if the same Suit value.
        """
        return self.value - other.value


class Value(Enum):
    """An Enum representing a card value."""
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

    def compare(self, other: 'Value') -> int:
        """Compares another Value with this Value.

        Args:
            other (Value): Other Value to compare.

        Returns:
            int: Negative value if this Value is of lesser value.
            Positive value if this Value is of greater value.
            0 if the same Value value.
        """
        return self.value - other.value

class HandRanking(Enum):
    """An Enum representing poker hand rankings."""
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10

    def compare(self, other: 'HandRanking') -> int:
        """Compares another HandRanking with this HandRanking.

        Args:
            other (HandRanking): Other HandRanking to compare.

        Returns:
            int: Negative value if this HandRanking is of lesser value.
            Positive value if this HandRanking is of greater value.
            0 if the same HandRanking value.
        """
        return self.value - other.value


class GameState(Enum):
    """An Enum representing the states of a poker game."""
    PREPARING = 1
    PREFLOP = 2
    FLOP = 3
    TURN = 4
    RIVER = 5
    SHOWDOWN = 6

class Button(Enum):
    """An Enum representing the buttons the players have access to."""
    FOLD = 1
    CHECK = 2
    CALL = 3
    BET = 4
    WHITE_CHIP = 5
    BLUE_CHIP = 6
    RED_CHIP = 7
    SETTINGS = 8

