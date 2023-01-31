import Deck
import Card
import PlayerHand
from Enums import GameState

class PokerRound():
    potSize: int
    state: GameState
    hands: list[PlayerHand]
    communityCards: list[Card]
    deck: Deck
    playerIDs: list[int]

    def __init__(self) -> None:
        self.playerIDs = []
        self.potSize = 0
        # self.state = PREPARING
        self.hands = []
        self.communityCards = []
        self.deck = Deck()

    


