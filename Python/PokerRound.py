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
    players: list[Player] # list of all players in the round
    activePlayers: list[Player] # players who are still in the round
    currentPlayer: Player # keeps track of who's turn it is to bet
    turnIndex: int # keeps track of who's turn it is to bet
    betToMatch: int # the current bet to match

    def __init__(self) -> None:
        self.players = []
        self.activePlayers = []
        self.currentPlayer = None
        self.potSize = 0
        self.state = GameState.PREPARING
        self.communityCards = []
        self.deck = Deck()
        self.turnIndex = 0
        self.betToMatch = 0

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
    
    def startRound(self) -> tuple(bool, list[Card]):
        """
        Starts the round. This will deal the cards to the players and set the state to PREFLOP. 
        The dealing of cards will be done 1 to each player at a time.

        Returns:
            bool: True if the round was started, false if not (e.g. if the round has already started or if not all players are ready)
            list[Card]: The player cards that were dealt
        """
        cardsDealt = []
        if self.state == GameState.PREPARING:
            # Check if all players are ready
            allReady = True
            for player in self.activePlayers:
                allReady = allReady and player.isReady
            if allReady:
                # Deal cards to players
                for _ in range(2):
                    for player in self.activePlayers:
                        card = self.deck.dealCard()
                        player.addCard(card)
                        cardsDealt.append(card)
                self.state = GameState.PREFLOP
                self.currentPlayer = self.activePlayers[self.turnIndex]
                return (True, cardsDealt)
        return (False, cardsDealt)
    
    def nextTurn(self) -> bool:
        """
        Moves to the next turn. This will increment the turn index and set the current player to the next player in the list. 

        Returns:
            bool: True if the turn was moved to the next player, false if not (e.g. if the round has not started)
        """
        if self.state != GameState.PREPARING:
            self.turnIndex += 1
            if self.turnIndex >= len(self.activePlayers):
                self.turnIndex = 0
            self.currentPlayer = self.activePlayers[self.turnIndex]
            return True
        return False
    
    def nextRound(self) -> bool:
        """
        Moves to the next round. This will increment the round index and set the current player to the next player in the list. 

        Returns:
            bool: True if the round was moved to the next player, false if not (e.g. if the round has not started)
        """
        if self.state != GameState.PREPARING:
            self.state = GameState(self.state.value + 1)
            self.turnIndex = 0
            self.currentPlayer = self.activePlayers[self.turnIndex]
            return True
        return False
    
    def dealCommunityCards(self, numCards: int) -> tuple(bool, list[Card]):
        """
        Deals the specified number of community cards. 
        The first card dealt will be burnt (i.e. discarded) and the next ones will be dealt to the community cards.

        Args:
            numCards (int): The number of cards to deal

        Returns:
            bool: True if the cards were dealt, false if not (e.g. if the round has not started) or if the number of cards is invalid
            list[Card]: The community cards that were dealt
        """
        cardsDealt = []
        if len(self.communityCards) + numCards > 5:
            return (False, cardsDealt)
        if self.state != GameState.PREPARING:
            for _ in range(numCards):
                burnt = self.deck.drawCard()
                self.communityCards.append(self.deck.drawCard())
                cardsDealt.append(self.communityCards[-1])
            return (True, cardsDealt)
        return (False, cardsDealt)

    def foldCurrentPlayer(self) -> bool:
        """
        Folds the current player. This will remove the player from the active players list and move to the next turn.

        Returns:
            bool: True if the player was folded, false if not (e.g. if the round has not started)
        """
        if self.state != GameState.PREPARING:
            self.activePlayers.remove(self.currentPlayer)
            self.nextTurn()
            return True
        return False
    
    def updateBetCurrentPlayer(self, amount: int) -> bool:
        """
        Updates the current player's potential bet. This will not increment the pot size or change the bet to match.

        Args:
            amount (int): The amount to bet

        Returns:
            bool: True if the player bet, false if not (e.g. if the round has not started)
        """
        if self.state != GameState.PREPARING:
            # The updateBet method will check if the amount is valid
            self.currentPlayer.updateBet(amount)
            return True
        return False
    
    def resetBetCurrentPlayer(self) -> bool:
        """
        Resets the current player's potential bet. This will not increment the pot size or change the bet to match.

        Returns:
            bool: True if the player bet, false if not (e.g. if the round has not started)
        """
        if self.state != GameState.PREPARING:
            self.currentPlayer.resetBet()
            return True
        return False
    
    def makeBetCurrentPlayer(self) -> bool:
        """
        Makes the current player bet their potential bet. This will increment the pot size and set the bet to match to the amount.
        This method is equivalent to raising, provided the player has been using `updateBetCurrentPlayer` to update their bet.

        Returns:
            bool: True if the player bet, false if not (e.g. if the round has not started)
        """
        if self.state != GameState.PREPARING:
            amount = self.currentPlayer.getPotentialBet()
            if amount < self.betToMatch:
                return False
            self.potSize += amount
            self.betToMatch = amount
            # As the bet is updated, its validity is checked, so makeBet will be valid
            self.currentPlayer.makeBet()
            return True
        return False
    
    def callCurrentPlayer(self) -> bool:
        """
        Makes the current player call the bet to match. This will increment the pot size by the bet to match.

        Returns:
            bool: True if the player called, false if not (e.g. if the round has not started)
        """
        if self.state != GameState.PREPARING:
            self.potSize += self.betToMatch
            self.currentPlayer.setBet(self.betToMatch)
            return True
        return False
    
    def checkCurrentPlayer(self) -> bool:
        """
        Makes the current player check. This will do nothing.

        Returns:
            bool: True if the player checked, false if not (e.g. if the round has not started)
        """
        if self.state != GameState.PREPARING:
            return True
        return False
