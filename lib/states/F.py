import pygame
from config import *

from lib.functions.bigNumber import BigNumber
from lib.functions.RateLimitedFunction import RateLimitedFunction
from lib.functions.functions import returnTrue

class F:
    def __init__(self  , screen):
        self.F = BigNumber(0)
        self.F_boost = BigNumber(1)

        self.screen = screen

        self.add_rate = RateLimitedFunction(1 , self.can_add)

    def update(self):
        self.add_rate.execute(self.addF)

    def addF(self):
        self.F_boost = BigNumber(1)

        self.F += self.F_boost

    def can_add(self):
        return self.screen.upgrade.main_upgrades["unlock something #3"].bought 
