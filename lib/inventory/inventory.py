import pygame
from config import *

from lib.inventory.item import *
from lib.inventory.inventoryUI import *

class inventory:
    def __init__(self,screen):
        self.inventoryData = {"normalItem":{},"specialItem":{},"extraItem":{}}
        self.screen = screen

        self.UI :inventoryUI = inventoryUI(screen)

        self.item_list  = {
            "common"          : item("common"          ,2          ,0,"./images/items/common.png","normalItem",screen),
            "uncommon"        : item("uncommon"        ,4          ,1,"./images/items/uncommon.png","normalItem",screen),
            "Rare"            : item("Rare"            ,8          ,2,"./images/items/rare.png","normalItem",screen),
            "rock"            : item("rock"            ,12         ,3,"./images/items/rock.png","normalItem",screen),
            "VeryRare"        : item("VeryRare"        ,50         ,4,"./images/items/veryrare.png","normalItem",screen),
            "Epic"            : item("Epic"            ,100        ,5,"./images/items/epic.png","normalItem",screen),
            "Line"            : item("Line"            ,1500       ,6,"./images/items/line.png","normalItem",screen),

            "1K"              : item("1K"              ,1000       ,0,"./images/items/1K.png","specialItem",screen),
            "2025HappyNewYear": item("2025HappyNewYear",2025       ,1,"./images/items/2025happynewyear.png","specialItem",screen)
        }

    def update(self):
        self.UI.update()

    def draw(self):
        self.UI.draw()