from Card import Card
from Enums import HandRanking

class PlayerHand():
    holeCards: list[Card]
    bestHand: list[Card]
    ranking: HandRanking

    def __init__(self, holeCards: list[Card]) -> None:
        self.holeCards = holeCards
        self.bestHand = []
        self.ranking = None

    def getHandRanking(self, communityCards: list[Card]) -> HandRanking:
        """Takes in the community cards and returns the ranking of the best 5 card hand"""
        if (self.ranking == None):
            allCards = self.holeCards.append(communityCards)
            bestFive = self.getBestFiveCards(allCards)
            self.bestHand = bestFive
            self.ranking = HandRanking.getRanking(self.bestHand)
        return self.ranking
    
    def getBestFiveCards(self, availableCards: list[Card]) -> list[Card]:
        """Get the best five card hand given the total cards available"""
        # TODO
        return []
