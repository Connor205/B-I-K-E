import logging
import sys
from PokerGameModel import PokerGameModel
from PokerGameView import PokerGameView
from Turret import Turret
from Enums import Button, Seat, GameState
from Constants import *
from typing import Tuple
from Interface import Interface
from threading import Lock 

class PokerGameController():
    logger: logging.Logger
    model: PokerGameModel
    view: PokerGameView
    turret: Turret
    lock: Lock


    def __init__(self, model, view, turret) -> None:
        # init the logger
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.StreamHandler(sys.stdout))
        self.logger.setLevel(logging.DEBUG)

        self.model = model
        self.view = view
        self.turret = turret
        self.interface = Interface("/dev/ttyUSB0", self.buttonListener)

        self.lock = Lock()

        # Create a round
        self.model.createRound()

        # Update the view to reflect the new round
        self.view.createFromModel()

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

    def buttonListener(self, buttonStatus: Tuple[int, int]) -> None:
        """
        Listens for button presses and calls the appropriate function

        Args:
            buttonStatus (Tuple[int, int]): Tuple containing the button number and the panel number
        """
        with self.lock:
            button = self.numToButton(buttonStatus[0])
            seat = self.numToSeat(buttonStatus[1])

            origState = self.model.getCurrentRoundState()
            self.logger.debug("origState: " + str(origState))

            # If the gamestate is preparing, any button press will ready the player
            if origState == GameState.PREPARING:
                player = self.model.getPlayerFromSeat(seat)
                if player is not None:
                    player.toggleReady()
                    self.view.setPlayerReady(seat, player.isReady)
                    self.logger.debug("Toggled ready for player: " + str(player))
                else:
                    self.logger.error("Tried to toggle ready on a non-existent player")
                # Starting a round
                if self.model.allReadyStatus():
                    # Remove the ready status text from all players in view
                    self.view.clearReadyStatusText()

                    # Update the view to say "Please put cards in and press deal confirm"
                    self.view.createPopup("Please put the cards in the turret", "Press the dealer confirmation button to continue")
                    # The turret call is blocking, so let's update the view before calling it
                    self.view.update()

                    # Call the blocking method for the turret, waiting for confirmation button
                    self.turret.waitForConfirmation()

                    # Once confirmed, we can clear the popup and start the round
                    self.view.clearPopups()

                    # If in state preparing, we just advance the round to start it
                    self.model.advanceRound()

            elif origState == GameState.POSTHAND:
                # If the gamestate is posthand, any button press will reset the round
                if self.model.resetRound():
                    self.view.resetRound()
                    self.view.updateFromModel()
            
            else:
                match button:
                    case Button.FOLD:
                        if self.model.inSettings:
                            # self.removePlayer(seat)
                            pass
                        else:
                            self.fold(seat)
                    case Button.CHECK:
                        if self.model.inSettings:
                            # self.addPlayer(seat)
                            pass
                        else:
                            self.check(seat)
                    case Button.CALL:
                        if self.model.inSettings:
                            # self.changeBlinds(seat)
                            pass
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
            self.logger.debug("newState: " + str(newState))
            self.logger.debug("game potsize: " + str(self.model.currentRound.potSize))

            if newState != origState:
                self.deal(newState)

            if newState != GameState.PREPARING:
                self.view.indicatePlayerTurn(self.model.currentRound.currentPlayer.seatNumber)

            self.updateViewText()

            # just debug a lot of shit
            self.logger.debug(str(self.model.currentRound.currentPlayer))

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
            self.logger.debug("Updated bet for player: " + str(seat))

    def resetBet(self, seat: Seat) -> None:
        # Based on input from the buttons for each player
        # Update the potential bet amount in the model
        # Update the bet amount displayed in the view
        if self.model.resetBet(seat):
            self.view.updatePlayerBet(seat, 0)
            self.logger.debug("Reset bet for player: " + str(seat))

    def makeBet(self, seat: Seat) -> None:
        # Based on input from the buttons for each player
        # Update the bet amount displayed in view
        # Update the model to reflect the bet amount
        success, amount = self.model.makeBet(seat)
        if success:
            self.view.updatePlayerBet(seat, amount)
            self.view.updatePlayerChips(seat, self.model.getPlayerFromSeat(seat).stackSize)
            self.view.updatePot(self.model.getPotSize())
            self.logger.debug("Made bet for player: " + str(seat))

    def fold(self, seat: Seat) -> None:
        # Based on input from the buttons for each player
        # Based on the seat mapping, updates model to fold those players
        # Update the view to reflect the fold
        if self.model.fold(seat):
            self.view.fold(seat)
            self.logger.debug("Folded player: " + str(seat))

    def check(self, seat: Seat) -> None:
        # Based on input from the buttons for each player
        # Based on the seat mapping, updates model to check those players
        # Update the view to reflect the check
        self.resetBet(seat)
        self.makeBet(seat)
        self.logger.debug("Checked player: " + str(seat))

    def call(self, seat: Seat) -> None:
        # Based on input from the buttons for each player
        # Based on the seat mapping, updates model to call those players
        success, amount = self.model.call(seat)
        if success:
            self.view.updatePlayerBet(seat, amount)
            self.view.updatePlayerChips(seat, self.model.getPlayerFromSeat(seat).stackSize)
            self.view.updatePot(self.model.getPotSize())
            self.logger.debug("Called player: " + str(seat))

    def ready(self, seat: Seat) -> None:
        # Based on input from the buttons for each player
        # Based on the seat mapping, updates model to ready those players
        # Update the view to reflect the ready
        self.model.ready(seat)

    def deal(self, state: GameState) -> None:
        self.logger.debug("Dealing cards")
        players = self.model.getPlayersInHand()
        match state:
            case GameState.PREFLOP:
                for i in range(2):
                    for player in players:
                        self.turret.dealToSeat(player.seatNumber)
                        self.view.dealPlayerCard(player.seatNumber, player.hand.getHoleCards()[i])
                self.view.indicatePlayerTurn(self.model.currentRound.currentPlayer.seatNumber)
            case GameState.FLOP:
                self.turret.dealDiscard(1)
                self.turret.dealFlop()
                self.view.dealBurn(self.model.currentRound.burnCards[0])
                self.view.dealFlop()
                self.view.indicatePlayerTurn(self.model.currentRound.currentPlayer.seatNumber)
            case GameState.TURN:
                self.turret.dealDiscard(1)
                self.turret.dealTurn()
                self.view.dealBurn(self.model.currentRound.burnCards[1])
                self.view.dealTurn()
                self.view.indicatePlayerTurn(self.model.currentRound.currentPlayer.seatNumber)
            case GameState.RIVER:
                self.turret.dealDiscard(1)
                self.turret.dealRiver()
                self.view.dealBurn(self.model.currentRound.burnCards[2])
                self.view.dealRiver()
                self.view.indicatePlayerTurn(self.model.currentRound.currentPlayer.seatNumber)
            case GameState.SHOWDOWN:
                # Have view display winner, wait for button confirmation from winner to end hand
                winners = self.model.currentRound.determineWinners()
                if len(winners) == 1:
                    self.view.createPopup(winners[0].name + " wins with " + str(winners[0].getHand().getRanking()) + " and gets " + str(self.model.getPotSize()) + " chips!", "Press any button to continue")
                else:
                    # Print out all the winners with their winning and the overall pot size
                    winnerString = ""
                    for winner in winners:
                        winnerString += winner.name + " with " + str(winner.getHand().getRanking()) + ", "
                    winnerString = winnerString[:-2]
                    self.view.createPopup(winnerString + " split the pot of " + str(self.model.getPotSize()) + " chips!", "Press any button to continue")
            case GameState.POSTHAND:
                remainingCards = self.model.getRemainingCards()
                self.turret.dealDiscard(remainingCards)
                self.view.createPopup("Please put the cards in the shuffler", "Press the shuffler confirmation button to continue")
                # Turret waits for confirmation from the shuffler and is blocking so update the view
                self.view.update()
                self.turret.waitForConfirmation()
                self.view.clearPopups()

    def updateViewText(self) -> None:
        # Update the pot size in the view based on the model
        self.view.updatePot(self.model.getPotSize(), growShrink=False)
        # Update each of the players' chips and bet amounts in the view based on the model
        for player in self.model.getPlayersInHand():
            self.view.updatePlayerChips(player.seatNumber, player.stackSize, growShrink=False)
            self.view.updatePlayerBet(player.seatNumber, player.potentialBet)
    
    def settings(self) -> None:
        # Toggle the settings menu
        self.model.toggleSettings()
        
        if self.model.inSettings:
            self.view.createPopup("Settings Menu Active", "Press settings button to return to game")
        else:
            self.view.clearPopups()

    def update(self) -> None:

        # Update the view to reflect the model
        with self.lock:
            view.update()

    def debug(self) -> None:
        print(str(self.model.currentRound))


if __name__ == "__main__":
    import pygame
    # Test code
    model = PokerGameModel()
    view = PokerGameView(model)
    turret = Turret("/dev/ttyACM0")
    
    controller = PokerGameController(model, view, turret)

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
                    # 0 represents settings
                    controller.buttonListener((0, playerNum))
                if event.key == pygame.K_2:
                    # 1 represents red chip
                    controller.buttonListener((1, playerNum))
                if event.key == pygame.K_3:
                    # 2 represents blue chip
                    controller.buttonListener((2, playerNum))
                if event.key == pygame.K_4:
                    # 3 represents white chip
                    controller.buttonListener((3, playerNum))
                if event.key == pygame.K_5:
                    # 4 represents fold
                    controller.buttonListener((4, playerNum))
                if event.key == pygame.K_6:
                    # 5 represents bet
                    controller.buttonListener((5, playerNum))
                if event.key == pygame.K_7:
                    # 6 represents check
                    controller.buttonListener((6, playerNum))
                if event.key == pygame.K_8:
                    # 7 represents call
                    controller.buttonListener((7, playerNum))
                if event.key == pygame.K_q:
                    playerNum = 0
                if event.key == pygame.K_w:
                    playerNum = 1
                if event.key == pygame.K_e:
                    playerNum = 2
                if event.key == pygame.K_r:
                    playerNum = 3
                if event.key == pygame.K_p:
                    controller.debug()

        controller.update()
