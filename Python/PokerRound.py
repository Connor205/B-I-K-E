from Deck import Deck
from Card import Card
from PlayerHand import PlayerHand
from Enums import GameState
from Player import Player

class PokerRound():
    potSize: int
    state: GameState
    communityCards: list[Card]
    deck: Deck
    players: list[Player]
    turnIndex: int # keeps track of who's turn it is to bet
    currentPlayer: Player # keeps track of who's turn it is to bet
    betToMatch: int # the current bet to match

    def __init__(self) -> None:
        self.playerIDs = []
        self.potSize = 0
        self.state = GameState.PREPARING
        self.communityCards = []
        self.deck = Deck()
        self.turnIndex = 0
        self.betToMatch = 0

    def playerFolds(self) -> bool:
        origSize = len(self.players)
        self.players.remove(self.currentPlayer)
        return len(self.players) == origSize - 1
    
    def startRound(self) -> bool:
        allReady = True
        for player in self.players:
            allReady = allReady and player.isReady
        if allReady:
            self.state = GameState.PREFLOP
            self.currentPlayer = self.players[self.turnIndex]


    def getCommunityCards(self) -> list[Card]:
        return self.communityCards
