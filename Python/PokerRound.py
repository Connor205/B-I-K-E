from Deck import Deck
from Card import Card
from PlayerHand import PlayerHand
from Enums import GameState
from Player import Player

class PokerRound():
    potSize: int
    state: GameState
    hands: list[PlayerHand]
    communityCards: list[Card]
    deck: Deck
    playerIDs: list[int]
    turnIndex: int # keeps track of who's turn it is to bet
    currentPlayer: Player # keeps track of who's turn it is to bet
    betToMatch: int # the current bet to match

    def __init__(self) -> None:
        self.playerIDs = []
        self.potSize = 0
        # self.state = PREPARING
        self.hands = []
        self.communityCards = []
        self.deck = Deck()
        self.turnIndex = 0

    def getCommunityCards(self) -> list[Card]:
        return self.communityCards
