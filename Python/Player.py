from Enums import Seat
from PlayerHand import PlayerHand
from Constants import *

class Player():
    name: str
    seatNumber: Seat
    stackSize: int
    hand: PlayerHand
    potentialBet: int
    isReady: bool
    commitment: int # How much has the player bet during this round of betting

    def __init__(self, name: str, seatNumber: Seat) -> None:
        self.name = name
        self.seatNumber = seatNumber
        self.stackSize = INITIAL_STACK_SIZE
        self.hand = PlayerHand()
        self.potentialBet = 0
        self.isReady = False
        self.commitment = 0

    def getPotentialBet(self) -> int:
        """Returns the player's potential bet"""
        return self.potentialBet

    def addToGame(self, seatNumber: Seat) -> None:
        """Adds a player to a game at the given seat"""
        self.seatNumber = seatNumber

    def removeFromGame(self) -> None:
        """Removes the player from the game"""
        self.seatNumber = None

    def makeBet(self) -> bool:
        """Changing stack size based off of this player's bet"""
        if self.stackSize >= self.potentialBet:
            self.stackSize -= self.potentialBet
            self.commitment += self.potentialBet
            self.potentialBet = 0
            return True
        else:
            return False

    def winPot(self, potSize:int) -> None:
        """Changing stack size based off of the player's win"""
        self.stackSize += potSize

    def buyIn(self, buyInAmt: int) -> None:
        """Changing stack size based off of the player's buy in"""
        self.stackSize += buyInAmt

    def updateBet(self, betSize: int) -> None:
        """
        Changing the player's potential bet by the betSize. 
        If the betSize is negative, the player's potential bet is reset to 0. If the betSize is greater than the player's stack size,
        the player's potential bet is set to the player's stack size.
        
        Args:
            betSize (int): The amount to change the player's potential bet by"""
        self.potentialBet += betSize
        if self.potentialBet < 0:
            self.potentialBet = 0
        if self.potentialBet > self.stackSize:
            self.potentialBet = self.stackSize

    def setBet(self, totalBetSize: int) -> None:
        """
        Sets the player's potential bet to totalBetSize. If totalBetSize is greater than the player's stack size,
        the player's potential bet is set to the player's stack size.
        
        Args:
            totalBetSize (int): The total bet size
        """
        self.potentialBet = totalBetSize
        if self.potentialBet > self.stackSize:
            self.potentialBet = self.stackSize

    def resetBet(self) -> None:
        """Resets the player's bet"""
        self.potentialBet = 0

    def toggleReady(self) -> None:
        """Player is ready to play"""
        self.isReady = not self.isReady

    def resetCommitment(self) -> None:
        self.commitment = 0
        
    def setReady(self, isReady: bool) -> None:
        """Player is ready to play"""
        self.isReady = isReady

    def getHand(self) -> PlayerHand:
        """Returns the player's hand"""
        return self.hand
    
    def addCard(self, card) -> None:
        """Adds a card to the player's hand"""
        self.hand.addHoleCard(card)

    def __str__(self) -> str:
        return f"{self.name} is sitting at seat {self.seatNumber} with a stack size of {self.stackSize} and a potential bet of {self.potentialBet}"
