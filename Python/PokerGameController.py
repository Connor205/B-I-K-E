import logging
import sys
from PokerGameModel import PokerGameModel
from PokerGameView import PokerGameView
from Turret import Turret
from Shuffler import Shuffler
from Enums import Button, Seat

class PokerGameController():
    logger: logging.Logger
    model: PokerGameModel
    view: PokerGameView
    turret: Turret
    shuffler: Shuffler
    whiteChipValue: int
    redChipValue: int
    blueChipValue: int

    def __init__(self, model, view, turret, shuffler) -> None:
        # init the logger
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.StreamHandler(sys.stdout))

        self.model = model
        self.view = view
        self.turret = turret
        self.shuffler = shuffler
        self.whiteChipValue = 1
        self.redChipValue = 5
        self.blueChipValue = 10

    def numToSeat(self, num: int) -> Seat:
        """
        Converts a number to a Seat.
        
        Args:
            num (int): Number to convert
            
        Returns:
            Seat: Seat corresponding to the number
        """
        if num == 1:
            return Seat.ONE
        elif num == 2:
            return Seat.TWO
        elif num == 3:
            return Seat.THREE
        elif num == 4:
            return Seat.FOUR
        else:
            self.logger.error("Invalid seat number: %d", num)
            return None


    def buttonListener(self, buttonStatus) -> None:
        match buttonStatus[0]:
            case Button.FOLD:
                if self.model.inSettings:
                    self.removePlayer(buttonStatus[1])
                else:
                    self.fold(buttonStatus[1])
            case Button.CHECK:
                if self.model.inSettings:
                    self.addPlayer(buttonStatus[1])
                else:
                    self.bet(buttonStatus[1])
            case Button.CALL:
                if self.model.inSettings:
                    self.changeBlinds(buttonStatus[1])
                else:
                    self.bet(buttonStatus[1])
            case Button.BET:
                if not self.model.inSettings:
                    self.bet(buttonStatus[1])
            case Button.WHITE_CHIP:
                if not self.model.inSettings:
                    self.updateBet(buttonStatus[1], self.whiteChipValue)
            case Button.RED_CHIP:
                if not self.model.inSettings:
                    self.updateBet(buttonStatus[1], self.redChipValue)
            case Button.BLUE_CHIP:
                if not self.model.inSettings:
                    self.updateBet(buttonStatus[1], self.blueChipValue)
            case Button.SETTINGS:
                self.settings()
            case Button.SHUFFLECONFIRM:
                if self.model.shuffleWait:
                    self.shuffle()
            case Button.DEALCONFIRM:
                if self.model.dealWait:
                    self.deal()
            case _:
                raise NotImplementedError("Unrecognized button")

    def updatePlayers(self, seat: Seat) -> None:
        # Based on input from the Arduino-side,
        # update the model to reflect what players are active in the game
        # Has logic to add/remove players
        raise NotImplementedError("updatePlayers is not implemented")

    def addPlayer(self, seat: Seat) -> None:
        # Based on input from the Arduino-side,
        # update the model to reflect what players are active in the game
        # calls model function to add player
        if self.model.addPlayer(seat):
            self.view.addPlayer(seat)

    def removePlayer(self, seat: Seat) -> None:
        # Based on input from the Arduino-side,
        # update the model to reflect what players are active in the game
        # calls model function to remove player
        if self.model.removePlayer(seat):
            self.view.removePlayer(seat)

    def updateBet(self, seat: Seat, bet: int) -> None:
        # Based on input from the buttons for each player
        # Update the potential bet amount in the model
        # Update the bet amount displayed in the view
        if self.model.updateBet(seat, bet):
            self.view.updatePlayerBet(seat, bet)

    def makeBet(self, seat: Seat) -> None:
        # Based on input from the buttons for each player
        # Update the bet amount displayed in view
        # Update the model to reflect the bet amount
        self.model.makeBet(seat)
        # TODO: Update the view to reflect the bet amount

    def fold(self, seat: Seat) -> None:
        # Based on input from the buttons for each player
        # Based on the seat mapping, updates model to fold those players
        # Update the view to reflect the fold
        if self.model.fold(seat):
            self.view.fold(seat)

    def call(self, seat: Seat) -> None:
        # Based on input from the buttons for each player
        # Based on the seat mapping, updates model to call those players
        # TODO: Update the view to reflect the call
        self.model.call(seat)

    def ready(self, seat: Seat) -> None:
        # Based on input from the buttons for each player
        # Based on the seat mapping, updates model to ready those players
        # Update the view to reflect the ready
        self.model.ready(seat)

    def deal(self) -> None:
        self.model.dealWait = False
        self.model.startRound()
        raise NotImplementedError("deal is not implemented")

    def shuffle(self) -> None:
        self.runShuffler()
        self.model.shuffleWait = False
        self.model.dealWait = True
        raise NotImplementedError("shuffle is not implemented")
    
    def settings(self) -> None:
        # Toggle the settings menu
        self.model.toggleSettings()
        # TODO: Update the view to reflect the settings menu
