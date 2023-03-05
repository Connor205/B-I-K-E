import pygame
import random
from PokerGameModel import PokerGameModel
from Sprites import CardSprite, TableSprite
from Card import Card
from Enums import *
class PokerGameView:
    model: PokerGameModel
    screen: pygame.Surface
    background: pygame.Surface
    font: pygame.font.Font
    text: pygame.Surface
    textpos: pygame.Rect
    backSprites: pygame.sprite.RenderUpdates
    playerSprites: pygame.sprite.RenderUpdates
    communitySprites: pygame.sprite.RenderUpdates

    # Constants... but set at runtime based on screen size
    constTurretPosition: list[int]
    constPlayer1Position: list[int]
    constPlayer2Position: list[int]
    constPlayer3Position: list[int]
    constPlayer4Position: list[int]

    def __init__(self, model) -> None:
        # init pygame
        pygame.init()

        # init the given model
        self.model = model

        # setup the screen and load the background
        self.screen = pygame.display.set_mode((0,0))
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((250, 250, 250))

        # Set the turret position based on the screen size
        self.constTurretPosition = [self.screen.get_width() / 2, self.screen.get_height() / 9]

        # Set the player positions based on the screen size and the turret position
        self.constPlayer1Position = [self.constTurretPosition[0] - 500, self.constTurretPosition[1] + 150]
        self.constPlayer2Position = [self.constTurretPosition[0] - 200, self.constTurretPosition[1] + 500]
        self.constPlayer3Position = [self.constTurretPosition[0] + 200, self.constTurretPosition[1] + 500]
        self.constPlayer4Position = [self.constTurretPosition[0] + 500, self.constTurretPosition[1] + 150]

        # Create the render updates groups for the sprite categories
        self.backSprites = pygame.sprite.RenderUpdates()
        self.playerSprites = pygame.sprite.RenderUpdates()
        self.communitySprites = pygame.sprite.RenderUpdates()

        # Add the table sprite to the background
        newSprite = TableSprite(self.screen.get_size(), self.backSprites)

    def testMovingCards(self, show: bool) -> None:
        # Create a five random cards to test that will go to each player position
        card = Card(random.choice(list(Value)), random.choice(list(Suit)))
        newSprite = CardSprite(card, self.constTurretPosition, self.constPlayer1Position, showCard=show, group=self.communitySprites)
        newSprite = None
        card = Card(random.choice(list(Value)), random.choice(list(Suit)))
        newSprite = CardSprite(card, self.constTurretPosition, self.constPlayer2Position, showCard=show, group=self.communitySprites)
        newSprite = None
        card = Card(random.choice(list(Value)), random.choice(list(Suit)))
        newSprite = CardSprite(card, self.constTurretPosition, self.constPlayer3Position, showCard=show, group=self.communitySprites)
        newSprite = None
        card = Card(random.choice(list(Value)), random.choice(list(Suit)))
        newSprite = CardSprite(card, self.constTurretPosition, self.constPlayer4Position, showCard=show, group=self.communitySprites)
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
            # w key moves card backs to each player position
            if event.key == pygame.K_w:
                view.testMovingCards(False)
            # s key moves card fronts to each player position
            if event.key == pygame.K_s:
                view.testMovingCards(True)
    view.update()