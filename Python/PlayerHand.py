from itertools import combinations
from collections import Counter
from Card import Card, Value, Suit
from Enums import HandRanking
from typing import Tuple

class PlayerHand():
    holeCards: list[Card]
    bestHand: list[Card]
    ranking: HandRanking

    def __init__(self, holeCards: list[Card] = []) -> None:
        self.holeCards = holeCards
        self.bestHand = []
        self.ranking = None

    def getRanking(self) -> HandRanking:
        return self.ranking
    
    def getBestHand(self) -> list[Card]:
        return self.bestHand
    
    def getHoleCards(self) -> list[Card]:
        return self.holeCards
    
    def addHoleCard(self, card: Card) -> bool:
        """
        Adds a card to the player's hand.
        Args:
            card (Card): Card to add to the player's hand.
        Returns:
            bool: True if the card was added, false if the player already has 2 cards.
        """
        if len(self.holeCards) >= 2:
            return False
        self.holeCards.append(card)
        return True
    
    def determineBestHand(self, communityCards: list[Card]) -> bool:
        """
        Given a list of cards, computes the best hand and its score.
        This method must be called with at least 3 community cards.
        Args:
            cards (list[Card]): List of cards to compute the best hand from.
        Returns:
            bool : True if the best hand has changed, false if not.
        """
        if len(communityCards) < 3:
            return False
        self.ranking, self.bestHand = self.score(communityCards)
        return True

    def score(self, communityCards: list[Card]) -> Tuple[HandRanking, list[Card]]:
        """
        Given a list of cards, computes the best hand and its score.
        This method must be called with at least 3 community cards.
        Args:
            cards (list[Card]): List of cards to compute the best hand from.
        Returns:
            Tuple[HandRanking, list[Card]]: Tuple containing the score and best hand.
        """
        cards = self.holeCards + communityCards

        max_score = HandRanking.HIGH_CARD
        best_hand = None
        
        for combination in combinations(cards, 5):
            # Compute the score and best hand for the current combination
            values = [card.value for card in combination]
            suits = [card.suit for card in combination]
            value_counts = Counter(values)
            flush = len(set(suits)) == 1
            straight = max(values) - min(values) == 4 and len(set(values)) == 5
            straight_flush = flush and straight
            royal_flush = straight_flush and max(values) == Value.ACE
            
            if royal_flush:
                score = HandRanking.ROYAL_FLUSH
                best_hand = combination
            elif straight_flush:
                score = HandRanking.STRAIGHT_FLUSH
                best_hand = combination
            elif value_counts.most_common(1)[0][1] == 4:
                score = HandRanking.FOUR_OF_A_KIND
                best_hand = combination
            elif value_counts.most_common(1)[0][1] == 3 and value_counts.most_common(2)[1][1] == 2:
                score = HandRanking.FULL_HOUSE
                best_hand = combination
            elif flush:
                score = HandRanking.FLUSH
                best_hand = combination
            elif straight:
                score = HandRanking.STRAIGHT
                best_hand = combination
            elif value_counts.most_common(1)[0][1] == 3:
                score = HandRanking.THREE_OF_A_KIND
                best_hand = combination
            elif value_counts.most_common(1)[0][1] == 2 and value_counts.most_common(2)[1][1] == 2:
                score = HandRanking.TWO_PAIR
                best_hand = combination
            elif value_counts.most_common(1)[0][1] == 2:
                score = HandRanking.PAIR
                best_hand = combination
            else:
                score = HandRanking.HIGH_CARD
                best_hand = combination
            
            # Update max_score and best_hand if necessary
            if score > max_score:
                max_score = score
                best_hand = combination
        
        return (max_score, best_hand)

if __name__ == "__main__":
    def testScore(cards, expected_score):
        hand = PlayerHand([])
        score, best_hand = hand.score(cards)
        print(score)
        if best_hand is None:
            print("No best hand")
            return
        for card in best_hand:
            print(str(card))
        assert score == expected_score, "Expected score: " + str(expected_score) + ", actual score: " + str(score)

    # Test cases
    # High card
    print("High card")
    cards = [Card(Value.TWO, Suit.HEART), Card(Value.THREE, Suit.SPADE), Card(Value.FIVE, Suit.CLUB), Card(Value.SEVEN, Suit.DIAMOND), Card(Value.ACE, Suit.HEART)]
    testScore(cards, HandRanking.HIGH_CARD)

    # One pair
    print("One pair")
    cards = [Card(Value.TWO, Suit.HEART), Card(Value.THREE, Suit.SPADE), Card(Value.TWO, Suit.CLUB), Card(Value.FIVE, Suit.DIAMOND), Card(Value.SIX, Suit.HEART)]
    testScore(cards, HandRanking.PAIR)

    # Two pair
    print("Two pair")
    cards = [Card(Value.TWO, Suit.HEART), Card(Value.THREE, Suit.SPADE), Card(Value.TWO, Suit.CLUB), Card(Value.THREE, Suit.DIAMOND), Card(Value.SIX, Suit.HEART)]
    testScore(cards, HandRanking.TWO_PAIR)

    # Three of a kind
    print("Three of a kind")
    cards = [Card(Value.TWO, Suit.HEART), Card(Value.THREE, Suit.SPADE), Card(Value.TWO, Suit.CLUB), Card(Value.TWO, Suit.DIAMOND), Card(Value.SIX, Suit.HEART)]
    testScore(cards, HandRanking.THREE_OF_A_KIND)

    # Straight
    print("Straight")
    cards = [Card(Value.TWO, Suit.HEART), Card(Value.THREE, Suit.SPADE), Card(Value.FOUR, Suit.CLUB), Card(Value.FIVE, Suit.DIAMOND), Card(Value.SIX, Suit.HEART)]
    testScore(cards, HandRanking.STRAIGHT)

    # Flush
    print("Flush")
    cards = [Card(Value.TWO, Suit.HEART), Card(Value.THREE, Suit.HEART), Card(Value.FIVE, Suit.HEART), Card(Value.SEVEN, Suit.HEART), Card(Value.ACE, Suit.HEART)]
    testScore(cards, HandRanking.FLUSH)

    # Full house
    print("Full house")
    cards = [Card(Value.TWO, Suit.HEART), Card(Value.THREE, Suit.SPADE), Card(Value.TWO, Suit.CLUB), Card(Value.THREE, Suit.DIAMOND), Card(Value.TWO, Suit.SPADE)]
    testScore(cards, HandRanking.FULL_HOUSE)

    # Four of a kind
    print("Four of a kind")
    cards = [Card(Value.TWO, Suit.HEART), Card(Value.THREE, Suit.SPADE), Card(Value.TWO, Suit.CLUB), Card(Value.TWO, Suit.DIAMOND), Card(Value.TWO, Suit.SPADE)]
    testScore(cards, HandRanking.FOUR_OF_A_KIND)

    # Straight flush
    print("Straight flush")
    cards = [Card(Value.TWO, Suit.HEART), Card(Value.THREE, Suit.HEART), Card(Value.FOUR, Suit.HEART), Card(Value.FIVE, Suit.HEART), Card(Value.SIX, Suit.HEART)]
    testScore(cards, HandRanking.STRAIGHT_FLUSH)

    # Royal flush
    print("Royal flush")
    cards = [Card(Value.TEN, Suit.HEART), Card(Value.JACK, Suit.HEART), Card(Value.QUEEN, Suit.HEART), Card(Value.KING, Suit.HEART), Card(Value.ACE, Suit.HEART)]
    testScore(cards, HandRanking.ROYAL_FLUSH)

    # > 5 cards
    print("> 5 cards")
    cards = [Card(Value.TWO, Suit.HEART), Card(Value.THREE, Suit.SPADE), Card(Value.FOUR, Suit.CLUB), Card(Value.FIVE, Suit.DIAMOND), Card(Value.SIX, Suit.HEART), Card(Value.SEVEN, Suit.HEART), Card(Value.EIGHT, Suit.HEART)]
    testScore(cards, HandRanking.STRAIGHT)

    # < 5 cards
    print("< 5 cards")
    cards = [Card(Value.TWO, Suit.HEART), Card(Value.THREE, Suit.SPADE), Card(Value.FOUR, Suit.CLUB), Card(Value.FIVE, Suit.DIAMOND)]
    testScore(cards, HandRanking.HIGH_CARD)

    # No cards
    print("No cards")
    cards = []
    testScore(cards, HandRanking.HIGH_CARD)
