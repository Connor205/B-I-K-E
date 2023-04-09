import logging
import sys
from Constants import *
from Deck import Deck
from Card import Card
from PlayerHand import PlayerHand
from Enums import GameState, Seat
from Player import Player
from typing import Tuple

class PokerRound():
    potSize: int
    state: GameState
    communityCards: list[Card]
    burnCards: list[Card]
    deck: Deck
    players: list[Player]
    turnIndex: int # keeps track of who's turn it is to bet
    startBettingRoundIndex: int # keeps track of who's starts betting each round
    smallBlindIndex: int # keeps track of who has the blinds each round
    currentPlayer: Player # keeps track of who's turn it is to bet
    betToMatch: int # the current bet to match
    overallPlayers: list[Player] # Tracking the players between hands
    smallBlind: int # the size of the small blind
    bigBlind: int # the size of the big blind
    logger: logging.Logger
    cardsDealt: int # the number of cards dealt so far

    def __init__(self) -> None:
        # init the logger
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.StreamHandler(sys.stdout))
        self.logger.setLevel(logging.DEBUG)

        self.initFourPlayers()
        self.potSize = 0
        self.state = GameState.PREPARING
        self.deck = Deck()
        self.communityCards = []
        self.burnCards = []
        self.turnIndex = 0
        self.startBettingRoundIndex = 0
        self.smallBlindIndex = 0
        self.betToMatch = 0
        self.currentPlayer = self.players[0]
        self.smallBlind = SMALL_BLIND
        self.bigBlind = BIG_BLIND
        self.cardsDealt = 0

    def initFourPlayers(self) -> None:
        self.players = [Player("Player 1", Seat.ONE), Player("Player 2", Seat.TWO), Player("Player 3", Seat.THREE), Player("Player 4", Seat.FOUR)]
        self.overallPlayers = self.players

    def playerFolds(self) -> bool:
        origSize = len(self.players)
        self.players.remove(self.currentPlayer)
        self.currentPlayer = self.players[self.turnIndex % len(self.players)]
        if len(self.players) == 1:
            self.playerWins(self.players[0])
            return True
        if self.startBettingRoundIndex > self.turnIndex:
            self.startBettingRoundIndex -= 1
        if self.checkAllMatched():
            self.advanceRound()
        return len(self.players) == origSize - 1
    
    def makeBet(self, player: Player) -> Tuple[bool, int]:
        if player != self.currentPlayer:
            return (False, 0)

        playerBet = player.potentialBet
        if playerBet < self.betToMatch and playerBet != player.stackSize:
            return (False, 0)
        if player.makeBet():
            self.potSize += playerBet
            if player.commitment > self.betToMatch:
                self.betToMatch = player.commitment
            self.turnIndex = (self.turnIndex + 1) % len(self.players)
            self.currentPlayer = self.players[self.turnIndex]
            if self.checkAllMatched():
                self.advanceRound()
            return (True, playerBet)
        else:
            return (False, 0)
        
    def checkAllMatched(self) -> bool:
        allMatched = True
        for player in self.players:
            allMatched = allMatched and player.commitment == self.betToMatch
        return allMatched
    
    def allReadyStatus(self) -> bool:
        allReady = True
        for player in self.players:
            allReady = allReady and player.isReady
        return allReady

    def advanceRound(self) -> bool:
        self.logger.debug("Called advance round. Current round is: " + str(self.state))
        self.state = GameState(self.state.value + 1)
        self.logger.debug("New round is: " + str(self.state))
        match self.state:
            case GameState.PREFLOP:
                self.logger.debug("Advancing state to PREFLOP")
                self.resetForBettingRound()
                # Make bets for blinds
                smallBlindPlayer = self.players[self.smallBlindIndex]
                bigBlindPlayer = self.players[(self.smallBlindIndex + 1) % len(self.players)]
                smallBlindPlayer.setBet(self.smallBlind)
                self.makeBet(smallBlindPlayer)
                bigBlindPlayer.setBet(self.bigBlind)
                self.makeBet(bigBlindPlayer)

                # Deal cards
                for i in range(2):
                    for player in self.players:
                        card = self.deck.drawCard()
                        print("Dealt " + str(card) + " to " + player.name)
                        self.cardsDealt += 1
                        player.addCard(card)
                        # player.hand.holeCards.append(card)
                        for card in player.hand.holeCards:
                            print(card)
                        # print(player.hand.holeCards[i])
                # debug print all the players' cards
                for player in self.players:
                    print(player.name + " has " + str(player.hand.getHoleCards()[0]) + " and " + str(player.hand.getHoleCards()[1]))
                return True
            case GameState.FLOP:
                self.logger.debug("Advancing state to FLOP")
                self.resetForBettingRound()
                # Deal burn card
                self.burnCards.append(self.deck.drawCard())
                # Deal community cards
                self.communityCards.append(self.deck.drawCard())
                self.communityCards.append(self.deck.drawCard())
                self.communityCards.append(self.deck.drawCard())
                self.cardsDealt += 4
                return True
            case GameState.TURN:
                self.logger.debug("Advancing state to TURN")
                self.resetForBettingRound()
                # Deal burn card
                self.burnCards(self.deck.drawCard())
                # Deal community card
                self.communityCards.append(self.deck.drawCard())
                self.cardsDealt += 2
                return True
            case GameState.RIVER:
                self.logger.debug("Advancing state to RIVER")
                self.resetForBettingRound()
                # Deal burn card
                self.burnCards(self.deck.drawCard())
                # Deal community card
                self.communityCards.append(self.deck.drawCard())
                self.cardsDealt += 2
                return True
            case GameState.SHOWDOWN:
                self.logger.debug("Advancing state to SHOWDOWN")
                self.playerWins(self.determineWinner())
                return True
            case _:
                self.logger.debug("Case didn't match")
                return False
    
    def resetForBettingRound(self) -> bool:
        self.currentPlayer = self.players[self.startBettingRoundIndex]
        self.turnIndex = self.startBettingRoundIndex
        self.betToMatch = 0
        for player in self.players:
            player.resetCommitment()
        return True

    def addPlayer(self, player: Player) -> bool:
        """
        Adds a player to the round
        Args:
            player (Player): The player to add
        Returns:
            bool: True if the player was added, false if not (e.g. if the round has already started or if the player is already in the round)
        """
        # Only add the player if they're not already in the round and if the round hasn't started
        if player not in self.players and self.state == GameState.PREPARING:
            self.players.append(player)
            self.activePlayers.append(player)
            return True
        return False
    
    def removePlayer(self, player: Player) -> bool:
        """
        Removes a player from the round
        Args:
            player (Player): The player to remove
        Returns:
            bool: True if the player was removed, false if not (e.g. if the round has already started or if the player is not in the round)
        """
        # Only remove the player if they're in the round and if the round hasn't started
        if player in self.players and self.state == GameState.PREPARING:
            self.players.remove(player)
            # The player may not be in the active players list if they've already folded
            if player in self.activePlayers:
                self.activePlayers.remove(player)
            return True
        return False

    def shuffleDeck(self) -> None:
        """Shuffles the deck"""
        self.deck.shuffleDeck()

    def getDeck(self) -> Deck:
        """Returns the deck"""
        return self.deck
    
    def readyPlayer(self, player: Player) -> bool:
        """
        Sets a player to ready
        Args:
            player (Player): The player to set to ready
        Returns:
            bool: True if the player was set to ready, false if not (e.g. if the player is not in the round)
        """
        if player in self.players:
            player.setReady(True)
            return True
        return False
    
    def unreadyPlayer(self, player: Player) -> bool:
        """
        Sets a player to not ready
        Args:
            player (Player): The player to set to not ready
        Returns:
            bool: True if the player was set to not ready, false if not (e.g. if the player is not in the round)
        """
        if player in self.players:
            player.setReady(False)
            return True
        return False
    
    def getPlayers(self) -> list[Player]:
        """Returns the players in the round"""
        return self.players
    
    def getActivePlayers(self) -> list[Player]:
        """Returns the active players in the round"""
        return self.activePlayers
    
    def getPlayerFromSeat(self, seat: Seat) -> Player | None:
        """
        Gets the player from a seat number
        Args:
            seat (int): The seat number
        Returns:
            Player: The player at the seat number
        """
        for player in self.players:
            if player.seatNumber == seat:
                return player
        return None
    
    def getPotSize(self) -> int:
        """Returns the pot size"""
        return self.potSize
    
    def getState(self) -> GameState:
        """Returns the state of the round"""
        return self.state
    
    def getTurnIndex(self) -> int:
        """Returns the turn index"""
        return self.turnIndex
    
    def getBetToMatch(self) -> int:
        """Returns the bet to match"""
        return self.betToMatch
    
    def getCurrentPlayer(self) -> Player:
        """Returns the current player"""
        return self.currentPlayer
    
    def getCommunityCards(self) -> list[Card]:
        """Returns the community cards"""
        return self.communityCards
    
    def determineWinner(self) -> Player:
        """
        Determines the winner of the round

        Returns:
            Player: The winner of the round
        """
        playerRanks = {}
        for player in self.players:
            player.determineBestHand(self.communityCards)
            playerRanks[player] = player.getHand().getRanking()

        bestRank = max(playerRanks.values())
        bestPlayers = [player for player, rank in playerRanks.items() if rank == bestRank]

        if len(bestPlayers) == 1:
            return bestPlayers[0]
        else:
            return self.determineWinnerByKickers(bestPlayers)
    
    def determineWinnerByKickers(self, players: list[Player]) -> Player:
        """
        Determines the winner of the round by kickers

        Args:
            players (list[Player]): The players to determine the winner of the round by kickers

        Returns:
            Player: The winner of the round
        """
        playerKickers = {}
        for player in players:
            playerKickers[player] = player.getHand().getKickers(self.communityCards)

        bestKickers = max(playerKickers.values())
        bestPlayers = [player for player, kickers in playerKickers.items() if kickers == bestKickers]

        if len(bestPlayers) == 1:
            return bestPlayers[0]
        else:
            return self.determineWinnerByKickers(bestPlayers)
    
    def playerWins(self, player: Player) -> bool:
        player.stackSize += self.potSize
        self.state = GameState.POSTHAND
        #self.resetRound()
        return True
    
    def resetBet(self, player: Player) -> bool:
        if player != self.currentPlayer:
            return False
        player.resetBet()
        return True
    
    def call(self, player: Player) -> Tuple[bool, int]:
        if player != self.currentPlayer:
            return False
        player.setBet(self.betToMatch)
        return self.makeBet(player)
    
    def resetRound(self) -> bool:
        self.state = GameState.PREPARING
        self.players = []
        for player in self.overallPlayers:
            if player.stackSize != 0:
                self.players.append(player)
        self.potSize = 0
        self.deck = Deck()
        self.communityCards = []
        self.turnIndex = 0
        self.startBettingRoundIndex = 0
        self.smallBlindIndex += 1 % len(self.players)
        self.betToMatch = 0
        self.currentPlayer = self.players[self.smallBlindIndex]

    def getSmallBlindPlayer(self) -> Player:
        return self.players[self.smallBlindIndex]

    def getBigBlindPlayer(self) -> Player:
        return self.players[(self.smallBlindIndex + 1) % len(self.players)]
    
    def __str__(self) -> str:
        return f"State: {self.state}, \nPot Size: {self.potSize}, \
            \nPlayers: " + str([str(player) for player in self.players]) + ", \
                  \nCurrent Player: {self.currentPlayer}, \nCommunity Cards: {self.communityCards}, \
                    \nTurn Index: {self.turnIndex}, \nStart Betting Round Index: {self.startBettingRoundIndex}, \
                        \nSmall Blind Index: {self.smallBlindIndex}, \nBet to Match: {self.betToMatch}\n"
