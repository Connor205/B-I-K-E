from Enums import Seat
from PlayerHand import PlayerHand

class Player():
    name: str
    playerID: int
    seatNumber: Seat
    stackSize: int
    inGame: bool
    hand: PlayerHand
    potentialBet: int
    isReady: bool
    commmitment: int # How much has the player bet during this round of betting

    def __init__(self, name: str, playerID: int) -> None:
        self.name = name
        self.playerID = playerID
        self.seatNumber = None
        self.stackSize = 0
        self.inGame = False
        self.hand = None
        self.potentialBet = 0
        self.isReady = False
        self.commmitment = 0

    def addToGame(self, seatNumber: Seat) -> None:
        """Adds a player to a game at the given seat"""
        self.seatNumber = seatNumber
        self.inGame = True

    def removeFromGame(self) -> None:
        """Removes the player from the game"""
        self.seatNumber = None
        self.inGame = False

    def makeBet(self) -> bool:
        """Changing stack size based off of this player's bet"""
        if self.stackSize >= self.potentialBet:
            self.stackSize -= self.potentialBet
            self.commmitment += self.potentialBet
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
        """Changing the player's potential bet"""
        self.potentialBet += betSize

    def toggleReady(self) -> None:
        """Player is ready to play"""
        self.isReady = not self.isReady

    def resetCommitment(self) -> None:
        self.commmitment = 0
