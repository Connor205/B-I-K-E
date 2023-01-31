from Enums import Seat
import PlayerHand

class Player():
    name: str
    playerID: int
    seatNumber: Seat
    stackSize: int
    inGame: bool
    hand: PlayerHand

    def __init__(self, name: str, playerID: int) -> None:
        self.name = name
        self.playerID = playerID
        self.seatNumber = None
        self.stackSize = 0
        self.inGame = False
        self.hand = None

    def addToGame(self, seatNumber: Seat) -> None:
        """Adds a player to a game at the given seat"""
        self.seatNumber = seatNumber
        self.inGame = True

    def removeFromGame(self) -> None:
        """Removes the player from the game"""
        self.seatNumber = None
        self.inGame = False

    def makeBet(self, betSize: int) -> None:
        """Changing stack size based off of this player's bet"""
        self.stackSize -= betSize

    def winPot(self, potSize:int) -> None:
        """Changing stack size based off of the player's win"""
        self.stackSize += potSize

    def buyIn(self, buyInAmt: int) -> None:
        """Changing stack size based off of the player's buy in"""
        self.stackSize += buyInAmt