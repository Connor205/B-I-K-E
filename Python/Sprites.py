import pygame
from Card import Card
from typing import Tuple

class CardSprite(pygame.sprite.Sprite):
    """Class representing a playing card sprite in poker."""
    card: Card
    srcImage: pygame.Surface
    backImage: pygame.Surface
    image: pygame.Surface
    pos: list[float]
    destPos: list[int]
    srcPos: list[int]
    rect: pygame.Rect
    speed: float

    # Constants
    CARD_BACK_PATH = "img/card_back_black.png"

    def __init__(self, card: Card, cardSize: list[int], srcPos: list[int],  destPos: list[int], speed: float=0.6, showCard: bool=False, group: pygame.sprite.Group=None):
        """
        Constructor for CardSprite.

        Args:
            card (Card): Card to represent.
            cardSize (list[int]): Size of the card as (width, height).
            srcPos (list[int]): Source position of the card.
            destPos (list[int]): Destination position of the card.
            speed (float, optional): Speed of the card movement. Defaults to 0.6.
            showCard (bool, optional): Whether to show the card face or the back. Defaults to False.
            group (pygame.sprite.Group, optional): Group to add this sprite to. Defaults to None.
        """
        pygame.sprite.Sprite.__init__(self, group)
        self.srcImage = pygame.image.load(self.getCardImagePath(card))
        self.srcImage = pygame.transform.scale(self.srcImage, cardSize)
        self.backImage = pygame.image.load(self.CARD_BACK_PATH)
        self.backImage = pygame.transform.scale(self.backImage, cardSize)

        if (showCard):
            self.image = self.srcImage
        else:
            self.image = self.backImage
        self.card = card
        
        self.pos = [0.0, 0.0]
        self.pos[0] = srcPos[0] * 1.0  # float
        self.pos[1] = srcPos[1] * 1.0  # float
        self.destPos = destPos
        self.srcPos = srcPos
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self, seconds: float) -> None:
        """Updates the position of the card sprite."""
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

    def getDeltaX(self, seconds: float) -> float:
        """Get the delta x using the speed and the given time."""
        return (-1.0) *(self.srcPos[0] - self.destPos[0]) / seconds / self.speed

    def getDeltaY(self, seconds: float) -> float:
        """Get the delta y using the speed and the given time."""
        return (-1.0) *(self.srcPos[1] - self.destPos[1]) / seconds / self.speed

    def getCardImagePath(self, card: Card) -> str:
        """Get the image path of the card."""
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
    
    def flip(self) -> None:
        """Flip the card by changing the image of the sprite."""
        if self.image == self.srcImage:
            self.image = self.backImage
        else:
            self.image = self.srcImage

    def getCard(self) -> Card:
        """Get the card represented by this sprite."""
        return self.card
    
    def moveTo(self, destPos: list[int]) -> None:
        """Move the card to the given destination position."""
        self.srcPos = int(self.pos[0]), int(self.pos[1])
        self.destPos = destPos


class TableSprite(pygame.sprite.Sprite):
    """Sprite representing the table."""
    TABLE_PATH = "img/Table.png"
    srcImage: pygame.Surface
    image: pygame.Surface
    rect: pygame.Rect

    def __init__(self, screenSize: list[int], group: pygame.sprite.Group=None):
        """
        Initialize the table sprite.
        
        Args:
            screenSize (list[int]): Size of the screen as (width, height)
            group (pygame.sprite.Group, optional): Group to add this sprite to. Defaults to None.
        """
        pygame.sprite.Sprite.__init__(self, group)
        self.srcImage = pygame.image.load(self.TABLE_PATH)
        self.srcImage = pygame.transform.scale(self.srcImage, screenSize)
        self.image = self.srcImage
        self.rect = (0, 0)

    def update(self, seconds):
        """Updates the table sprite."""
        pass

class TextSprite(pygame.sprite.Sprite):
    """Sprite representing text."""
    MAX_FONT_MULT = 2
    SPEED = 0.3

    text: str
    fontPath: str
    originalFontSize: int
    fontSize: int
    prevFontSize: int
    destFontSize: int
    color: Tuple[int, int, int]
    image: pygame.Surface
    rect: pygame.Rect
    pos: list[int]
    repeatCount: int
    timesCalled: int
    state: str

    def __init__(self, text: str, fontPath: str, fontSize: int, color: Tuple[int, int, int], pos: list[int], group: pygame.sprite.Group=None):
        """
        Initialize the text sprite.
        
        Args:
            text (str): Text to display
            font (pygame.font.Font): Font to use
            color (Tuple[int, int, int]): Color of the text
            pos (list[int]): Position of the text
            group (pygame.sprite.Group, optional): Group to add this sprite to. Defaults to None.
        """
        pygame.sprite.Sprite.__init__(self, group)
        self.text = text
        self.fontPath = fontPath
        self.originalFontSize = fontSize
        self.fontSize = fontSize
        self.color = color
        self.pos = pos
        self.write(self.text)
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.prevFontSize = fontSize
        self.destFontSize = int(self.MAX_FONT_MULT * fontSize)
        self.repeatCount = 0
        self.timesCalled = 0

        self.state = 'idle'

    def growShrinkOnce(self) -> None:
        """Grow and shrink the text."""
        self.repeatCount = 0
        self.timesCalled = 0
        self.state = 'once'

    def growShrinkRepeat(self) -> None:
        """Grow and shrink the text repeatedly."""
        self.repeatCount = 0
        self.timesCalled = 0
        self.state = 'repeat'

    def growShrinkReset(self) -> None:
        """Reset the text to its original size."""
        self.repeatCount = 0
        self.timesCalled = 0
        self.state = 'reset'

    def write(self, text: str) -> None:
        """Write the given text."""
        self.text = text
        myFont = pygame.font.Font(self.fontPath, self.fontSize)
        self.image = myFont.render(self.text, True, self.color)

    def update(self, seconds):
        """Updates the text sprite."""
        self.write(self.text)

        # center the text
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        if self.state == 'once':
            self.growShrinkText(seconds, False)
        elif self.state == 'repeat':
            self.growShrinkText(seconds, True)
        elif self.state == 'reset':
            self.resetSize()
        elif self.state == 'idle':
            pass

    def growShrinkText(self, seconds, repeatable):
        """Grow or shrink the text."""

        # If it isn't repeatable and it already grew/shrank,
        # reset the state back to idle and return
        if not repeatable and self.repeatCount > 1:
            self.state = 'idle'
            return
        
        self.timesCalled += 1
        diff = self.destFontSize - self.prevFontSize
        # check if the font size has reached the destination font size
        # and if so, swap the destination font size with the previous font size
        if (diff >= 0 and self.fontSize >= self.destFontSize) \
                or (diff <= 0 and self.fontSize <= self.destFontSize):
            tmp = self.prevFontSize
            self.prevFontSize = self.destFontSize
            self.destFontSize = tmp
            diff = self.destFontSize - self.prevFontSize
            self.repeatCount += 1

        delta_size = diff / seconds / self.SPEED
        # if the delta font size is bigger than 5% of current font size
        # just use 5%
        if delta_size > 0.05 * self.fontSize :
            delta_size = 0.05 * self.fontSize
        if int(delta_size) == 0:
            delta_size = 1
            # Since we can only increment the font with integers,
            # artifically add a delay
            if self.timesCalled % 5 == 0:
                return
        self.fontSize += int(delta_size)
    
    def resetSize(self) -> None:
        """Reset the font size to the original font size."""
        self.fontSize = self.originalFontSize
        self.state = 'idle'


# Class for pop-up windows that will be rectangular and display text
class PopUpWindow(pygame.sprite.Sprite):
    """Sprite representing a pop-up window."""
    text: str
    font: pygame.font.Font
    color: Tuple[int, int, int]
    image: pygame.Surface
    rect: pygame.Rect
    pos: list[int]
    size: list[int]

    IMG_PATH = "img/popup.png"

    def __init__(self, text: str, font: pygame.font.Font, color: Tuple[int, int, int], pos: list[int], size: list[int], group: pygame.sprite.Group=None):
        """
        Initialize the pop-up window.
        
        Args:
            text (str): Text to display
            font (pygame.font.Font): Font to use
            color (Tuple[int, int, int]): Color of the text
            pos (list[int]): Position of the text
            size (int): Size (width, height) of the window
            group (pygame.sprite.Group, optional): Group to add this sprite to. Defaults to None.
        """
        pygame.sprite.Sprite.__init__(self, group)
        self.text = text
        self.font = font
        self.color = color
        self.pos = pos
        self.size = size
        self.image = pygame.image.load(self.IMG_PATH)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.write(self.text)

    def write(self, text):
        """
        Write the given text centered on this popup window.
        
        Args:
            text (str): Text to write
        """
        self.text = text
        # first, split the text into words
        words = text.split()

        # now, construct lines out of these words
        lines = []
        while len(words) > 0:
            # get as many words as will fit within allowed_width
            line_words = []
            while len(words) > 0:
                line_words.append(words.pop(0))
                fw, fh = self.font.size(' '.join(line_words + words[:1]))
                if fw > self.size[0]:
                    break

            # add a line consisting of those words
            line = ' '.join(line_words)
            lines.append(line)

        # now we've split our text into lines that fit into the width, actually
        # render them

        # we'll render each line below the last, so we need to keep track of
        # the culmative height of the lines we've rendered so far
        y_offset = 0.1 * self.size[1]
        for line in lines:
            # Render each line centered on this popup's self.image
            fw, fh = self.font.size(line)
            textRender = self.font.render(line, True, self.color)
            self.image.blit(textRender, (self.size[0] / 2 - fw / 2, y_offset))
            y_offset += fh


    def update(self, seconds):
        """Updates the pop-up window."""
        pass