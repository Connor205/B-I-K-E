import pygame

class PokerGameView:
    def __init__(self, model) -> None:
        self.model = model
        self.screen = pygame.display.set_mode((800, 600))
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((250, 250, 250))

        self.font = pygame.font.Font(None, 36)
        self.text = self.font.render("Hello There", 1, (10, 10, 10))
        self.textpos = self.text.get_rect(centerx=self.background.get_width()/2)
        self.background.blit(self.text, self.textpos)

        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

    def update(self) -> None:
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

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
