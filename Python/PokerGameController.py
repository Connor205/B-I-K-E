import logging
import sys
from PokerGameModel import PokerGameModel
from PokerGameView import PokerGameView
from Turret import Turret
from Shuffler import Shuffler
from Enums import Button, Seat, GameState
from Constants import *

class PokerGameController():
    logger: logging.Logger
    model: PokerGameModel
    view: PokerGameView
    turret: Turret
    shuffler: Shuffler

    def __init__(self, model, view, turret, shuffler) -> None:
        # init the logger
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.StreamHandler(sys.stdout))
        self.logger.setLevel(logging.DEBUG)

        self.model = model
        self.view = view
        self.turret = turret
        self.shuffler = shuffler

        self.model.createRound()

    def numToSeat(self, num: int) -> Seat:
        """
        Converts a number to a Seat. 
        From Interface.py, the panels are labeled 0-3 from left to right while facing the table (and screen)
        0 is the one closest to the shuffler, 3 is the one closest to the estop
        
        Args:
            num (int): Number to convert
            
        Returns:
            Seat: Seat corresponding to the number
        """
        if num == 0:
            return Seat.ONE
        elif num == 1:
            return Seat.TWO
        elif num == 2:
            return Seat.THREE
        elif num == 3:
            return Seat.FOUR
        else:
            self.logger.error("Invalid seat number: %d", num)
            return None

    def numToButton(self, num: int) -> Button:
        """
        Converts a number to a Button.
        From Interface.py, the buttons are labeled right to left (0 -> 7) for each panel
        From 0->7 we have: Black, Red, Blue, White, Fold, Bet, Check, Call
        
        Args:
            num (int): Number to convert
            
        Returns:
            Button: Button corresponding to the number
        """
        if num == 0:
            return Button.SETTINGS
        elif num == 1:
            return Button.RED_CHIP
        elif num == 2:
            return Button.BLUE_CHIP
        elif num == 3:
            return Button.WHITE_CHIP
        elif num == 4:
            return Button.FOLD
        elif num == 5:
            return Button.BET
        elif num == 6:
            return Button.CHECK
        elif num == 7:
            return Button.CALL
        else:
            self.logger.error("Invalid button number: %d", num)
            return None

    def buttonListener(self, buttonStatus: tuple[int, int]) -> None:
        """
        Listens for button presses and calls the appropriate function

        Args:
            buttonStatus (tuple[int, int]): Tuple containing the button number and the panel number
        """
        button = self.numToButton(buttonStatus[0])
        seat = self.numToSeat(buttonStatus[1])

        origState = self.model.getCurrentRoundState()

        # If the gamestate is preparing, any button press will ready the player
        if origState == GameState.PREPARING:
            player = self.model.getPlayerFromSeat(seat)
            if player is not None:
                player.toggleReady()
                self.logger.debug("Toggled ready for player: " + str(player))
            else:
                self.logger.error("Tried to toggle ready on a non-existent player")
            return

        match button:
            case Button.FOLD:
                if self.model.inSettings:
                    self.removePlayer(seat)
                else:
                    self.fold(seat)
            case Button.CHECK:
                if self.model.inSettings:
                    self.addPlayer(seat)
                else:
                    self.resetBet(seat)
                    self.makeBet(seat)
            case Button.CALL:
                if self.model.inSettings:
                    self.changeBlinds(seat)
                else:
                    self.call(seat)
            case Button.BET:
                if not self.model.inSettings:
                    self.makeBet(seat)
            case Button.WHITE_CHIP:
                if not self.model.inSettings:
                    self.updateBet(seat, WHITE_CHIP_VALUE)
            case Button.RED_CHIP:
                if not self.model.inSettings:
                    self.updateBet(seat, RED_CHIP_VALUE)
            case Button.BLUE_CHIP:
                if not self.model.inSettings:
                    self.updateBet(seat, BLUE_CHIP_VALUE)
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
            
        newState = self.model.getCurrentRoundState()

        if newState != origState:
            self.deal(newState)

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

    def resetBet(self, seat: Seat) -> None:
        # Based on input from the buttons for each player
        # Update the potential bet amount in the model
        # Update the bet amount displayed in the view
        self.model.resetBet(seat)
        # TODO: Update the view to reflect the bet amount

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

    def deal(self, state: GameState) -> None:
        players = self.model.getPlayersInHand()
        match state:
            case GameState.PREFLOP:
                for _ in range(2):
                    for player in players:
                        self.turret.dealToSeat(player.seatNumber)
            case GameState.FLOP:
                self.turret.dealDiscard(1)
                self.turret.dealCommunity(3)
            case GameState.TURN:
                self.turret.dealDiscard(1)
                self.turret.dealCommunity(1)
            case GameState.RIVER:
                self.turret.dealDiscard(1)
                self.turret.dealCommunity(1)
            case GameState.SHOWDOWN:
                # TODO: Have view display winner, wait for button confirmation from winner to end hand
            case GameState.POSTHAND:
                remainingCards = self.model.getRemainingCards()
                self.turret.dealDiscard(remainingCards)
            

    
    def settings(self) -> None:
        # Toggle the settings menu
        self.model.toggleSettings()
        # TODO: Update the view to reflect the settings menu

    def update(self) -> None:

        # Starting a round
        if self.model.getCurrentRoundState() == GameState.PREPARING and self.model.allReadyStatus():
            # TODO: Update the view to say "Please put cards in and press deal confirm"

            # Call the blocking method for the turret, waiting for confirmation button
            self.turret.waitForConfirmation()

            # If in state preparing, we just advance the round to start it
            self.model.advanceRound()

        # Update the view to reflect the model
        view.update()


if __name__ == "__main__":
    import pygame
    # Test code
    model = PokerGameModel()
    view = PokerGameView(model)
    turret = Turret("/dev/tty.Bluetooth-Incoming-Port")
    shuffler = Shuffler("/dev/tty.Bluetooth-Incoming-Port")
    controller = PokerGameController(model, view, turret, shuffler)

    playerNum = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                # test each of the buttonListener cases
                if event.key == pygame.K_1:
                    controller.buttonListener((0, playerNum))
                if event.key == pygame.K_2:
                    controller.buttonListener((1, playerNum))
                if event.key == pygame.K_3:
                    controller.buttonListener((2, playerNum))
                if event.key == pygame.K_4:
                    controller.buttonListener((3, playerNum))
                if event.key == pygame.K_5:
                    controller.buttonListener((4, playerNum))
                if event.key == pygame.K_6:
                    controller.buttonListener((5, playerNum))
                if event.key == pygame.K_7:
                    controller.buttonListener((6, playerNum))
                if event.key == pygame.K_8:
                    controller.buttonListener((7, playerNum))
                if event.key == pygame.K_q:
                    playerNum = 0
                if event.key == pygame.K_w:
                    playerNum = 1
                if event.key == pygame.K_e:
                    playerNum = 2
                if event.key == pygame.K_r:
                    playerNum = 3

        controller.update()
