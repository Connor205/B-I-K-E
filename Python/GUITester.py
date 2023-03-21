import pygame as pg
from Turret import Turret

BUTTON_HEIGHT = 100
BUTTON_WIDTH = 300
BUTTON_SPACING = 25
BUTTON_TEXT_SIZE = 20
BUTTON_TEXT_COLOR = (0, 0, 0)


class GUITester:

    def __init__(self, debug=False):
        self.debug = debug
        # initialize a pygame window to 1920x1080
        pg.init()
        self.screen = pg.display.set_mode((1200, 800))
        self.clock = pg.time.Clock()
        self.running = True

        self.buttons = []
        self.turretButtons = []
        self.buttons.append({
            "x": 100,
            "y": 100,
            "width": 300,
            "height": 100,
            "text": "Test Button",
            "function": lambda: print("Hello World"),
            "is_pressed": False,
        })

        self.serial_port_str_turret = input(
            "Provide the Serial Port For the Turret:").strip()
        if self.serial_port_str_turret == "" and not debug:
            self.serial_port_str_turret = None
        else:
            self.turret = None

            self.connect()

    def draw(self):
        # First we want to fill the background
        self.screen.fill((105, 105, 105))

        # Lets draw the turret buttons
        for i, button in enumerate(self.turretButtons):
            x = 250
            y = i * (BUTTON_HEIGHT + BUTTON_SPACING) + BUTTON_SPACING
            pg.draw.rect(self.screen, button["color"],
                         (x, y, BUTTON_WIDTH, BUTTON_HEIGHT))
            pg.draw.rect(self.screen, (255, 255, 255),
                         (x, y, BUTTON_WIDTH, BUTTON_HEIGHT), 2)
            font = pg.font.Font('freesansbold.ttf', BUTTON_TEXT_SIZE)
            text = font.render(button["text"], True, BUTTON_TEXT_COLOR)
            textRect = text.get_rect()
            textRect.center = (x + (BUTTON_WIDTH / 2), y + (BUTTON_HEIGHT / 2))
            self.screen.blit(text, textRect)

        # We can draw the fps in the bottom right
        pg.display.set_caption(f"FPS: {self.clock.get_fps():.2f}")
        pg.display.flip()

    # Lets write a function to connect to the serial port of the arduinos
    def connectTurret(self):
        if self.turret:
            print("Turret already connected, attempting to reconnect... ")
        if not self.debug:
            self.turret = Turret(self.serial_port_str_turret)

        # We want to add more buttons if we are connected to the arduino
        self.turretButtons.append({
            "text":
            "90 degrees",
            "function":
            lambda: self.turret.turn_to_angle(90),
            "color": (152, 175, 199)
        })
        self.turretButtons.append({
            "text":
            "120 degrees",
            "function":
            lambda: self.turret.turn_to_angle(120),
            "color": (152, 175, 199)
        })

        # Buttons for turning the flywheel and indexer on and off
        self.turretButtons.append({
            "text":
            "Flywheel On",
            "function":
            lambda: self.turret.activateFlywheel(),
            "color": (132, 132, 130)
        })
        self.turretButtons.append({
            "text":
            "Flywheel Off",
            "function":
            lambda: self.turret.deactivateFlywheel(),
            "color": (132, 132, 130)
        })
        self.turretButtons.append({
            "text":
            "Indexer On",
            "function":
            lambda: self.turret.activateIndexer(),
            "color": (84, 98, 111)
        })
        self.turretButtons.append({
            "text":
            "Indexer Off",
            "function":
            lambda: self.turret.deactivateIndexer(),
            "color": (84, 98, 111)
        })

        for i, button in enumerate(self.turretButtons):
            button["x"] = 250
            button["y"] = i * (BUTTON_HEIGHT + BUTTON_SPACING) + BUTTON_SPACING
            button["width"] = BUTTON_WIDTH
            button["height"] = BUTTON_HEIGHT

    def connectShuffler(self):
        
    def events(self):
        # We dont have any user input so we just need to make sure we can exit the simulation
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN
                                         and event.key == pg.K_ESCAPE):
                self.running = False

    # This function will get called 60 times per second
    def update(self):
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        for button in self.turretButtons:
            if button["x"] < mouse[
                    0] < button["x"] + button["width"] and button["y"] < mouse[
                        1] < button["y"] + button["height"]:
                if click[0] == 1 and not button["is_pressed"]:
                    button["function"]()
                    button["is_pressed"] = True
                if click[0] == 0:
                    button["is_pressed"] = False

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()


if __name__ == "__main__":
    gui = GUITester(debug=True)
    gui.run()