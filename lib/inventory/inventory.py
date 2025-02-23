import pygame
from config import *

from lib.inventory.item import item
from lib.inventory.itemUI import *
from lib.functions.functions import LongNumberToText

class inventory:
    def __init__(self,screen):
        self.inventoryData = {"cash":0,"normalItem":{},"specialItem":{},"extraItem":{}}
        self.screen = screen
        pygame.font.init()

        self.ItemUI :ItemUI = ItemUI(screen)

        self.item_list  = {
            # 稀有度類的
            "common"          : item("common"          ,2          ,0,"./images/items/common.png","normalItem",screen),
            "uncommon"        : item("uncommon"        ,4          ,1,"./images/items/uncommon.png","normalItem",screen),
            "Rare"            : item("Rare"            ,8          ,2,"./images/items/rare.png","normalItem",screen),
            "VeryRare"        : item("VeryRare"        ,50         ,3,"./images/items/veryrare.png","normalItem",screen),
            "Epic"            : item("Epic"            ,100        ,4,"./images/items/epic.png","normalItem",screen),
            "lengendery"      : item("lengendery"      ,100000     ,5,"./images/items/lengendery.png","normalItem",screen),
            "mythical"        : item("mythical"        ,1000000    ,6,"./images/items/mythical.png","normalItem",screen),
            # 物質類的
            "rock"            : item("rock"            ,12         ,7,"./images/items/rock.png","normalItem",screen),
            "air"             : item("air"             ,50         ,8,"./images/items/air.png","normalItem",screen),
            "coal"            : item("coal"            ,50         ,9,"./images/items/coal.png","normalItem",screen),
            "dirt"            : item("dirt"            ,100        ,10,"./images/items/dirt.png","normalItem",screen),
            "water"           : item("water"           ,150        ,11,"./images/items/water.png","normalItem",screen),
            "grass"           : item("grass"           ,300        ,12,"./images/items/grass.png","normalItem",screen),
            "iron"            : item("iron"            ,800        ,13,"./images/items/iron.png","normalItem",screen),
            "Line"            : item("Line"            ,1500       ,14,"./images/items/line.png","normalItem",screen),
            # 難度類的
            "Effortless"      : item("Effortless"      ,3     ,14,"./images/items/Effortless.png","normalItem",screen),
            "Easy"            : item("Easy"            ,10      ,14,"./images/items/Easy.png","normalItem",screen),
            "Painless"        : item("Painless"        ,50      ,14,"./images/items/Painless.png","normalItem",screen),
            "Uncomplicated"   : item("Uncomplicated"   ,100      ,14,"./images/items/Uncomplicated.png","normalItem",screen),
            "Straightforward" : item("Straightforward" ,500     ,14,"./images/items/Straightforward.png","normalItem",screen),
            "Manageable"      : item("Manageable"      ,1000      ,14,"./images/items/Manageable.png","normalItem",screen),
            "Mild"            : item("Mild"            ,6000      ,14,"./images/items/Mild.png","normalItem",screen),
            "Undemanding"     : item("Undemanding"     ,10000      ,14,"./images/items/Undemanding.png","normalItem",screen),
            "Fairly easy"     : item("Fairly easy"     ,30000      ,14,"./images/items/Fairly easy.png","normalItem",screen),
            "A bit difficult" : item("A bit difficult" ,50000      ,14,"./images/items/A bit difficult.png","normalItem",screen),
            # 尚未啟用特出功能
            "Challenging"     : item("Challenging"     ,100000      ,14,"./images/items/Challenging.png","normalItem",screen),
            "Tough"           : item("Tough"           ,450000      ,14,"./images/items/Tough.png","normalItem",screen),
            "Complicated"     : item("Complicated"     ,800000      ,14,"./images/items/Complicated.png","normalItem",screen),
            "Demanding"       : item("Demanding"       ,1000000      ,14,"./images/items/Demanding.png","normalItem",screen),
            "Quite difficult" : item("Quite difficult" ,3000000      ,14,"./images/items/Quite difficult.png","normalItem",screen),
            "Hard"            : item("Hard"            ,5000000      ,14,"./images/items/Hard.png","normalItem",screen),

            "1K"              : item("1K"              ,1000       ,0,"./images/items/1K.png","specialItem",screen),
            "CURV"            : item("CURV"            ,3200       ,2,"./images/items/CURV.png","specialItem",screen),
            "watermelon"      : item("watermelon"      ,22500      ,3,"./images/items/watermelon.png","specialItem",screen),
            "error-1"         : item("error-1"         ,451578     ,4,"./images/items/error-1.png","specialItem",screen),
            "666666"          : item("666666"          ,666666     ,5,"./images/items/666666.png","specialItem",screen),

            "100roll"         : item("100roll"         ,0          ,0,"./images/items/100roll.png","extraItem",screen),
            "10Htimeplayed"   : item("10Htimeplayed"   ,0          ,1,"./images/items/10Htimeplayed.png","extraItem",screen),
            "10000roll"       : item("10000roll"       ,0          ,2,"./images/items/10000roll.png","extraItem",screen),
            "2025HappyNewYear": item("2025HappyNewYear",0          ,1,"./images/items/2025happynewyear.png","extraItem",screen),
        }
        a = 0
        upitem = "common"
        for _item in self.item_list:
            if self.item_list[upitem].item_type == "normalItem" and self.item_list[_item].item_type == "specialItem":
                a = 0
            if self.item_list[upitem].item_type == "specialItem" and self.item_list[_item].item_type == "extraItem":
                a = 0
            self.item_list[_item].rarity_count = a
            self.item_list[_item].loadImage()
            a +=1
            upitem  = _item

        # cash
        self.cash_boost = 1
        self.cash_font = pygame.font.Font("./font/Ubuntu/Ubuntu-Bold.ttf",70)
        self.cash_font_height = self.cash_font.get_height() +10
        image = self.cash_font.render(f"${LongNumberToText(self.inventoryData["cash"])}",True,(53, 255, 107))
        self.cash_rect = image.get_rect()
        self.cash_rect.center = (SCREENSIZEX//2,self.cash_font_height//2)

    def update(self):
        self.ItemUI.update()
        self.cash_boost = 1
        self.cash_boost *=( self.screen.Achievement.achievementData["cash"]["level"] *0.1 +1)
        self.cash_boost *= self.screen.upgrade.cashboost

    def draw(self):
        self.ItemUI.draw()
        # draw cash
        if self.screen.scene == SCENE_MAIN:
            i = self.cash_font.render(f"${LongNumberToText(self.inventoryData["cash"])}",True,(53, 255, 107))
            self.cash_rect =  i.get_rect()
            self.cash_rect.center = (SCREENSIZEX//2,self.cash_font_height//2)
            self.screen.screen.blit(i,self.cash_rect)

    def checkExtraGet(self):
        """
        檢查是否有extra item獲得,如有,則回傳其一
        """
        for item in self.item_list:
            if self.item_list[item].checkExtraGet():
                return item
        return None
    
    def addCash(self,noboost_cash:int = 0,boosted_cash:int = 0):
        """
        增加錢錢
        noboost_cash : 需要加成的
        boosted_cash : 以加成的
        """
        self.inventoryData["cash"] += noboost_cash * self.cash_boost + boosted_cash