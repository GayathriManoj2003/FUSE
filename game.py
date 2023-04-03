from window_config import *
import pygame
from player import Player

class Game:
    def __init__(self, id):
        self.ready = False
        self.id = id
        self.wins = [0,0]
        self.p1Went = False
        self.p2Went = False
    def connected(self):
        return self.ready
    def bothWent(self):
        return self.p1Went and self.p2Went