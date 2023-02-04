from PokerGameModel import PokerGameModel
from PokerGameView import PokerGameView
from Turret import Turret
from Shuffler import Shuffler

class PokerGameController():
    model: PokerGameModel = None
    view: PokerGameView = None
    turret: Turret = None
    shuffler: Shuffler = None

    def __init__(self, model, view, turret, shuffler) -> None:
        self.model = model
        self.view = view
        self.turret = turret
        self.shuffler = shuffler

    def buttonListener(self, buttonStatus) -> None:
        # This is the listener for the buttons on the arduino side
        # We need to figure out what button was pressed and then call the appropriate function
        # We still need to figure out the format/type of buttonStatus
        raise NotImplementedError("buttonListener is not implemented")

    def updatePlayers(self, seats) -> None:
        # Based on input from the Arduino-side,
        # update the model to reflect what players are active in the game
        # Has logic to add/remove players
        raise NotImplementedError("updatePlayers is not implemented")

    def addPlayer(self, seat) -> None:
        # Based on input from the Arduino-side,
        # update the model to reflect what players are active in the game
        # calls model function to add player
        raise NotImplementedError("addPlayers is not implemented")

    def removePlayer(self, seat) -> None:
        # Based on input from the Arduino-side,
        # update the model to reflect what players are active in the game
        # calls model function to remove player
        raise NotImplementedError("removePlayers is not implemented")

    def updateBet(self, seat) -> None:
        # Based on input from the buttons for each player
        # Update the potential bet amount in the model
        # Update the bet amount displayed in the view
        raise NotImplementedError("updateBets is not implemented")

    def makeBet(self, bet) -> None:
        # Based on input from the buttons for each player
        # Update the bet amount displayed in view
        # Update the model to reflect the bet amount
        raise NotImplementedError("makeBets is not implemented")

    def fold(self, seat) -> None:
        # Based on input from the buttons for each player
        # Based on the seat mapping, updates model to fold those players
        # Update the view to reflect the fold
        raise NotImplementedError("fold is not implemented")

    def call(self, seat) -> None:
        # Based on input from the buttons for each player
        # Based on the seat mapping, updates model to call those players
        # Update the view to reflect the call
        raise NotImplementedError("call is not implemented")

    def ready(self, seat) -> None:
        # Based on input from the buttons for each player
        # Based on the seat mapping, updates model to ready those players
        # Update the view to reflect the ready
        raise NotImplementedError("ready is not implemented")

    def deal(self) -> None:
        # Get the game state and the list of seats
        # Give the command to the shuffler to deal to the seats
        raise NotImplementedError("deal is not implemented")

    def shuffle(self) -> None:
        # Command the shuffler to shuffle deck
        raise NotImplementedError("shuffle is not implemented")
