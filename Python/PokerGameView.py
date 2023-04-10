import pygame
import random
import logging
import sys
from PokerGameModel import PokerGameModel
from Sprites import *
from Card import Card
from Enums import *


class PokerGameView:
    # CONSTANTS
    FONT_PATH = "fonts/Designer.otf"
    FONT_COLOR = (0, 0, 0)
    POPUP_FONT_COLOR = (0, 0, 0)
    # Sizes denote the actual sizes/lengths
    # Positions denote the center of the object at a coordinate

    # Boundaries
    # Full monitor size: 1920x1080
    # Desired resolution: 1280x720
    SCREEN_SIZE = [1280, 720]
    TABLE_SIZE = [int(SCREEN_SIZE[0] * 4/5), SCREEN_SIZE[1]]
    MENU_SIZE = [int(SCREEN_SIZE[0] * 1/5), SCREEN_SIZE[1]]
    POPUP_SIZE = [int(0.5 * SCREEN_SIZE[1]), int(0.5 * SCREEN_SIZE[1])]

    # Sizes
    # Keeping it slightly to scale, table width is 60 inches, 
    # say card height is 5 inches and width is 2/3 of that
    CARD_SIZE = [int(TABLE_SIZE[0] * (5*2/3)/60), int(TABLE_SIZE[0] * 5/60)]
    FONT_HEIGHT = int(0.03 * TABLE_SIZE[1])
    POPUP_FONT_HEIGHT = int(0.1 * POPUP_SIZE[1])

    # Positions
    POPUP_POSITION = [int(SCREEN_SIZE[0]/2), int(SCREEN_SIZE[1]/2)]
    MENU_CORNER_POSITION = [TABLE_SIZE[0], 0]
    MENU_CENTER_POSITION = [int(MENU_CORNER_POSITION[0] + MENU_SIZE[0]/2), int(MENU_CORNER_POSITION[1] + FONT_HEIGHT)]
    TURRET_POSITION = [int(0.5 * TABLE_SIZE[0]), int(0.1 * TABLE_SIZE[1])]
    BURN_POSITION = [int(TURRET_POSITION[0] - 2 * CARD_SIZE[0]), TURRET_POSITION[1]]
    DEAL_POSITION = [int(TURRET_POSITION[0] + 2 * CARD_SIZE[0]), TURRET_POSITION[1]]

    COMMUNITY_3_POSITION = [int(TURRET_POSITION[0] + 0 * CARD_SIZE[0]), int(TURRET_POSITION[1] + 0.17 * TABLE_SIZE[1])]
    COMMUNITY_2_POSITION = [int(COMMUNITY_3_POSITION[0] - 1.25 * CARD_SIZE[0]), COMMUNITY_3_POSITION[1]]
    COMMUNITY_1_POSITION = [int(COMMUNITY_2_POSITION[0] - 1.25 * CARD_SIZE[0]), COMMUNITY_3_POSITION[1]]
    COMMUNITY_4_POSITION = [int(COMMUNITY_3_POSITION[0] + 1.25 * CARD_SIZE[0]), COMMUNITY_3_POSITION[1]]
    COMMUNITY_5_POSITION = [int(COMMUNITY_4_POSITION[0] + 1.25 * CARD_SIZE[0]), COMMUNITY_3_POSITION[1]]

    POT_POSITION = [int(TURRET_POSITION[0]), int(COMMUNITY_3_POSITION[1] + 0.75 * CARD_SIZE[1])]

    # The hub positions are center positions of the 4 player hubs which will have several sprites
    PLAYER_1_HUB_POSITION = [int(TURRET_POSITION[0] - 0.3 * TABLE_SIZE[0]), int(TURRET_POSITION[1] + 0.1 * TABLE_SIZE[1])]
    PLAYER_1_NAME_POSITION = [int(PLAYER_1_HUB_POSITION[0]), int(PLAYER_1_HUB_POSITION[1] - 0.75 * CARD_SIZE[1])]
    PLAYER_1_CARD_1_POSITION = [int(PLAYER_1_HUB_POSITION[0] - 0.6 * CARD_SIZE[0]), int(PLAYER_1_HUB_POSITION[1])]
    PLAYER_1_CARD_2_POSITION = [int(PLAYER_1_HUB_POSITION[0] + 0.6 * CARD_SIZE[0]), int(PLAYER_1_HUB_POSITION[1])]
    PLAYER_1_STACK_POSITION = [int(PLAYER_1_HUB_POSITION[0]), int(PLAYER_1_HUB_POSITION[1] + 0.75 * CARD_SIZE[1])]
    PLAYER_1_BET_POSITION = [int(PLAYER_1_HUB_POSITION[0]), int(PLAYER_1_STACK_POSITION[1] + 1.25 * FONT_HEIGHT)]
    PLAYER_1_BLIND_POSITION = [int(PLAYER_1_HUB_POSITION[0]), int(PLAYER_1_NAME_POSITION[1] - 1.25 * FONT_HEIGHT)]

    PLAYER_2_HUB_POSITION = [int(TURRET_POSITION[0] - 0.13 * TABLE_SIZE[0]), int(TURRET_POSITION[1] + 0.45 * TABLE_SIZE[1])]
    PLAYER_2_NAME_POSITION = [int(PLAYER_2_HUB_POSITION[0]), int(PLAYER_2_HUB_POSITION[1] - 0.75 * CARD_SIZE[1])]
    PLAYER_2_CARD_1_POSITION = [int(PLAYER_2_HUB_POSITION[0] - 0.6 * CARD_SIZE[0]), int(PLAYER_2_HUB_POSITION[1])]
    PLAYER_2_CARD_2_POSITION = [int(PLAYER_2_HUB_POSITION[0] + 0.6 * CARD_SIZE[0]), int(PLAYER_2_HUB_POSITION[1])]
    PLAYER_2_STACK_POSITION = [int(PLAYER_2_HUB_POSITION[0]), int(PLAYER_2_HUB_POSITION[1] + 0.75 * CARD_SIZE[1])]
    PLAYER_2_BET_POSITION = [int(PLAYER_2_HUB_POSITION[0]), int(PLAYER_2_STACK_POSITION[1] + 1.25 * FONT_HEIGHT)]
    PLAYER_2_BLIND_POSITION = [int(PLAYER_2_HUB_POSITION[0]), int(PLAYER_2_NAME_POSITION[1] - 1.25 * FONT_HEIGHT)]

    PLAYER_3_HUB_POSITION = [int(TURRET_POSITION[0] + 0.13 * TABLE_SIZE[0]), int(TURRET_POSITION[1] + 0.45 * TABLE_SIZE[1])]
    PLAYER_3_NAME_POSITION = [int(PLAYER_3_HUB_POSITION[0]), int(PLAYER_3_HUB_POSITION[1] - 0.75 * CARD_SIZE[1])]
    PLAYER_3_CARD_1_POSITION = [int(PLAYER_3_HUB_POSITION[0] - 0.6 * CARD_SIZE[0]), int(PLAYER_3_HUB_POSITION[1])]
    PLAYER_3_CARD_2_POSITION = [int(PLAYER_3_HUB_POSITION[0] + 0.6 * CARD_SIZE[0]), int(PLAYER_3_HUB_POSITION[1])]
    PLAYER_3_STACK_POSITION = [int(PLAYER_3_HUB_POSITION[0]), int(PLAYER_3_HUB_POSITION[1] + 0.75 * CARD_SIZE[1])]
    PLAYER_3_BET_POSITION = [int(PLAYER_3_HUB_POSITION[0]), int(PLAYER_3_STACK_POSITION[1] + 1.25 * FONT_HEIGHT)]
    PLAYER_3_BLIND_POSITION = [int(PLAYER_3_HUB_POSITION[0]), int(PLAYER_3_NAME_POSITION[1] - 1.25 * FONT_HEIGHT)]

    PLAYER_4_HUB_POSITION = [int(TURRET_POSITION[0] + 0.3 * TABLE_SIZE[0]), int(TURRET_POSITION[1] + 0.1 * TABLE_SIZE[1])]
    PLAYER_4_NAME_POSITION = [int(PLAYER_4_HUB_POSITION[0]), int(PLAYER_4_HUB_POSITION[1] - 0.75 * CARD_SIZE[1])]
    PLAYER_4_CARD_1_POSITION = [int(PLAYER_4_HUB_POSITION[0] - 0.6 * CARD_SIZE[0]), int(PLAYER_4_HUB_POSITION[1])]
    PLAYER_4_CARD_2_POSITION = [int(PLAYER_4_HUB_POSITION[0] + 0.6 * CARD_SIZE[0]), int(PLAYER_4_HUB_POSITION[1])]
    PLAYER_4_STACK_POSITION = [int(PLAYER_4_HUB_POSITION[0]), int(PLAYER_4_HUB_POSITION[1] + 0.75 * CARD_SIZE[1])]
    PLAYER_4_BET_POSITION = [int(PLAYER_4_HUB_POSITION[0]), int(PLAYER_4_STACK_POSITION[1] + 1.25 * FONT_HEIGHT)]
    PLAYER_4_BLIND_POSITION = [int(PLAYER_4_HUB_POSITION[0]), int(PLAYER_4_NAME_POSITION[1] - 1.25 * FONT_HEIGHT)]

    logger: logging.Logger
    model: PokerGameModel
    screen: pygame.Surface
    background: pygame.Surface
    backSprites: pygame.sprite.RenderUpdates # Sprite group for the background-related sprites
    burnSprites: pygame.sprite.RenderUpdates # Sprite group for the burn card sprites
    player1Sprites: pygame.sprite.RenderUpdates # Sprite group for non-card sprites of player 1
    player2Sprites: pygame.sprite.RenderUpdates # Sprite group for non-card sprites of player 2
    player3Sprites: pygame.sprite.RenderUpdates # Sprite group for non-card sprites of player 3
    player4Sprites: pygame.sprite.RenderUpdates # Sprite group for non-card sprites of player 4
    communitySprites: pygame.sprite.RenderUpdates # Sprite group for non-card sprites of the community cards
    player1CardSprites: pygame.sprite.RenderUpdates # Sprite group for card sprites of player 1
    player2CardSprites: pygame.sprite.RenderUpdates # Sprite group for card sprites of player 2
    player3CardSprites: pygame.sprite.RenderUpdates # Sprite group for card sprites of player 3
    player4CardSprites: pygame.sprite.RenderUpdates # Sprite group for card sprites of player 4
    communityCardSprites: pygame.sprite.RenderUpdates # Sprite group for card sprites of the community cards
    menuSprites: pygame.sprite.RenderUpdates # Sprite group for the menu-related sprites
    popupSprites: pygame.sprite.RenderUpdates # Sprite group for the popup-related sprites

    def __init__(self, model: PokerGameModel) -> None:
        # init the logger
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.StreamHandler(sys.stdout))
        self.logger.setLevel(logging.DEBUG)

        # init pygame
        pygame.init()

        # init the given model
        self.model = model

        # setup the screen and load the background
        self.screen = pygame.display.set_mode((self.SCREEN_SIZE[0], self.SCREEN_SIZE[1]), pygame.NOFRAME)
        self.background = pygame.Surface(self.SCREEN_SIZE)
        self.background = self.background.convert()
        self.background.fill((255, 255, 255))
        self.screen.blit(self.background, (0, 0))

        # Create the render updates groups for the sprite categories
        self.backSprites = pygame.sprite.RenderUpdates()
        self.burnSprites = pygame.sprite.RenderUpdates()
        self.player1Sprites = pygame.sprite.RenderUpdates()
        self.player2Sprites = pygame.sprite.RenderUpdates()
        self.player3Sprites = pygame.sprite.RenderUpdates()
        self.player4Sprites = pygame.sprite.RenderUpdates()
        self.communitySprites = pygame.sprite.RenderUpdates()
        self.player1CardSprites = pygame.sprite.RenderUpdates()
        self.player2CardSprites = pygame.sprite.RenderUpdates()
        self.player3CardSprites = pygame.sprite.RenderUpdates()
        self.player4CardSprites = pygame.sprite.RenderUpdates()
        self.communityCardSprites = pygame.sprite.RenderUpdates()
        self.menuSprites = pygame.sprite.RenderUpdates()
        self.popupSprites = pygame.sprite.RenderUpdates()

        # Add the table sprite to the background
        newSprite = TableSprite(self.TABLE_SIZE, self.backSprites)

        print("Screen size: " + str(self.screen.get_size()))

    def getPlayerPositions(self, seatNumber: Seat) -> dict[str, list[int]]:
        """
        Method to get the position constants corresponding to a player

        Args:
            seatNumber (Seat): The seat number of the player

        Returns:
            dict[str, list[int]]: The position constants for the player with options:
            "hub", "name", "card1", "card2", "stack", "bet", "blind"
        """
        if seatNumber == Seat.ONE:
            return {
                "hub": self.PLAYER_1_HUB_POSITION, 
                "name": self.PLAYER_1_NAME_POSITION, 
                "card1": self.PLAYER_1_CARD_1_POSITION, 
                "card2": self.PLAYER_1_CARD_2_POSITION, 
                "stack": self.PLAYER_1_STACK_POSITION, 
                "bet": self.PLAYER_1_BET_POSITION, 
                "blind": self.PLAYER_1_BLIND_POSITION
                }
        elif seatNumber == Seat.TWO:
            return {
                "hub": self.PLAYER_2_HUB_POSITION,
                "name": self.PLAYER_2_NAME_POSITION,
                "card1": self.PLAYER_2_CARD_1_POSITION,
                "card2": self.PLAYER_2_CARD_2_POSITION,
                "stack": self.PLAYER_2_STACK_POSITION,
                "bet": self.PLAYER_2_BET_POSITION,
                "blind": self.PLAYER_2_BLIND_POSITION
                }
        elif seatNumber == Seat.THREE:
            return {
                "hub": self.PLAYER_3_HUB_POSITION,
                "name": self.PLAYER_3_NAME_POSITION,
                "card1": self.PLAYER_3_CARD_1_POSITION,
                "card2": self.PLAYER_3_CARD_2_POSITION,
                "stack": self.PLAYER_3_STACK_POSITION,
                "bet": self.PLAYER_3_BET_POSITION,
                "blind": self.PLAYER_3_BLIND_POSITION
                }
        elif seatNumber == Seat.FOUR:
            return {
                "hub": self.PLAYER_4_HUB_POSITION,
                "name": self.PLAYER_4_NAME_POSITION,
                "card1": self.PLAYER_4_CARD_1_POSITION,
                "card2": self.PLAYER_4_CARD_2_POSITION,
                "stack": self.PLAYER_4_STACK_POSITION,
                "bet": self.PLAYER_4_BET_POSITION,
                "blind": self.PLAYER_4_BLIND_POSITION
                }
        
    def getPlayerGroup(self, seatNumber: Seat) -> pygame.sprite.Group:
        """
        Method to get the non-card sprite group for a player

        Args:
            seatNumber (Seat): The seat number of the player

        Returns:
            pygame.sprite.Group: The sprite group for the player
        """
        if seatNumber == Seat.ONE:
            return self.player1Sprites
        elif seatNumber == Seat.TWO:
            return self.player2Sprites
        elif seatNumber == Seat.THREE:
            return self.player3Sprites
        elif seatNumber == Seat.FOUR:
            return self.player4Sprites
        
    def getPlayerCardGroup(self, seatNumber: Seat) -> pygame.sprite.Group:
        """
        Method to get the card sprite group for a player

        Args:
            seatNumber (Seat): The seat number of the player

        Returns:
            pygame.sprite.Group: The sprite group for the player
        """
        if seatNumber == Seat.ONE:
            return self.player1CardSprites
        elif seatNumber == Seat.TWO:
            return self.player2CardSprites
        elif seatNumber == Seat.THREE:
            return self.player3CardSprites
        elif seatNumber == Seat.FOUR:
            return self.player4CardSprites
        
    def createFromModel(self) -> None:
        """
        Method to create the sprites from the model
        """
        currentRound = self.model.currentRound

        # Create the pot
        self.createPot()
        self.updatePot(currentRound.potSize)

        # Create the player hubs
        for player in currentRound.players:
            self.createPlayerHub(player.seatNumber)
            self.updatePlayerChips(player.seatNumber, player.stackSize)
            self.updatePlayerBet(player.seatNumber, player.potentialBet)
            self.updatePlayerName(player.seatNumber, player.name)
            self.setPlayerReady(player.seatNumber, player.isReady)

        # Assign the small and big blind
        self.setBlind(currentRound.getSmallBlindPlayer().seatNumber, Blind.SB)
        self.setBlind(currentRound.getBigBlindPlayer().seatNumber, Blind.BB)

    def updateFromModel(self) -> None:
        """
        Method to update the sprites from the model
        """
        currentRound = self.model.currentRound

        # Update the pot
        self.updatePot(currentRound.potSize)

        # Update the player hubs
        for player in currentRound.players:
            self.updatePlayerChips(player.seatNumber, player.stackSize)
            self.updatePlayerBet(player.seatNumber, player.potentialBet)
            self.updatePlayerName(player.seatNumber, player.name)
            self.setPlayerReady(player.seatNumber, player.isReady)

        # Update the small and big blind
        self.setBlind(currentRound.getSmallBlindPlayer().seatNumber, Blind.SB)
        self.setBlind(currentRound.getBigBlindPlayer().seatNumber, Blind.BB)
        
    # TODO: Method to display the menu
    # Update the text menu items based on the model
    # or have the item to be updated passed as an arg but makes more sense to have the model passed

    def createPot(self) -> None:
        """
        Method to create the pot. 
        The pot sprite will be the first sprite in the community group.
        """
        # The pot group should be empty
        # If it isn't, log an error and return
        if len(self.communitySprites) > 0:
            logging.error("Trying to create a pot for a non-empty layer group")
            return

        # Create the text for the pot
        newSprite = TextSprite("Pot: 0", self.FONT_PATH, self.FONT_HEIGHT, self.FONT_COLOR, self.POT_POSITION, self.communitySprites)
        newSprite = None

    def createBetToMatch(self) -> None:
        """
        Method to create the bet to match. 
        The bet to match sprite will be the second sprite in the community group.
        """
        # The bet to match group should be empty
        # If it isn't, log an error and return
        if len(self.communitySprites) > 1:
            logging.error("Trying to create a bet to match for a non-empty layer group")
            return

        # Create the text for the bet to match
        newSprite = TextSprite("Bet to Match: 0", self.FONT_PATH, self.FONT_HEIGHT, self.FONT_COLOR, self.BET_TO_MATCH_POSITION, self.communitySprites)
        newSprite = None
    
    def createPlayerHub(self, seatNumber: Seat) -> None:
        """
        Method to create a player hub (the non-card sprites).
        The player name sprite will be the first sprite in the player group.
        The player chips sprite will be the second sprite in the player group.
        The player bet sprite will be the third sprite in the player group.

        Args:
            seatNumber (Seat): The seat number of the player
        """
        # Get the positions for the player
        positions = self.getPlayerPositions(seatNumber)

        # Get the non-card sprite group for the player
        playerGroup = self.getPlayerGroup(seatNumber)

        # The player group should be empty
        # If it isn't, log an error and return
        if len(playerGroup) > 0:
            logging.error("Trying to create a player hub for a non-empty layer group")
            return

        # Create the text for the player name
        newSprite = TextSprite("Player", self.FONT_PATH, self.FONT_HEIGHT, self.FONT_COLOR, positions["name"], playerGroup)
        newSprite = None

        # Create the text for the player chips
        newSprite = TextSprite("Chips: 1000", self.FONT_PATH, self.FONT_HEIGHT, self.FONT_COLOR, positions["stack"], playerGroup)
        newSprite = None

        # Create the text for the player bet
        newSprite = TextSprite("Bet: 0", self.FONT_PATH, self.FONT_HEIGHT, self.FONT_COLOR, positions["bet"], playerGroup)
        newSprite = None

    def removePlayerHub(self, seatNumber: Seat) -> None:
        """
        Method to remove a player hub (the non-card sprites)

        Args:
            seatNumber (Seat): The seat number of the player
        """
        # Get the non-card sprite group for the player
        playerGroup = self.getPlayerGroup(seatNumber)

        # Remove all the sprites from the group
        playerGroup.empty()

    def removePlayerCards(self, seatNumber: Seat) -> None:
        """
        Method to remove a player's cards

        Args:
            seatNumber (Seat): The seat number of the player
        """
        # Get the card sprite group for the player
        playerGroup = self.getPlayerCardGroup(seatNumber)

        # Remove all the sprites from the group
        playerGroup.empty()

    def addPlayer(self, seatNumber: Seat) -> None:
        """
        Method to add a player to the game

        Args:
            seatNumber (Seat): The seat number of the player
        """
        self.createPlayerHub(seatNumber)

    def removePlayer(self, seatNumber: Seat) -> None:
        """
        Method to remove a player from the game

        Args:
            seatNumber (Seat): The seat number of the player
        """
        self.removePlayerHub(seatNumber)
        self.removePlayerCards(seatNumber)

    def setBlind(self, seatNumber: Seat, blindType: Blind) -> None:
        """
        Method to set the blind for a player.
        The player blind sprite will be the fourth sprite in the player group.

        Args:
            seatNumber (Seat): The seat number of the player
            blindType (Blind): The blind type
        """
        # Get the positions for the player
        positions = self.getPlayerPositions(seatNumber)

        # Get the sprite group for the player
        playerGroup = self.getPlayerGroup(seatNumber)

        # The player group should be created and have exactly 3 sprites
        # If it isn't, log an error and return
        if len(playerGroup) != 3:
            logging.error("Trying to set a blind for a player with an invalid number of sprites")
            return

        # Create the text for the player blind
        newSprite = TextSprite(blindType.name, self.FONT_PATH, self.FONT_HEIGHT, self.FONT_COLOR, positions["blind"], playerGroup)
        newSprite = None

    def removeBlind(self, seatNumber: Seat) -> None:
        """
        Method to remove the blind for a player

        Args:
            seatNumber (Seat): The seat number of the player
        """
        # Get the sprite group for the player
        playerGroup = self.getPlayerGroup(seatNumber)

        # The player group should be created and have exactly 4 sprites
        # If it isn't, log an error and return
        if len(playerGroup) != 4:
            logging.error("Trying to remove a blind for a player with an invalid number of sprites")
            return

        # Remove the blind sprite
        playerGroup.remove(playerGroup.sprites()[3])

    def clearReadyStatusText(self) -> None:
        """
        Method to clear the ready states for all players
        """
        currentRound = self.model.currentRound

        for player in currentRound.players:
            self.updatePlayerName(player.seatNumber, player.name)

    def setPlayerReady(self, seatNumber: Seat, status: bool) -> None:
        """
        Method to toggle the ready state for a player

        Args:
            seatNumber (Seat): The seat number of the player
            status (bool): The ready state
        """
        # Get the sprite group for the player
        playerGroup = self.getPlayerGroup(seatNumber)

        if len(playerGroup) == 0:
            logging.error("Trying to toggle the ready state for an empty player group")
            return

        # Get the player name text sprite - at index 0
        playerNameSprite = playerGroup.sprites()[0]

        # Toggle the ready state
        statusText = " (Ready)" if status else " (Not Ready)"

        # Find within the sprite text if there's already a status text in ()
        # If there is, remove it
        if " (" in playerNameSprite.text:
            playerNameSprite.text = playerNameSprite.text[:playerNameSprite.text.find(" (")]

        # Update the text
        self.updatePlayerName(seatNumber, playerNameSprite.text + statusText)

    def updatePlayerName(self, seatNumber: Seat, newName: str, growShrink: bool = False) -> None:
        """
        Method to update the player name

        Args:
            seatNumber (Seat): The seat number of the player
            newName (str): The new name
        """

        # Get the sprite group for the player
        playerGroup = self.getPlayerGroup(seatNumber)

        if len(playerGroup) == 0:
            logging.error("Trying to update the player name for an empty player group")
            return

        # Get the player name text sprite - at index 0
        playerNameSprite = playerGroup.sprites()[0]

        # Update the text
        playerNameSprite.write(newName)

        # Grow and shrink the text if needed
        if growShrink:
            playerNameSprite.growShrinkOnce()

    def updatePlayerChips(self, seatNumber: Seat, newChipValue: int, growShrink: bool = True) -> None:
        """
        Method to update the player chips

        Args:
            seatNumber (Seat): The seat number of the player
            newChipValue (int): The new chip value
        """

        # Get the sprite group for the player
        playerGroup = self.getPlayerGroup(seatNumber)

        if len(playerGroup) == 0:
            logging.error("Trying to update the player chips for an empty player group")
            return

        # Get the player chips text sprite - at index 1
        playerChipsSprite = playerGroup.sprites()[1]

        # Update the text
        playerChipsSprite.write("Chips: " + str(newChipValue))

        # Grow and shrink the text if needed
        if growShrink:
            playerChipsSprite.growShrinkOnce()

    def updatePlayerBet(self, seatNumber: Seat, newBetValue: int) -> None:
        """
        Method to update the player bet

        Args:
            seatNumber (Seat): The seat number of the player
            newBetValue (int): The new bet value
        """

        # Get the sprite group for the player
        playerGroup = self.getPlayerGroup(seatNumber)

        if len(playerGroup) == 0:
            logging.error("Trying to update the player bet for an empty player group")
            return

        # Get the player bet text sprite - at index 2
        playerBetSprite = playerGroup.sprites()[2]

        # Update the text
        playerBetSprite.write("Bet: " + str(newBetValue))

    # TODO: Method to confirm the player bet
    # Needs to be passed the seat number of the player
    # Should display the bet text moving to the pot
    # Should also update the player chips and bet text
    def confirmPlayerBet(self, seatNumber: Seat) -> None:
        raise NotImplementedError("confirmPlayerBet not implemented")

    def updatePot(self, newPotValue: int, growShrink: bool = True) -> None:
        """
        Method to update the pot

        Args:
            newPotValue (int): The new pot value
        """

        if len(self.communitySprites) == 0:
            logging.error("Trying to update the pot for an empty community sprite group")
            return

        # Get the pot text sprite - at index 0
        potSprite = self.communitySprites.sprites()[0]

        # Update the text
        potSprite.write("Pot: " + str(newPotValue))

        # Grow and shrink the text if needed
        if growShrink:
            potSprite.growShrinkOnce()

    def dealBurn(self, card: Card) -> None:
        """
        Method to deal a card to the burn pile.

        Args:
            card (Card): The card to deal
        """
        # Create the burn card sprite
        newSprite = CardSprite(card, self.CARD_SIZE, self.TURRET_POSITION, self.BURN_POSITION, showCard=False, group=self.burnSprites)
        newSprite = None

    def fold(self, seatNumber: Seat) -> None:
        """
        Method to fold a player. Moves the player's cards to the burn pile.

        Args:
            seatNumber (Seat): The seat number of the player
        """
        # Get the player group
        playerCardGroup = self.getPlayerCardGroup(seatNumber)

        # Get the player card sprites
        playerCardSprites = playerCardGroup.sprites()

        # Move the card sprites to the burn pile
        for cardSprite in playerCardSprites:
            cardSprite.moveTo(self.BURN_POSITION)
            cardSprite.add(self.burnSprites)
            cardSprite.remove(playerCardGroup)

    def dealFlop(self) -> None:
        """
        Method to deal the flop
        """
        # Get the community cards from the model
        communityCards = self.model.getCommunityCards()
        # Ensure there are 3 cards
        if len(communityCards) < 3:
            self.logger.error("Not enough community cards to deal flop")
            return
        # Ensure there are no cards in the community card sprite group
        if len(self.communityCardSprites) > 0:
            self.logger.error("Trying to deal flop when there are already cards in the community card sprite group")
            return
        # Deal the first card
        newSprite = CardSprite(communityCards[0], self.CARD_SIZE, self.TURRET_POSITION, self.COMMUNITY_1_POSITION, showCard=True, group=self.communityCardSprites)
        newSprite = None
        # Deal the second card
        newSprite = CardSprite(communityCards[1], self.CARD_SIZE, self.TURRET_POSITION, self.COMMUNITY_2_POSITION, showCard=True, group=self.communityCardSprites)
        newSprite = None
        # Deal the third card
        newSprite = CardSprite(communityCards[2], self.CARD_SIZE, self.TURRET_POSITION, self.COMMUNITY_3_POSITION, showCard=True, group=self.communityCardSprites)
        newSprite = None

    def dealTurn(self) -> None:
        """
        Method to deal the turn
        """
        # Get the community cards from the model
        communityCards = self.model.getCommunityCards()
        # Ensure there are 4 cards
        if len(communityCards) < 4:
            self.logger.error("Not enough community cards to deal turn")
            return
        # Ensure there are 3 cards in the community card sprite group
        if len(self.communityCardSprites) != 3:
            self.logger.error("Trying to deal turn when there are not 3 cards in the community card sprite group")
            return
        # Deal the card
        newSprite = CardSprite(communityCards[3], self.CARD_SIZE, self.TURRET_POSITION, self.COMMUNITY_4_POSITION, showCard=True, group=self.communityCardSprites)

    def dealRiver(self) -> None:
        """
        Method to deal the river
        """
        # Get the community cards from the model
        communityCards = self.model.getCommunityCards()
        # Ensure there are 5 cards
        if len(communityCards) < 5:
            self.logger.error("Not enough community cards to deal river")
            return
        # Ensure there are 4 cards in the community card sprite group
        if len(self.communityCardSprites) != 4:
            self.logger.error("Trying to deal river when there are not 4 cards in the community card sprite group")
            return
        # Deal the card
        newSprite = CardSprite(communityCards[4], self.CARD_SIZE, self.TURRET_POSITION, self.COMMUNITY_5_POSITION, showCard=True, group=self.communityCardSprites)

    def dealPlayerCard(self, seatNumber: Seat, card: Card) -> None:
        """
        Method to deal a card to a player. Does not deal the card if the player already has two cards

        Args:
            seatNumber (Seat): The seat number of the player
            card (Card): The card to be dealt
        """
        # Get the position of the card
        playerCardGroup = self.getPlayerCardGroup(seatNumber)
        playerPositions = self.getPlayerPositions(seatNumber)
        cardPosition = [0, 0]
        # If the player has no cards, deal the first card
        if len(playerCardGroup) == 0:
            cardPosition = playerPositions["card1"]
        # If the player has one card, deal the second card
        elif len(playerCardGroup) == 1:
            cardPosition = playerPositions["card2"]
        # If the player has two or more cards, throw an error and don't deal the card
        else:
            self.logger.error("Trying to deal a card to a player who already has two cards")
            return
        # Deal the card
        newSprite = CardSprite(card, self.CARD_SIZE, self.TURRET_POSITION, cardPosition, showCard=True, group=playerCardGroup)

    # TODO: Method to indicate the player is the winner
    # Needs to be passed the player number
    # Displays the winner text for that player

    def resetPlayerTurns(self) -> None:
        """
        Method to reset the player turn indicators
        """
        # Iterate through the player groups
        for seatNumber in Seat:
            # Get the sprite group for the player
            playerGroup = self.getPlayerGroup(seatNumber)
            if len(playerGroup) == 0:
                continue
            # Get the player name text sprite - at index 0
            playerNameSprite = playerGroup.sprites()[0]
            # Reset the player name text sprite
            playerNameSprite.growShrinkReset()

    def indicatePlayerTurn(self, seatNumber: Seat) -> None:
        """
        Method to indicate the player turn

        Args:
            seatNumber (Seat): The seat number of the player
        """
        # First reset the player turns
        self.resetPlayerTurns()

        # Get the sprite group for the player
        playerGroup = self.getPlayerGroup(seatNumber)

        if len(playerGroup) == 0:
            logging.error("Trying to indicate player turn for a player who doesn't exist")
            return

        # Get the player name text sprite - at index 0
        playerNameSprite = playerGroup.sprites()[0]

        # Indicate the player turn
        playerNameSprite.growShrinkRepeat()

    def findCardSprite(self, card: Card) -> CardSprite:
        """
        Method to find the card sprite for a card. Cards should only be in the player card groups or the community card group.
        Returns None if the card is not found

        Args:
            card (Card): The card to find the sprite for

        Returns:
            CardSprite: The card sprite
        """
        for sprite in self.player1CardSprites:
            if sprite.getCard().isSameCard(card):
                return sprite
        for sprite in self.player2CardSprites:
            if sprite.getCard().isSameCard(card):
                return sprite
        for sprite in self.player3CardSprites:
            if sprite.getCard().isSameCard(card):
                return sprite
        for sprite in self.player4CardSprites:
            if sprite.getCard().isSameCard(card):
                return sprite
        for sprite in self.communityCardSprites:
            if sprite.getCard().isSameCard(card):
                return sprite
        return None

    def flipCard(self, card: Card) -> None:
        """
        Method to flip a card

        Args:
            card (Card): The card to be flipped
        """
        cardSprite = self.findCardSprite(card)
        if cardSprite is None:
            self.logger.error("Unable to find the card sprite to flip for card " + str(card))
            return
        cardSprite.flip()

    def resetRound(self) -> None:
        """
        Method to reset the round. 

        Removes all cards from the screen,
        resets the pot, 
        resets the player bets,
        removes the blinds,
        """

        # Remove the cards
        self.player1CardSprites.empty()
        self.player2CardSprites.empty()
        self.player3CardSprites.empty()
        self.player4CardSprites.empty()
        self.communityCardSprites.empty()
        self.burnSprites.empty()

        # Reset the pot
        self.updatePot(0)

        # Reset the player bets
        if len(self.player1Sprites) > 0:
            self.updatePlayerBet(Seat.ONE, 0)
        if len(self.player2Sprites) > 0:
            self.updatePlayerBet(Seat.TWO, 0)
        if len(self.player3Sprites) > 0:
            self.updatePlayerBet(Seat.THREE, 0)
        if len(self.player4Sprites) > 0:
            self.updatePlayerBet(Seat.FOUR, 0)

        # Remove the blinds
        # If a player has the blind sprite, it will be the fourth sprite in the group
        if len(self.player1Sprites) > 3:
            self.player1Sprites.remove(self.player1Sprites.sprites()[3])
        if len(self.player2Sprites) > 3:
            self.player2Sprites.remove(self.player2Sprites.sprites()[3])
        if len(self.player3Sprites) > 3:
            self.player3Sprites.remove(self.player3Sprites.sprites()[3])
        if len(self.player4Sprites) > 3:
            self.player4Sprites.remove(self.player4Sprites.sprites()[3])

        self.resetPlayerTurns()

    def createPopup(self, text: str) -> None:
        """
        Method to create a popup

        Args:
            text (str): The text to display in the popup
        """
        # Create the popup
        popup = PopUpWindow(text, self.FONT_PATH, self.POPUP_FONT_HEIGHT, self.FONT_COLOR, self.POPUP_POSITION, self.POPUP_SIZE, self.popupSprites)

    def clearPopups(self) -> None:
        """
        Method to clear all popups
        """
        self.popupSprites.empty()


    def update(self) -> None:
        
        # Clear the sprites on screen
        self.backSprites.clear(self.screen, self.background)
        self.burnSprites.clear(self.screen, self.background)
        self.player1Sprites.clear(self.screen, self.background)
        self.player2Sprites.clear(self.screen, self.background)
        self.player3Sprites.clear(self.screen, self.background)
        self.player4Sprites.clear(self.screen, self.background)
        self.communitySprites.clear(self.screen, self.background)
        self.player1CardSprites.clear(self.screen, self.background)
        self.player2CardSprites.clear(self.screen, self.background)
        self.player3CardSprites.clear(self.screen, self.background)
        self.player4CardSprites.clear(self.screen, self.background)
        self.communityCardSprites.clear(self.screen, self.background)
        self.menuSprites.clear(self.screen, self.background)
        self.popupSprites.clear(self.screen, self.background)

        seconds = 60

        # Update the sprites giving the time
        self.backSprites.update(seconds)
        self.burnSprites.update(seconds)
        self.player1Sprites.update(seconds)
        self.player2Sprites.update(seconds)
        self.player3Sprites.update(seconds)
        self.player4Sprites.update(seconds)
        self.communitySprites.update(seconds)
        self.player1CardSprites.update(seconds)
        self.player2CardSprites.update(seconds)
        self.player3CardSprites.update(seconds)
        self.player4CardSprites.update(seconds)
        self.communityCardSprites.update(seconds)
        self.menuSprites.update(seconds)
        self.popupSprites.update(seconds)

        # Draw the sprites on screen
        dirtyRects = self.backSprites.draw(self.screen)
        dirtyRects += self.burnSprites.draw(self.screen)
        dirtyRects += self.player1Sprites.draw(self.screen)
        dirtyRects += self.player2Sprites.draw(self.screen)
        dirtyRects += self.player3Sprites.draw(self.screen)
        dirtyRects += self.player4Sprites.draw(self.screen)
        dirtyRects += self.communitySprites.draw(self.screen)
        dirtyRects += self.player1CardSprites.draw(self.screen)
        dirtyRects += self.player2CardSprites.draw(self.screen)
        dirtyRects += self.player3CardSprites.draw(self.screen)
        dirtyRects += self.player4CardSprites.draw(self.screen)
        dirtyRects += self.communityCardSprites.draw(self.screen)
        dirtyRects += self.menuSprites.draw(self.screen)
        dirtyRects += self.popupSprites.draw(self.screen)

        pygame.display.update(dirtyRects)


if __name__ == "__main__":
    # Test code
    view = PokerGameView(PokerGameModel())
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                # w key moves card backs to each community position
                if event.key == pygame.K_w:
                    view.testDealCommunity(False)
                # s key moves card fronts to each community position
                if event.key == pygame.K_s:
                    view.testDealCommunity(True)
                # e key moves card backs to each player position
                if event.key == pygame.K_e:
                    view.testDealPlayer(False)
                # d key moves card fronts to each player position
                if event.key == pygame.K_d:
                    view.testDealPlayer(True)
                # q key displays the text
                if event.key == pygame.K_q:
                    view.testPlayerText()
                # r key displays the other text
                if event.key == pygame.K_r:
                    view.testDrawOther()
                # t key displays the menu text
                if event.key == pygame.K_t:
                    view.testDrawMenu()
                # y key calls the player menu method
                if event.key == pygame.K_y:
                    view.createPlayerHub(Seat.ONE)
                # u key calls the update chips method
                if event.key == pygame.K_u:
                    view.updatePlayerChips(Seat.ONE, 100)
                # i key calls the update bet method
                if event.key == pygame.K_i:
                    view.updatePlayerBet(Seat.ONE, 100)
                # o key calls the create pot method
                if event.key == pygame.K_o:
                    view.createPot()
                # p key calls the update pot method
                if event.key == pygame.K_p:
                    view.updatePot(100)
                # v key deals a queen of hearts to player 1
                if event.key == pygame.K_v:
                    view.dealPlayerCard(Seat.ONE, Card(Value.QUEEN, Suit.HEART))
                # b key deals an ace of spades to player 2
                if event.key == pygame.K_b:
                    view.dealPlayerCard(Seat.TWO, Card(Value.ACE, Suit.SPADE))
                # n key flips the queen of hearts
                if event.key == pygame.K_n:
                    view.flipCard(Card(Value.QUEEN, Suit.HEART))
                # m key flips the ace of spades
                if event.key == pygame.K_m:
                    view.flipCard(Card(Value.ACE, Suit.SPADE))
                # c key calls the reset method
                if event.key == pygame.K_c:
                    view.resetRound()
                # x key calls the clear popups method
                if event.key == pygame.K_x:
                    view.clearPopups()
                # z key calls the create popup method
                if event.key == pygame.K_z:
                    view.createPopup("Place cards in shuffler")
                # a key calls the fold method
                if event.key == pygame.K_a:
                    view.fold(Seat.ONE)

        view.update()