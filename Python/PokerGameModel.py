from PokerRound import PokerRound
from Player import Player

class PokerGameModel():
    previousRounds: list[PokerRound]
    players: list[Player]
    smallBlind: int
    bigBlind: int
    currentRound: PokerRound
    startIndex: int # tracks what player will start betting of each hand

    def __init__(self) -> None:
        self.previousRounds = []
        self.players = []
        self.smallBlind = 0
        self.bigBlind = 0
        self.currentRound = None

    def createRound(self) -> bool:
        # creates a new round (calls PokerRound constructor) and makes it the current round
        # returns true if successful, false if not
        raise NotImplementedError("createRound is not implemented")

    def endRound(self) -> bool:
        # ends the current round and moves it to the previous rounds
        # returns true if successful, false if not
        raise NotImplementedError("endRound is not implemented")

    def getPlayerFromSeat(self, seat) -> Player | None:
        # Returns the player object from the seat number
        # or none if no player is at that seat
        # for each player in self.players
        # if player.seatNumber == seat
        # return player
        # return None
        raise NotImplementedError("getPlayerFromSeat is not implemented")

    def addPlayer(self, seat) -> bool:
        # Updates to reflect what players are active in the game
        # calls getPlayerFromSeat
        # expects player to be None
        # create new player with that seat
        # otherwise if we did getPlayerFromSeat and it wasn't None
        # throw soft error / return false (don't quit program)
        # return true if successful, false if not
        raise NotImplementedError("addPlayers is not implemented")

    def removePlayer(self, seat) -> bool:
        # Updates to reflect what players should be removed from the game
        # calls getPlayerFromSeat
        # expects player to not be None
        # remove player from self.players
        # otherwise if we did getPlayerFromSeat and it was None
        # throw soft error / return false (don't quit program)
        # return true if successful, false if not
        raise NotImplementedError("removePlayers is not implemented")

    def isPlayerTurn(self, player: Player) -> bool:
        # Returns true if it is the player's turn to bet
        # return player == currentRound.currentPlayer
        raise NotImplementedError("isPlayerTurn is not implemented")

    def updateBet(self, seat) -> bool:
        # Keeps track of the potential bet amount as the users are still
        # deciding on the amount (haven't confirmed the bet yet)
        # call getPlayerFromSeat
        # pass return value into isPlayerTurn
        # if returns true, calls that Player's update bet method
        # return true if successful, false if not
        raise NotImplementedError("updateBets is not implemented")

    def makeBet(self, bet) -> bool:
        # Confirms the bet amount made from updateBet and updates
        # both the player amount and pot size for the round
        # call getPlayerFromSeat
        # pass return value into isPlayerTurn
        # if returns true, calls that Player's make bet method
        # call the round's make bet method
        # check that bet they're making is >= bet they need to make (check in round)
        # return true if successful, false if not
        raise NotImplementedError("makeBets is not implemented")

    def fold(self, seat) -> bool:
        # Based on the seat mapping, fold that player
        # call getPlayerFromSeat
        # pass return value into isPlayerTurn
        # if returns true, calls the rounds's fold method with the player
        # return true if successful, false if not
        raise NotImplementedError("fold is not implemented")

    def call(self, seat) -> bool:
        # Based on the seat mapping, call that player
        # call makeBet with betSize = pokerRound.betToMatch
        # return true if successful, false if not
        raise NotImplementedError("call is not implemented")

    def ready(self, seat) -> bool:
        # Updates the player status to ready (call toggleReady)
        # return true if successful, false if not
        raise NotImplementedError("ready is not implemented")
