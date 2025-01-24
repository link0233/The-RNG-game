import pygame
from config import *

from lib.inventory.item import item
from lib.inventory.inventoryUI import *

class inventory:
    def __init__(self,screen):
        self.inventoryData = {"normalItem":{},"specialItem":{},"extraItem":{}}
        self.screen = screen

        self.ItemUI :ItemUI = ItemUI(screen)

        self.item_list  = {
            "common"          : item("common"          ,2          ,0,"./images/items/common.png","normalItem",screen),
            "uncommon"        : item("uncommon"        ,4          ,1,"./images/items/uncommon.png","normalItem",screen),
            "Rare"            : item("Rare"            ,8          ,2,"./images/items/rare.png","normalItem",screen),
            "rock"            : item("rock"            ,12         ,3,"./images/items/rock.png","normalItem",screen),
            "VeryRare"        : item("VeryRare"        ,50         ,4,"./images/items/veryrare.png","normalItem",screen),
            "air"             : item("air"             ,50         ,5,"./images/items/air.png","normalItem",screen),
            "coal"            : item("coal"            ,50         ,6,"./images/items/coal.png","normalItem",screen),
            "Epic"            : item("Epic"            ,100        ,7,"./images/items/epic.png","normalItem",screen),
            "dirt"            : item("dirt"            ,100        ,8,"./images/items/dirt.png","normalItem",screen),
            "water"           : item("water"           ,100        ,9,"./images/items/water.png","normalItem",screen),
            "grass"           : item("grass"           ,300        ,10,"./images/items/grass.png","normalItem",screen),
            "iron"            : item("iron"            ,800        ,11,"./images/items/iron.png","normalItem",screen),
            "Line"            : item("Line"            ,1500       ,12,"./images/items/line.png","normalItem",screen),
            "lengendery"      : item("lengendery"      ,100000     ,13,"./images/items/lengendery.png","normalItem",screen),

            "1K"              : item("1K"              ,1000       ,0,"./images/items/1K.png","specialItem",screen),
            "2025HappyNewYear": item("2025HappyNewYear",2025       ,1,"./images/items/2025happynewyear.png","specialItem",screen),
            "CURV"            : item("CURV"            ,3200       ,2,"./images/items/CURV.png","specialItem",screen),
            "watermelon"      : item("watermelon"      ,22500      ,3,"./images/items/watermelon.png","specialItem",screen),
            "error-1"         : item("error-1"         ,451578     ,4,"./images/items/error-1.png","specialItem",screen),
            "666666"          : item("666666"          ,666666     ,5,"./images/items/666666.png","specialItem",screen),

            "100roll"         : item("100roll"         ,0          ,0,"./images/items/100roll.png","extraItem",screen),
            "10Htimeplayed"   : item("10Htimeplayed"   ,0          ,1,"./images/items/10Htimeplayed.png","extraItem",screen),
            "10000roll"       : item("10000roll"       ,0          ,2,"./images/items/10000roll.png","extraItem",screen),
        }

    def update(self):
        self.ItemUI.update()

    def draw(self):
        self.ItemUI.draw()

    def checkExtraGet(self):
        """
        檢查是否有extra item獲得,如有,則回傳其一
        """
        for item in self.item_list:
            if self.item_list[item].checkExtraGet():
                return item
        return None