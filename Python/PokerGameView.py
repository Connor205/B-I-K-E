import pygame
import random
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
    STATS_SIZE = [int(SCREEN_SIZE[0] * 1/2), SCREEN_SIZE[1]]

    # Sizes
    # Keeping it slightly to scale, table width is 60 inches, 
    # say card height is 5 inches and width is 2/3 of that
    CARD_SIZE = [int(TABLE_SIZE[0] * (5*2/3)/60), int(TABLE_SIZE[0] * 5/60)]
    FONT_HEIGHT = int(TABLE_SIZE[1] * 1/30)

    # Positions
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
    backSprites: pygame.sprite.RenderUpdates
    playerSprites: pygame.sprite.RenderUpdates
    communitySprites: pygame.sprite.RenderUpdates

    def __init__(self, model) -> None:
        # init pygame
        pygame.init()

        # init the given model
        self.model = model

        # setup the screen and load the background
        self.screen = pygame.display.set_mode((self.SCREEN_SIZE[0], self.SCREEN_SIZE[1]), pygame.NOFRAME)
        self.background = pygame.Surface(self.SCREEN_SIZE)
        self.background = self.background.convert()
        self.background.fill((250, 250, 250))

        # load the font
        self.font = pygame.font.Font(None, self.FONT_HEIGHT)

        # Create the render updates groups for the sprite categories
        self.backSprites = pygame.sprite.RenderUpdates()
        self.playerSprites = pygame.sprite.RenderUpdates()
        self.communitySprites = pygame.sprite.RenderUpdates()

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
        newSprite = TextSprite("Player 1", self.font, [0, 0, 0], self.PLAYER_1_NAME_POSITION, self.playerSprites)
        newSprite = None
        newSprite = TextSprite("Player 2", self.font, [0, 0, 0], self.PLAYER_2_NAME_POSITION, self.playerSprites)
        newSprite = None
        newSprite = TextSprite("Player 3", self.font, [0, 0, 0], self.PLAYER_3_NAME_POSITION, self.playerSprites)
        newSprite = None
        newSprite = TextSprite("Player 4", self.font, [0, 0, 0], self.PLAYER_4_NAME_POSITION, self.playerSprites)
        newSprite = None

        # Create the text for the player chips
        newSprite = TextSprite("Chips: 1000", self.font, [0, 0, 0], self.PLAYER_1_STACK_POSITION, self.playerSprites)
        newSprite = None
        newSprite = TextSprite("Chips: 1000", self.font, [0, 0, 0], self.PLAYER_2_STACK_POSITION, self.playerSprites)
        newSprite = None
        newSprite = TextSprite("Chips: 1000", self.font, [0, 0, 0], self.PLAYER_3_STACK_POSITION, self.playerSprites)
        newSprite = None
        newSprite = TextSprite("Chips: 1000", self.font, [0, 0, 0], self.PLAYER_4_STACK_POSITION, self.playerSprites)
        newSprite = None

        # Create the text for the player bets
        newSprite = TextSprite("Bet: 0", self.font, [0, 0, 0], self.PLAYER_1_BET_POSITION, self.playerSprites)
        newSprite = None
        newSprite = TextSprite("Bet: 0", self.font, [0, 0, 0], self.PLAYER_2_BET_POSITION, self.playerSprites)
        newSprite = None
        newSprite = TextSprite("Bet: 0", self.font, [0, 0, 0], self.PLAYER_3_BET_POSITION, self.playerSprites)
        newSprite = None
        newSprite = TextSprite("Bet: 0", self.font, [0, 0, 0], self.PLAYER_4_BET_POSITION, self.playerSprites)
        newSprite = None

        # Create the text for if the player is small or big blind
        newSprite = TextSprite("Small Blind", self.font, [0, 0, 0], self.PLAYER_1_BLIND_POSITION, self.playerSprites)
        newSprite = None
        newSprite = TextSprite("Big Blind", self.font, [0, 0, 0], self.PLAYER_2_BLIND_POSITION, self.playerSprites)
        newSprite = None
        newSprite = TextSprite("Small Blind", self.font, [0, 0, 0], self.PLAYER_3_BLIND_POSITION, self.playerSprites)
        newSprite = None
        newSprite = TextSprite("Big Blind", self.font, [0, 0, 0], self.PLAYER_4_BLIND_POSITION, self.playerSprites)
        newSprite = None

    def testDrawOther(self) -> None:
        # Create the text for the pot
        newSprite = TextSprite("Pot: 0", self.font, [0, 0, 0], self.POT_POSITION, self.communitySprites)
        newSprite = None

        # Deal card to the burn pile
        newSprite = CardSprite(None, self.CARD_SIZE, self.TURRET_POSITION, self.BURN_POSITION, showCard=False, group=self.communitySprites)
        newSprite = None

        # Deal card to the deal position
        newSprite = CardSprite(None, self.CARD_SIZE, self.TURRET_POSITION, self.DEAL_POSITION, showCard=False, group=self.communitySprites)
        newSprite = None

    def update(self) -> None:
        
        # Clear the sprites on screen
        self.backSprites.clear(self.screen, self.background)
        self.playerSprites.clear(self.screen, self.background)
        self.communitySprites.clear(self.screen, self.background)

        seconds = 60

        # Update the sprites giving the time
        self.backSprites.update(seconds)
        self.playerSprites.update(seconds)
        self.communitySprites.update(seconds)

        # Draw the sprites on screen
        dirtyRects1 = self.backSprites.draw(self.screen)
        dirtyRects2 = self.playerSprites.draw(self.screen)
        dirtyRects3 = self.communitySprites.draw(self.screen)

        # Update the display
        dirtyRects = dirtyRects1 + dirtyRects2 + dirtyRects3
        pygame.display.update(dirtyRects)

        
        

    def drawPlayer(self, player) -> None:
        # Draw the player on the screen
        raise NotImplementedError("drawPlayer is not implemented")

    def drawPlayers(self) -> None:
        # Draw all the players on the screen
        raise NotImplementedError("drawPlayers is not implemented")

    def drawTable(self) -> None:
        # Draw the table on the screen
        raise NotImplementedError("drawTable is not implemented")

    def drawCards(self) -> None:
        # Draw the cards on the screen
        raise NotImplementedError("drawCards is not implemented")

    def drawPot(self) -> None:
        # Draw the pot on the screen
        raise NotImplementedError("drawPot is not implemented")

    def drawBet(self) -> None:
        # Draw the bet on the screen
        raise NotImplementedError("drawBet is not implemented")

    def drawDealer(self) -> None:
        # Draw the dealer on the screen
        raise NotImplementedError("drawDealer is not implemented")

    def drawBlinds(self) -> None:
        # Draw the blinds on the screen
        raise NotImplementedError("drawBlinds is not implemented")

    def drawButton(self) -> None:
        # Draw the button on the screen
        raise NotImplementedError("drawButton is not implemented")

    def drawButtonStatus(self) -> None:
        # Draw the button status on the screen
        raise NotImplementedError("drawButtonStatus is not implemented")

    def drawButtonStatuses(self) -> None:
        # Draw all the button statuses on the screen
        raise NotImplementedError("drawButtonStatuses is not implemented")

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

    view.update()