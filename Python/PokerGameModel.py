import PokerRound
import Player

class PokerGameModel():
    rounds: list[PokerRound]
    players: list[Player]
    smallBlind: int
    bigBlind: int

    def __init__(self) -> None:
        self.rounds = []
        self.players = []
        self.smallBlind = 0
        self.bigBlind = 0
        
