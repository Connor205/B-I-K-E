import pygame
import random
from typing import Tuple
from PokerGameModel import PokerGameModel
from Sprites import *
from Card import Card
from Enums import *
class PokerGameView:
    # CONSTANTS
    # Sizes denote the actual sizes/lengths
    # Positions denote the center of the object at a coordinate

    # Boundaries
    # Full monitor size: 1920x1080
    # Desired resolution: 1280x720
    SCREEN_SIZE = [1280, 720]
    TABLE_SIZE = [int(SCREEN_SIZE[0] * 4/5), SCREEN_SIZE[1]]
    MENU_SIZE = [int(SCREEN_SIZE[0] * 1/5), SCREEN_SIZE[1]]

    # Sizes
    # Keeping it slightly to scale, table width is 60 inches, 
    # say card height is 5 inches and width is 2/3 of that
    CARD_SIZE = [int(TABLE_SIZE[0] * (5*2/3)/60), int(TABLE_SIZE[0] * 5/60)]
    FONT_HEIGHT = int(TABLE_SIZE[1] * 1/30)

    # Positions
    MENU_CORNER_POSITION = [TABLE_SIZE[0], 0]
    MENU_CENTER_POSITION = [int(MENU_CORNER_POSITION[0] + MENU_SIZE[0]/2), int(MENU_CORNER_POSITION[1] + FONT_HEIGHT)]
    TURRET_POSITION = [int(0.5 * TABLE_SIZE[0]), int(0.1 * TABLE_SIZE[1])]
    BURN_POSITION = [int(TURRET_POSITION[0] - 2 * CARD_SIZE[0]), TURRET_POSITION[1]]
    DEAL_POSITION = [int(TURRET_POSITION[0] + 2 * CARD_SIZE[0]), TURRET_POSITION[1]]

    COMMUNITY_3_POSITION = [int(TURRET_POSITION[0] + 0 * CARD_SIZE[0]), int(TURRET_POSITION[1] + 0.2 * TABLE_SIZE[1])]
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

    PLAYER_2_HUB_POSITION = [int(TURRET_POSITION[0] - 0.2 * TABLE_SIZE[0]), int(TURRET_POSITION[1] + 0.5 * TABLE_SIZE[1])]
    PLAYER_2_NAME_POSITION = [int(PLAYER_2_HUB_POSITION[0]), int(PLAYER_2_HUB_POSITION[1] - 0.75 * CARD_SIZE[1])]
    PLAYER_2_CARD_1_POSITION = [int(PLAYER_2_HUB_POSITION[0] - 0.6 * CARD_SIZE[0]), int(PLAYER_2_HUB_POSITION[1])]
    PLAYER_2_CARD_2_POSITION = [int(PLAYER_2_HUB_POSITION[0] + 0.6 * CARD_SIZE[0]), int(PLAYER_2_HUB_POSITION[1])]
    PLAYER_2_STACK_POSITION = [int(PLAYER_2_HUB_POSITION[0]), int(PLAYER_2_HUB_POSITION[1] + 0.75 * CARD_SIZE[1])]
    PLAYER_2_BET_POSITION = [int(PLAYER_2_HUB_POSITION[0]), int(PLAYER_2_STACK_POSITION[1] + 1.25 * FONT_HEIGHT)]
    PLAYER_2_BLIND_POSITION = [int(PLAYER_2_HUB_POSITION[0]), int(PLAYER_2_NAME_POSITION[1] - 1.25 * FONT_HEIGHT)]

    PLAYER_3_HUB_POSITION = [int(TURRET_POSITION[0] + 0.2 * TABLE_SIZE[0]), int(TURRET_POSITION[1] + 0.5 * TABLE_SIZE[1])]
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

    model: PokerGameModel
    screen: pygame.Surface
    background: pygame.Surface
    font: pygame.font.Font
    fontColor: Tuple[int, int, int]
    backSprites: pygame.sprite.RenderUpdates
    playerSprites: pygame.sprite.RenderUpdates
    communitySprites: pygame.sprite.RenderUpdates
    menuSprites: pygame.sprite.RenderUpdates

    def __init__(self, model) -> None:
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

        # load the font
        self.font = pygame.font.Font(None, self.FONT_HEIGHT)
        self.fontColor = [0, 0, 0]

        # Create the render updates groups for the sprite categories
        self.backSprites = pygame.sprite.RenderUpdates()
        self.playerSprites = pygame.sprite.RenderUpdates()
        self.communitySprites = pygame.sprite.RenderUpdates()
        self.menuSprites = pygame.sprite.RenderUpdates()

        # Add the table sprite to the background
        newSprite = TableSprite(self.TABLE_SIZE, self.backSprites)

        print("Screen size: " + str(self.screen.get_size()))

    def testDealCommunity(self, show: bool) -> None:
        # Create five random cards to test each community card position
        card = Card(random.choice(list(Value)), random.choice(list(Suit)))
        newSprite = CardSprite(card, self.CARD_SIZE, self.TURRET_POSITION, self.COMMUNITY_1_POSITION, showCard=show, group=self.communitySprites)
        newSprite = None
        card = Card(random.choice(list(Value)), random.choice(list(Suit)))
        newSprite = CardSprite(card, self.CARD_SIZE, self.TURRET_POSITION, self.COMMUNITY_2_POSITION, showCard=show, group=self.communitySprites)
        newSprite = None
        card = Card(random.choice(list(Value)), random.choice(list(Suit)))
        newSprite = CardSprite(card, self.CARD_SIZE, self.TURRET_POSITION, self.COMMUNITY_3_POSITION, showCard=show, group=self.communitySprites)
        newSprite = None
        card = Card(random.choice(list(Value)), random.choice(list(Suit)))
        newSprite = CardSprite(card, self.CARD_SIZE, self.TURRET_POSITION, self.COMMUNITY_4_POSITION, showCard=show, group=self.communitySprites)
        newSprite = None
        card = Card(random.choice(list(Value)), random.choice(list(Suit)))
        newSprite = CardSprite(card, self.CARD_SIZE, self.TURRET_POSITION, self.COMMUNITY_5_POSITION, showCard=show, group=self.communitySprites)
        newSprite = None
    
    def testDealPlayer(self, show: bool) -> None:
        # Create eight random cards to test each player position
        card = Card(random.choice(list(Value)), random.choice(list(Suit)))
        newSprite = CardSprite(card, self.CARD_SIZE, self.TURRET_POSITION, self.PLAYER_1_CARD_1_POSITION, showCard=show, group=self.playerSprites)
        newSprite = None
        card = Card(random.choice(list(Value)), random.choice(list(Suit)))
        newSprite = CardSprite(card, self.CARD_SIZE, self.TURRET_POSITION, self.PLAYER_1_CARD_2_POSITION, showCard=show, group=self.playerSprites)
        newSprite = None
        card = Card(random.choice(list(Value)), random.choice(list(Suit)))
        newSprite = CardSprite(card, self.CARD_SIZE, self.TURRET_POSITION, self.PLAYER_2_CARD_1_POSITION, showCard=show, group=self.playerSprites)
        newSprite = None
        card = Card(random.choice(list(Value)), random.choice(list(Suit)))
        newSprite = CardSprite(card, self.CARD_SIZE, self.TURRET_POSITION, self.PLAYER_2_CARD_2_POSITION, showCard=show, group=self.playerSprites)
        newSprite = None
        card = Card(random.choice(list(Value)), random.choice(list(Suit)))
        newSprite = CardSprite(card, self.CARD_SIZE, self.TURRET_POSITION, self.PLAYER_3_CARD_1_POSITION, showCard=show, group=self.playerSprites)
        newSprite = None
        card = Card(random.choice(list(Value)), random.choice(list(Suit)))
        newSprite = CardSprite(card, self.CARD_SIZE, self.TURRET_POSITION, self.PLAYER_3_CARD_2_POSITION, showCard=show, group=self.playerSprites)
        newSprite = None
        card = Card(random.choice(list(Value)), random.choice(list(Suit)))
        newSprite = CardSprite(card, self.CARD_SIZE, self.TURRET_POSITION, self.PLAYER_4_CARD_1_POSITION, showCard=show, group=self.playerSprites)
        newSprite = None
        card = Card(random.choice(list(Value)), random.choice(list(Suit)))
        newSprite = CardSprite(card, self.CARD_SIZE, self.TURRET_POSITION, self.PLAYER_4_CARD_2_POSITION, showCard=show, group=self.playerSprites)
        newSprite = None

    def testPlayerText(self) -> None:
        # Create the text for the player names
        newSprite = TextSprite("Player 1", self.font, self.fontColor, self.PLAYER_1_NAME_POSITION, self.playerSprites)
        newSprite = None
        newSprite = TextSprite("Player 2", self.font, self.fontColor, self.PLAYER_2_NAME_POSITION, self.playerSprites)
        newSprite = None
        newSprite = TextSprite("Player 3", self.font, self.fontColor, self.PLAYER_3_NAME_POSITION, self.playerSprites)
        newSprite = None
        newSprite = TextSprite("Player 4", self.font, self.fontColor, self.PLAYER_4_NAME_POSITION, self.playerSprites)
        newSprite = None

        # Create the text for the player chips
        newSprite = TextSprite("Chips: 1000", self.font, self.fontColor, self.PLAYER_1_STACK_POSITION, self.playerSprites)
        newSprite = None
        newSprite = TextSprite("Chips: 1000", self.font, self.fontColor, self.PLAYER_2_STACK_POSITION, self.playerSprites)
        newSprite = None
        newSprite = TextSprite("Chips: 1000", self.font, self.fontColor, self.PLAYER_3_STACK_POSITION, self.playerSprites)
        newSprite = None
        newSprite = TextSprite("Chips: 1000", self.font, self.fontColor, self.PLAYER_4_STACK_POSITION, self.playerSprites)
        newSprite = None

        # Create the text for the player bets
        newSprite = TextSprite("Bet: 0", self.font, self.fontColor, self.PLAYER_1_BET_POSITION, self.playerSprites)
        newSprite = None
        newSprite = TextSprite("Bet: 0", self.font, self.fontColor, self.PLAYER_2_BET_POSITION, self.playerSprites)
        newSprite = None
        newSprite = TextSprite("Bet: 0", self.font, self.fontColor, self.PLAYER_3_BET_POSITION, self.playerSprites)
        newSprite = None
        newSprite = TextSprite("Bet: 0", self.font, self.fontColor, self.PLAYER_4_BET_POSITION, self.playerSprites)
        newSprite = None

        # Create the text for if the player is small or big blind
        newSprite = TextSprite("Small Blind", self.font, self.fontColor, self.PLAYER_1_BLIND_POSITION, self.playerSprites)
        newSprite = None
        newSprite = TextSprite("Big Blind", self.font, self.fontColor, self.PLAYER_2_BLIND_POSITION, self.playerSprites)
        newSprite = None
        newSprite = TextSprite("Small Blind", self.font, self.fontColor, self.PLAYER_3_BLIND_POSITION, self.playerSprites)
        newSprite = None
        newSprite = TextSprite("Big Blind", self.font, self.fontColor, self.PLAYER_4_BLIND_POSITION, self.playerSprites)
        newSprite = None

    def testDrawOther(self) -> None:
        # Create the text for the pot
        newSprite = TextSprite("Pot: 0", self.font, self.fontColor, self.POT_POSITION, self.communitySprites)
        newSprite = None

        # Deal card to the burn pile
        newSprite = CardSprite(None, self.CARD_SIZE, self.TURRET_POSITION, self.BURN_POSITION, showCard=False, group=self.communitySprites)
        newSprite = None

        # Deal card to the deal position
        newSprite = CardSprite(None, self.CARD_SIZE, self.TURRET_POSITION, self.DEAL_POSITION, showCard=False, group=self.communitySprites)
        newSprite = None

    def testDrawMenu(self) -> None:
        itemCount = 0
        pos = [self.MENU_CENTER_POSITION[0], self.MENU_CENTER_POSITION[1] + itemCount * 2 * self.FONT_HEIGHT]
        # Create the text for the menu
        newSprite = TextSprite("Menu", self.font, self.fontColor, pos, self.menuSprites)
        newSprite = None

        itemCount += 1
        pos = [self.MENU_CENTER_POSITION[0], self.MENU_CENTER_POSITION[1] + itemCount * 2 * self.FONT_HEIGHT]
        newSprite = TextSprite("Press Settings to edit settings", self.font, self.fontColor, pos, self.menuSprites)
        newSprite = None

        itemCount += 1
        pos = [self.MENU_CENTER_POSITION[0], self.MENU_CENTER_POSITION[1] + itemCount * 2 * self.FONT_HEIGHT]
        newSprite = TextSprite("Small Blind: 1", self.font, self.fontColor, pos, self.menuSprites)
        newSprite = None

        itemCount += 1
        pos = [self.MENU_CENTER_POSITION[0], self.MENU_CENTER_POSITION[1] + itemCount * 2 * self.FONT_HEIGHT]
        newSprite = TextSprite("Big Blind: 2", self.font, self.fontColor, pos, self.menuSprites)
        newSprite = None

        itemCount += 1
        pos = [self.MENU_CENTER_POSITION[0], self.MENU_CENTER_POSITION[1] + itemCount * 2 * self.FONT_HEIGHT]
        newSprite = TextSprite("White Chip Value: 1", self.font, self.fontColor, pos, self.menuSprites)
        newSprite = None

    # Method to display the menu
    # Update the text menu items based on the model
    # or have the item to be updated passed as an arg but makes more sense to have the model passed
    
    # Method to create a player hub
    # Needs to be passed the player number
    # Displays name - given as arg or get from model or default
    # Displays chips - maybe have default value
    # Displays bet - set at 0

    # Method to remove a player hub
    # Needs to be passed the player number
    # Removes the player hub

    # Method to indicate the player is the small or big blind
    # Needs to be passed the player number
    # Needs to be passed the blind type
    # Displays the blind type for that player

    # Method to update the player chips
    # Needs to be passed the player number
    # Needs to be passed the new chip value
    # or alternatively get the values from the model when called
    # Displays the chips for that player

    # Method to update the player bet (updated value)
    # Needs to be passed the player number
    # Needs to be passed the new bet value
    # or alternatively get the values from the model when called
    # Displays the bet for that player

    # Method to update the pot
    # Needs to be passed the new pot value
    # or alternatively get the value from the model when called
    # Displays the pot

    # Method to deal a card to the burn pile
    # Needs to be passed the card to be dealt
    # or alternatively get the card from the model when called
    # Displays the card moving to the burn pile

    # Method to deal the flop
    # Needs to be passed the cards to be dealt
    # or alternatively get the cards from the model when called
    # Displays the 3 cards moving to the flop

    # Method to deal the turn
    # Needs to be passed the card to be dealt
    # or alternatively get the card from the model when called
    # Displays the card moving to the turn

    # Method to deal the river
    # Needs to be passed the card to be dealt
    # or alternatively get the card from the model when called
    # Displays the card moving to the river

    # Method to deal a card to a player
    # Needs to be passed the player number
    # Needs to be passed the card to be dealt
    # or alternatively get the card from the model when called
    # Displays the card moving to the player
    # Needs to move to the right position

    # Method to indicate the player is the winner
    # Needs to be passed the player number
    # Displays the winner text for that player

    # Method to indicate the player turn
    # Needs to be passed the player number
    # Displays the indicator for that player

    # Method to flip a card
    # Needs to be passed the card to be flipped
    # or alternatively get the card from the model when called
    # Displays the card flipped
    # Can be used for the community cards or the player cards

    # Method to reset the round
    # Removes all cards from the screen
    # Resets the pot
    # Resets the player bets


    def update(self) -> None:
        
        # Clear the sprites on screen
        self.backSprites.clear(self.screen, self.background)
        self.playerSprites.clear(self.screen, self.background)
        self.communitySprites.clear(self.screen, self.background)
        self.menuSprites.clear(self.screen, self.background)

        seconds = 60

        # Update the sprites giving the time
        self.backSprites.update(seconds)
        self.playerSprites.update(seconds)
        self.communitySprites.update(seconds)
        self.menuSprites.update(seconds)

        # Draw the sprites on screen
        dirtyRects1 = self.backSprites.draw(self.screen)
        dirtyRects2 = self.playerSprites.draw(self.screen)
        dirtyRects3 = self.communitySprites.draw(self.screen)
        dirtyRects4 = self.menuSprites.draw(self.screen)

        # Update the display
        dirtyRects = dirtyRects1 + dirtyRects2 + dirtyRects3 + dirtyRects4
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

        view.update()