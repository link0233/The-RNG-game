import pygame
from config import *

from lib.inventory.item import *

class inventory:
    def __init__(self,screen):
        self.itemData = {"item":[]}

        self.item_list  = {
            "common"   : common(screen),
            "uncommon" : uncommon(screen),
            "rock"     : rock(screen)
        }
