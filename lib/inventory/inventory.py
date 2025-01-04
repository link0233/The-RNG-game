import pygame
from config import *

from lib.inventory.item import *
from lib.inventory.inventoryUI import *

class inventory:
    def __init__(self,screen):
        self.inventoryData = {"item":[]}
        self.screen = screen

        self.UI :inventoryUI = inventoryUI(screen)

        self.item_list  = {
            "common"   : item("common"         ,2          ,0,"./images/items/common.png","normal item",screen),
            "uncommon" : item("uncommon"       ,4          ,1,"./images/items/uncommon.png","normal item",screen),
            "rare"     : item("Rare"           ,8          ,2,"./images/items/rare.png","normal item",screen),
            "rock"     : item("rock"           ,12         ,3,"./images/items/rock.png","normal item",screen),
            "VeryRare" : item("VeryRare"       ,50         ,4,"./images/items/veryrare.png","normal item",screen),
            "Epic"     : item("Epic"           ,100        ,5,"./images/items/epic.png","normal item",screen),
            "Line"     : item("Line"           ,1500       ,6,"./images/items/line.png","normal item",screen)
        }

    def update(self):
        self.UI.update()

    def draw(self):
        self.UI.draw()