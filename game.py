from window_config import *
from player import Player
import random

class Game:
    def __init__(self, id, vel = 1, width = 40, height = 60):
        self.ready = False
        self.id = id
        self.wins = [0,0]
        self.width = width
        self.height = height
        self.vel = vel
        self.curRound = 0
        self.rounds = 1
        self.complete = False
        self.tarX, self.tarY = self.genTar()
        self.players = [ Player(0, 0, vel, width, height, (255, 0, 255)),
                   Player(0, 0, vel, width, height, (255, 255, 0))]

    def connected(self):
        return self.ready

    def genTar(self):
        x = random.randint(self.width + self.vel,
                           screen_width - self.width - self.vel)
        y = random.randint(self.height + self.vel,
                           screen_height - self.height - self.vel)
        return x, y

    def getNewTar(self):
        self.tarX, self.tarY = self.genTar()

    def hasHitTar(self, p):
        t=[]
        t1=self.tarX-1
        t2=self.tarX+1
        t3=self.tarX-2
        t4=self.tarX+2
        t.append(t1)
        t.append(t2)
        t.append(t3)
        t.append(t4)
        t.append(self.tarX)
        r=[]
        r1=self.tarY-1
        r2=self.tarY+1
        r3=self.tarY-2
        r4=self.tarY+2
        r.append(r1)
        r.append(r2)
        r.append(r3)
        r.append(r4)
        r.append(self.tarY)
        return ((self.players[p]).x in t) and ((self.players[p]).y in r)

    def addWin(self, p):
        self.wins[p] += 1
        self.curRound += 1
        self.complete = self.isComplete()

    def isComplete(self):
        return self.curRound == self.rounds

    def close(self):
        pass