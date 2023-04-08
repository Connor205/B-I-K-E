from PokerRound import PokerRound
from Player import Player

class PokerGameModel():
    previousRounds: list[PokerRound]
    players: list[Player]
    smallBlind: int
    bigBlind: int
    currentRound: PokerRound
    startIndex: int # tracks what player will start betting of each hand
    inSettings: bool # is the settings menu active
    shuffleWait: bool
    dealWait: bool

    def __init__(self) -> None:
        self.previousRounds = []
        self.players = []
        self.smallBlind = 0
        self.bigBlind = 0
        self.currentRound = None
        self.startIndex = 0
        self.inSettings = False
        self.shuffleWait = True
        self.dealWait = False

    def createRound(self) -> bool:
        # creates a new round (calls PokerRound constructor) and makes it the current round
        # returns true if successful, false if not
        self.currentRound = PokerRound()
        return True

    def endRound(self) -> bool:
        # ends the current round and moves it to the previous rounds
        # returns true if successful, false if not
        self.previousRounds.append(self.currentRound)
        self.currentRound = None
        return True

    def startRound(self) -> bool:
        # Starts the current round
        # returns true if successful, false if not
        self.currentRound.startRound()
        return True

    def getPlayerFromSeat(self, seat) -> Player | None:
        # Returns the player object from the seat number
        # or none if no player is at that seat
        # for each player in self.players
        # if player.seatNumber == seat
        # return player
        # return None
        for player in self.players:
            if seat == player.seat:
                return player
        return None

    def addPlayer(self, seat) -> bool:
        # Updates to reflect what players are active in the game
        # calls getPlayerFromSeat
        # expects player to be None
        # create new player with that seat
        # otherwise if we did getPlayerFromSeat and it wasn't None
        # throw soft error / return false (don't quit program)
        # return true if successful, false if not
        if self.getPlayerFromSeat(seat) != None:
            return False
        else:
            self.players.append(Player("Player " + seat.toString(), seat))
            # TODO self.players.sort() sort by seat num
            return True

    def removePlayer(self, seat) -> bool:
        # Updates to reflect what players should be removed from the game
        # calls getPlayerFromSeat
        # expects player to not be None
        # remove player from self.players
        # otherwise if we did getPlayerFromSeat and it was None
        # throw soft error / return false (don't quit program)
        # return true if successful, false if not
        try:
            self.players.remove(self.getPlayerFromSeat(seat))
            return True
        except:
            return False
        

    def isPlayerTurn(self, player: Player) -> bool:
        # Returns true if it is the player's turn to bet
        return player == self.currentRound.currentPlayer

    def updateBet(self, seat, amount) -> bool:
        # Keeps track of the potential bet amount as the users are still
        # deciding on the amount (haven't confirmed the bet yet)
        # call getPlayerFromSeat
        # pass return value into isPlayerTurn
        # if returns true, calls that Player's update bet method
        # return true if successful, false if not
        player = self.getPlayerFromSeat(seat)
        if (self.isPlayerTurn(player)):
            player.updateBet(amount)
            return True
        else:
            return False

    def makeBet(self, seat) -> bool:
        # Confirms the bet amount made from updateBet and updates
        # both the player amount and pot size for the round
        # call getPlayerFromSeat
        # pass return value into isPlayerTurn
        # if returns true, calls that Player's make bet method
        # call the round's make bet method
        # check that bet they're making is >= bet they need to make (check in round)
        # return true if successful, false if not
        player = self.getPlayerFromSeat(seat)
        if (self.isPlayerTurn(player)):
            self.currentRound.makeBet(player)
            return True
        else:
            return False

    def fold(self, seat) -> bool:
        # Based on the seat mapping, fold that player if they have no potential bet
        # if their potential bet is not 0, set it to 0 
        # call getPlayerFromSeat
        # pass return value into isPlayerTurn
        # if returns true, calls the rounds's fold method with the player
        # return true if successful, false if not
        player = self.getPlayerFromSeat(seat)
        if (self.isPlayerTurn(player) and self.player.potentialBet == 0):
            self.currentRound.fold()
            return True
        elif (self.isPlayerTurn(player) and self.player.potentialBet != 0):
            player.potentialBet = 0
            return False
        else:
            return False

    def call(self, seat) -> bool:
        # Based on the seat mapping, call that player
        # call makeBet with betSize = pokerRound.betToMatch
        # return true if successful, false if not
        player = self.getPlayerFromSeat(seat)
        if (self.isPlayerTurn(player)):
            self.currentRound.call()
            return True
        else:
            return False

    def ready(self, seat) -> bool:
        # Updates the player status to ready (call toggleReady)
        # return true if successful, false if not
        self.getPlayerFromSeat(seat).toggleReady()
        self.currentRound.startRound(self.startIndex)

    def toggleSettings(self) -> bool:
        # Toggles the settings menu
        # return true if successful, false if not
        self.inSettings = not self.inSettings
        
