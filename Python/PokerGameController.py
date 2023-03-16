from PokerGameModel import PokerGameModel
from PokerGameView import PokerGameView
from Turret import Turret
from Shuffler import Shuffler
from Enums import Button

class PokerGameController():
    model: PokerGameModel
    view: PokerGameView
    turret: Turret
    shuffler: Shuffler
    whiteChipValue: int
    redChipValue: int
    blueChipValue: int

    def __init__(self, model, view, turret, shuffler) -> None:
        self.model = model
        self.view = view
        self.turret = turret
        self.shuffler = shuffler
        self.whiteChipValue = 1
        self.redChipValue = 5
        self.blueChipValue = 10

    def buttonListener(self, buttonStatus) -> None:
        match buttonStatus[0]:
            case Button.FOLD:
                # TODO logic for resetting potential bet if it's > 0
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
            case _:
                raise NotImplementedError("Unrecognized button")

    def updatePlayers(self, seat) -> None:
        # Based on input from the Arduino-side,
        # update the model to reflect what players are active in the game
        # Has logic to add/remove players
        raise NotImplementedError("updatePlayers is not implemented")

    def addPlayer(self, seat) -> None:
        # Based on input from the Arduino-side,
        # update the model to reflect what players are active in the game
        # calls model function to add player
        self.model.addPlayer(seat)

    def removePlayer(self, seat) -> None:
        # Based on input from the Arduino-side,
        # update the model to reflect what players are active in the game
        # calls model function to remove player
        self.model.removePlayer(seat)

    def updateBet(self, seat, bet) -> None:
        # Based on input from the buttons for each player
        # Update the potential bet amount in the model
        # Update the bet amount displayed in the view
        self.model.updateBet(seat, bet)

    def makeBet(self, seat) -> None:
        # Based on input from the buttons for each player
        # Update the bet amount displayed in view
        # Update the model to reflect the bet amount
        self.model.makeBet(seat)

    def fold(self, seat) -> None:
        # Based on input from the buttons for each player
        # Based on the seat mapping, updates model to fold those players
        # Update the view to reflect the fold
        self.model.fold(seat)

    def call(self, seat) -> None:
        # Based on input from the buttons for each player
        # Based on the seat mapping, updates model to call those players
        # Update the view to reflect the call
        self.model.call(seat)

    def ready(self, seat) -> None:
        # Based on input from the buttons for each player
        # Based on the seat mapping, updates model to ready those players
        # Update the view to reflect the ready
        self.model.ready(seat)

    def deal(self) -> None:
        # Get the game state and the list of seats
        # Give the command to the shuffler to deal to the seats
        raise NotImplementedError("deal is not implemented")

    def shuffle(self) -> None:
        # Command the shuffler to shuffle deck
        raise NotImplementedError("shuffle is not implemented")
    
    def settings(self) -> None:
        # Toggle the settings menu
        self.model.toggleSettings()
