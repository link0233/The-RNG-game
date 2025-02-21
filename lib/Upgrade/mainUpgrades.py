import pygame
from config import *

from lib.Upgrade.part import *

class firstUpd(part):
    def __init__(self,screen):
        super().__init__(screen,(0,0),"first upgrade" , "the first upgrade" , "$100",[])

    def check_can_buy(self):
        if self.screen.inventory.inventoryData["cash"] >= 100: return True
        else: return False

    def buy(self):
        self.screen.inventory.inventoryData["cash"] -= 100

class secondUpd(part):
    def __init__(self,screen):
        super().__init__(screen,(1,1),"second upgrade" , "the second upgrade" , "$100" , ["first upgrade"])

    def check_can_buy(self):
        if self.screen.inventory.inventoryData["cash"] >= 100: return True
        else: return False

    def buy(self):
        self.screen.inventory.inventoryData["cash"] -= 100