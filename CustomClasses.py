from DiceRollerConsts import *
from random import randint

class Dice:
    n=1
    d=6
    fateState=False
    results=[]
    def __init__(self):
        pass

    def setN(self, num):
        self.n=int(num)

    def setD(self, sides):
        self.d=int(sides)

    def toggleFateState(self):
        self.fateState = not(self.fateState)
        if self.fateState:
            self.d=6

    def roll_dice(self):
        if self.fateState:
            self.results = [FATE_DICE[randint(0,5)] for _ in range(self.n)]
        else:
            self.results = [randint(1, self.d) for _ in range(self.n)]