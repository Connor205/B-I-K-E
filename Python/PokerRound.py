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
    startIndex: int # keeps track of who's starts betting each round
    currentPlayer: Player # keeps track of who's turn it is to bet
    betToMatch: int # the current bet to match
    overallPlayers: list[Player] # Tracking the players between hands

    def __init__(self, players) -> None:
        self.players = []
        self.potSize = 0
        self.state = GameState.PREPARING
        self.deck = Deck()
        self.communityCards = []
        self.turnIndex = 0
        self.startIndex = 0
        self.betToMatch = 0
        self.currentPlayer = None

    def playerFolds(self) -> bool:
        origSize = len(self.players)
        self.players.remove(self.currentPlayer)
        self.currentPlayer = self.players[(self.turnIndex + 1) % len(self.players)]
        if self.startIndex > self.turnIndex:
            self.startIndex -= 1
        if self.checkAllMatched():
            self.advanceRound()
        return len(self.players) == origSize - 1
    
    def makeBet(self, player) -> bool:
        playerBet = player.potentialBet
        if player.makeBet():
            self.potSize += playerBet
            if player.commitment > self.betToMatch:
                self.betToMatch = player.commitment
            self.currentPlayer = self.players[(self.turnIndex + 1) % len(self.players)]
            if self.checkAllMatched():
                self.advanceRound()
            return True
        else:
            return False
        
    def checkAllMatched(self) -> bool:
        allMatched = True
        for player in self.players:
            allMatched = allMatched and player.commitment == self.betToMatch
        return allMatched
    
    def startRound(self) -> bool:
        allReady = True
        for player in self.players:
            allReady = allReady and player.isReady
        if allReady:
            return self.advanceRound()
        return False

    def advanceRound(self) -> bool:
        self.state = GameState(self.state.value + 1)
        match self.state:
            case GameState.SHOWDOWN:
                # TODO Determine Winner
                return True
            case GameState.PREFLOP:
                self.resetForBettingRound()
                return True
            case GameState.FLOP:
                # TODO Deal 1 burn card and 3 community cards
                self.resetForBettingRound()
                self.communityCards.append(self.deck[9])
                self.communityCards.append(self.deck[10])
                self.communityCards.append(self.deck[11])
                return True
            case GameState.TURN:
                # TODO Deal 1 burn card and 1 community card
                self.resetForBettingRound()
                self.communityCards.append(self.deck[13])
                return True
            case GameState.RIVER:
                # TODO Deal 1 burn card and 1 community card
                self.resetForBettingRound()
                self.communityCards.append(self.deck[15])
                return True
            case _:
                return False
    
    def resetForBettingRound(self) -> bool:
        self.currentPlayer = self.players[self.startIndex]
        self.turnIndex = self.startIndex
        self.betToMatch = 0
        for player in self.players:
            player.resetCommitment()
        return True

    def getCommunityCards(self) -> list[Card]:
        return self.communityCards
    
    def determineWinner(self) -> Player:
        #TODO
        return Player
    
    def playerWins(self, player) -> bool:
        player.stackSize += self.potSize
        self.resetRound()
        return True
    
    def resetRound(self) -> bool:
        self.state = GameState.PREPARING
        for player in self.overallPlayers:
            if player.stackSize != 0:
                self.players.append(player)
        self.potSize = 0
        self.deck = Deck()
        self.communityCards = []
        self.turnIndex = 0
        self.startIndex = 0
        self.betToMatch = 0
        self.currentPlayer = None


