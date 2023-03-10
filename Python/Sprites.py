import pygame
from Card import Card

class CardSprite(pygame.sprite.Sprite):
    srcImage: pygame.Surface
    image: pygame.Surface
    pos: list[float]
    destPos: list[int]
    srcPos: list[int]
    rect: pygame.Rect
    speed: float

    # Constants
    CARD_BACK_PATH = "img/card_back_black.png"

    def __init__(self, card: Card, cardSize: list[int], srcPos: list[int],  destPos: list[int], speed: float=0.6, showCard: bool=False, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        if (showCard):
            self.srcImage = pygame.image.load(self.getCardImagePath(card))
        else:
            self.srcImage = pygame.image.load(self.CARD_BACK_PATH)
        self.image = self.srcImage
        self.image = pygame.transform.scale(self.image, cardSize)
        self.pos = [0.0, 0.0]
        self.pos[0] = srcPos[0] * 1.0  # float
        self.pos[1] = srcPos[1] * 1.0  # float
        self.destPos = destPos
        self.srcPos = srcPos
        self.rect = self.image.get_rect()
        self.speed = speed

    # Update this card's position 
    def update(self, seconds: float) -> None:
        # updated position over the destination pos
        # calibrate the final pos not over the destPos
        if self.destPos[0] - self.srcPos[0] < 0 \
            and self.destPos[0] <= self.pos[0]:
            self.pos[0] += self.getDeltaX(seconds)
            if self.pos[0] <= self.destPos[0]:
                self.pos[0] = self.destPos[0]
        if self.destPos[0] - self.srcPos[0] >= 0 \
            and self.destPos[0] >= self.pos[0]:
            self.pos[0] += self.getDeltaX(seconds)
            if self.pos[0] >= self.destPos[0]:
                self.pos[0] = self.destPos[0]
        if self.destPos[1] - self.srcPos[1] < 0 \
            and self.destPos[1] <= self.pos[1]:
            self.pos[1] += self.getDeltaY(seconds)
            if self.pos[1] <= self.destPos[1]:
                self.pos[1] = self.destPos[1]
        if self.destPos[1] - self.srcPos[1] >= 0 \
            and self.destPos[1] >= self.pos[1]:
            self.pos[1] += self.getDeltaY(seconds)
            if self.pos[1] >= self.destPos[1]:
                self.pos[1] = self.destPos[1]

        self.rect.centerx = round(self.pos[0], 0)
        self.rect.centery = round(self.pos[1], 0)

    # Get the delta x using the speed and the time
    def getDeltaX(self, seconds: float) -> float:
        return (-1.0) *(self.srcPos[0] - self.destPos[0]) / seconds / self.speed

    # Get the delta y using the speed and the time
    def getDeltaY(self, seconds: float) -> float:
        return (-1.0) *(self.srcPos[1] - self.destPos[1]) / seconds / self.speed

    # Get the image name of the card
    def getCardImagePath(self, card: Card) -> str:
        suit = card.suit
        value = card.value

        suit_str = ''
        value_str = ''

        if value.value >= 2 and value.value <= 10:
            value_str = str(value.value)
        elif value.value == 11:
            value_str = 'jack'
        elif value.value == 12:
            value_str = 'queen'
        elif value.value == 13:
            value_str = 'king'
        elif value.value == 14:
            value_str = 'ace'

        if suit.value == 1:
            suit_str = 'hearts'
        elif suit.value == 2:
            suit_str = 'spades'
        elif suit.value == 3:
            suit_str = 'clubs'
        elif suit.value == 4:
            suit_str = 'diamonds'

        path = 'img/' + value_str + suit_str + '.png'
        return path


class TableSprite(pygame.sprite.Sprite):
    TABLE_PATH = "img/Table.png"
    srcImage: pygame.Surface
    image: pygame.Surface
    rect: pygame.Rect

    def __init__(self, screenSize, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.srcImage = pygame.image.load(self.TABLE_PATH)
        self.srcImage = pygame.transform.scale(self.srcImage, screenSize)
        self.image = self.srcImage
        self.rect = (0, 0)

    def update(self, seconds):
        pass

class TextSprite(pygame.sprite.Sprite):
    text: str
    font: pygame.font.Font
    color: tuple[int, int, int]
    image: pygame.Surface
    rect: pygame.Rect
    pos: list[int]

    def __init__(self, text: str, font: pygame.font.Font, color: tuple[int, int, int], pos: list[int], group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.text = text
        self.font = font
        self.color = color
        self.pos = pos
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def write(self, text: str):
        self.text = text
        self.image = self.font.render(self.text, True, self.color)

    def update(self, seconds):
        pass