import pygame
from config import *
import math

from lib.Achievement.buttons import *
from lib.Achievement.part import part
from lib.functions.RateLimitedFunction import RateLimitedFunction
from lib.functions.functions import returnTrue
from lib.functions.functions import closest_smaller
from lib.functions.functions import LongNumberToText
from lib.functions.bigNumber import BigNumber
from lib.GUI.imageButton import imageButtonChangeBg

class Achievement:
    def __init__(self,screen):              # 後兩項留給 part 讀取
        self.screen = screen
        self.totalLuckBoost = 1
        self.totalTimeReduce = 0

        self.scene = 0
        # 0 :基本的成就

        #移動
        self.move_step = 75
        self.move_max = SCREENSIZEY//5 * 5 * -1
        self.move_value = 0

        # 成就顯示方塊
        self.parts = {
            "roll"             : part("roll"        ,0,self.screen),
            "time"             : part("time"        ,1,self.screen),

            "cash"             : part("cash"        ,2,self.screen),

            "common"           : part("common"      ,3,self.screen),
            "uncommon"         : part("uncommon"    ,4,self.screen),
            "Rare"             : part("Rare"        ,5,self.screen),
            "VeryRare"         : part("VeryRare"    ,6,self.screen),
            "Epic"             : part("Epic"        ,7,self.screen),
            "lengendery"       : part("lengendery"  ,8,self.screen),
            "mythical"         : part("mythical"    ,9,self.screen),

            "Effortless"       : part("Effortless"  ,9,self.screen),
            "Easy"             : part("Easy"        ,10,self.screen),
            "Painless"         : part("Painless"    ,11,self.screen),
            "Uncomplicated"    : part("Uncomplicated"     ,12,self.screen),
            "Straightforward"  : part("Straightforward"   ,13,self.screen),
            "Manageable"       : part("Manageable"        ,14, self.screen),
            "Mild"             : part("Mild"              ,15,self.screen),
            "Undemanding"      : part("Undemanding"       ,16,self.screen),
            "Fairly easy"      : part("Fairly easy"       ,17,self.screen),
            "A bit difficult"  : part("A bit difficult"   ,18,self.screen),

            "hard pi"          : part("hard pi"           ,17,self.screen),
            "insane pi"        : part("insane pi"         ,17,self.screen),
            "terrifying pi"    : part("terrifying pi"     ,17,self.screen),
            "impossible pi"    : part("impossible pi"     ,17,self.screen),
        }
        # self.achievementData = {"roll":{"level": 0,"nextlevelreq" : "","boost" : "","nextlevelreq_value":0,"now_value":0,"now_state":"","last_level":0},
        #                         "time":{"level": 0,"nextlevelreq" : "","boost" : "","nextlevelreq_value":0,"now_value":0,"now_state":"","last_level":0},
        #                         "common":{"level": 0,"nextlevelreq" : "","boost" : "","nextlevelreq_value":0,"now_value":0,"now_state":"","last_level":0}}
        a = 0
        upitem = "common"
        for _item in self.parts:
            # if self.parts[upitem].item_type == "normalItem" and self.parts[_item].item_type == "specialItem":
            #     a = 0
            # if self.parts[upitem].item_type == "specialItem" and self.parts[_item].item_type == "extraItem":
            #     a = 0
            self.parts[_item].pos = a
            self.parts[_item].create_image()
            a +=1
            upitem  = _item
        
        self.achievementData = {}
        for name in self.parts:
            self.achievementData[name] = {"level": 0,"nextlevelreq" : "","boost" : "","nextlevelreq_value":0,"now_value":0,"now_state":"","last_level":0}
        
        size = self.screen.size
        self.openButton:imageButtonChangeBg = imageButtonChangeBg("./images/button/Anchievement.png",0,size[1]//2,size[1]//10-5,size[1]//10-5,50,border_radius=10)
        self.closeButton:closeAchievementButton = closeAchievementButton(screen)
        self.stateupdatetimelimit : RateLimitedFunction = RateLimitedFunction(10 , returnTrue)

        #images
        self.bg_image = pygame.Surface(SCREENSIZE)
        self.bg_image.fill((157, 255, 72))
        self.bg_image.set_alpha(100)

        #rects
        self.bg_rect = self.bg_image.get_rect()
        self.bg_rect.x = 0
        self.bg_rect.y = 0

        # 遊玩時間成就的每等級的時間
        self.time_allLevel = [0]
        for n in range(1,16):
            self.time_allLevel.append( 1800*n + 60*(n**(1/0.37)))

        ACHIEVEMENT_DATA = self.achievementData

    def update(self):
        ACHIEVEMENT_DATA = self.achievementData
        # buttons
        if self.openButton.check_clicked(self.screen.event) and self.screen.scene == SCENE_MAIN: self.screen.scene = SCENE_ACHIEVEMENT
        
        self.stateupdatetimelimit.execute(self.update_state)
        if self.screen.scene == SCENE_ACHIEVEMENT:
            if self.closeButton.handle_event(self.screen.event): self.screen.scene = SCENE_MAIN
            for event in self.screen.event:
                if event.type == pygame.MOUSEWHEEL:
                    self.move_value += event.y * self.move_step 
                    #調整溢出直
                    if self.move_value > SCREENSIZEY//10 :self.move_value = SCREENSIZEY//10
                    if self.move_value < self.move_max :  self.move_value = self.move_max

    def update_state(self):
        #roll
        totalroll = self.screen.states.states["rolls"]
        self.achievementData["roll"]["now_value"] = totalroll
        self.achievementData["roll"]["now_state"] = f"{totalroll} rolls"
        self.achievementData["roll"]["level"] = totalroll//100
        self.achievementData["roll"]["boost"] = f"X{self.achievementData["roll"]["level"]* 0.1 +1 :.1f} Luck"
        self.achievementData["roll"]["nextlevelreq_value"] = (self.achievementData["roll"]["level"] +1) * 100
        self.achievementData["roll"]["nextlevelreq"] = f"{(self.achievementData["roll"]["level"] +1) * 100} Rolls"
        self.achievementData["roll"]["last_level"] = (self.achievementData["roll"]["level"] ) *100

        #time
        totaltime = self.screen.states.states["playtime"]
        self.achievementData["time"]["now_value"] = totaltime
        self.achievementData["time"]["now_state"] =  f"{(((totaltime - totaltime%60)//60) - ((totaltime - totaltime%60)//60)%60) // 60:.0f}h {((totaltime - totaltime%60)//60%60):.0f}m {totaltime%60:.0f}s "
        self.achievementData["time"]["level"] = self.time_allLevel.index(closest_smaller(self.time_allLevel,totaltime)) 
        boost = self.achievementData["time"]["level"] * 0.1
        self.achievementData["time"]["boost"] = f"Reduced by {boost :.1f} seconds"
        if self.achievementData["time"]["level"] < 15 :
            t  =  self.achievementData["time"]["nextlevelreq_value"] = self.time_allLevel[self.achievementData["time"]["level"]+1]
            self.achievementData["time"]["nextlevelreq"] = f"{(((t - t%60)//60) - ((t - t%60)//60)%60) // 60:.0f}h {((t - t%60)//60%60):.0f}m {t%60:.0f}s "
        else:
            self.achievementData["time"]["nextlevelreq"] = "max"
            self.achievementData["time"]["nextlevelreq_value"] = -1
        self.achievementData["time"]["last_level"] = self.time_allLevel[min(self.achievementData["time"]["level"] ,0) ]
        
        #common
        inventoryData = self.screen.inventory.inventoryData
        text = ["common","uncommon","Rare","VeryRare","Epic","lengendery","mythical"]
        for item in text:
            if item in inventoryData["normalItem"]:
                c = inventoryData["normalItem"][item]
                print((c , inventoryData["normalItem"][item]))
            else:
                c = 0
            self.achievementData[item]["now_value"] = c
            self.achievementData[item]["now_state"] = f"{c}"
            
            if c != 0:
                if isinstance(c, (int, float)):
                    self.achievementData[item]["level"] = int(math.log2(c/8))
                    if self.achievementData[item]["level"] <0 : self.achievementData[item]["level"] = BigNumber(0)
                if isinstance(c, (BigNumber)):
                    self.achievementData[item]["level"] = int((c/8).log2())
                    if self.achievementData[item]["level"] <0 : self.achievementData[item]["level"] = BigNumber(0)
            else:
                self.achievementData[item]["level"] = BigNumber(0)
            self.achievementData[item]["boost"] = f"X{self.achievementData[item]["level"]* 0.1 +1 } {item}"
            self.achievementData[item]["nextlevelreq_value"] = (BigNumber(2)**((self.achievementData[item]["level"] +1)))*8
            self.achievementData[item]["nextlevelreq"] = f"{self.achievementData[item]["nextlevelreq_value"]} {item}"
            self.achievementData[item]["last_level"] = (BigNumber(2)**((self.achievementData[item]["level"] )))*8
            self.screen.inventory.item_list[item].Achievement_boost = self.achievementData[item]["level"]* 0.1 +1
            
        # cash-----------------------------------------------------------
        totalroll = self.screen.inventory.inventoryData["cash"]
        self.achievementData["cash"]["now_value"] = totalroll
        self.achievementData["cash"]["now_state"] = f"$ " + LongNumberToText(totalroll)
        if totalroll <= 0 : self.achievementData["cash"]["level"] = BigNumber(0)
        else: self.achievementData["cash"]["level"] = int(math.log10(totalroll/10))
        self.achievementData["cash"]["boost"] = f"X{self.achievementData["cash"]["level"]* 0.1 +1 } Cash"
        self.achievementData["cash"]["nextlevelreq_value"] = (BigNumber(10)**(self.achievementData["cash"]["level"] +1) )*10
        self.achievementData["cash"]["nextlevelreq"] = f"{ (BigNumber(10)**(self.achievementData["cash"]["level"] +1) )*10} Cash"
        self.achievementData["cash"]["last_level"] = (BigNumber(10)**(self.achievementData["cash"]["level"] ) )*10

        #南度系列----------------------------------------------------------------------------------
        #最低的
        try:Effortlesses = self.screen.inventory.inventoryData["normalItem"]["Effortless"]
        except : Effortlesses = BigNumber(0)
        self.achievementData["Effortless"]["now_value"] = Effortlesses
        self.achievementData["Effortless"]["now_state"] = f"" + Effortlesses.__repr__()
        if Effortlesses <= 0 : self.achievementData["Effortless"]["level"] = BigNumber(0)
        else: self.achievementData["Effortless"]["level"] = int(Effortlesses.log(1.35)) - 15
        if self.achievementData["Effortless"]["level"] <= 0 :self.achievementData["Effortless"]["level"]   = BigNumber(0)
        self.achievementData["Effortless"]["boost"] = f"x {self.achievementData["Effortless"]["level"]* 0.1 +1} Luck"
        self.achievementData["Effortless"]["nextlevelreq_value"] = BigNumber(1.35) ** (self.achievementData["Effortless"]["level"] +16)
        self.achievementData["Effortless"]["nextlevelreq"] = f"{ (BigNumber(1.35) ** (self.achievementData["Effortless"]["level"] +16)).__repr__(True)} Effortless"
        self.achievementData["Effortless"]["last_level"] =  BigNumber(1.35) ** (self.achievementData["Effortless"]["level"] + 15)

        #其他-----------------------------------------------------------------------------------------
        inventoryData = self.screen.inventory.inventoryData
        text = ["Effortless","Easy","Painless","Uncomplicated","Straightforward","Manageable","Mild","Undemanding","Fairly easy","A bit difficult"]
        for item in text:
            if item == "Effortless" : continue # 這東西是用來演算的，沒有他
            if item in inventoryData["normalItem"]:
                c = inventoryData["normalItem"][item]
            else:
                c = BigNumber(0)
            count = text.index(item)
            self.achievementData[item]["now_value"] = c
            self.achievementData[item]["now_state"] = f"{c.__repr__(True)}"
            if c != 0:
                self.achievementData[item]["level"] = c
                if self.achievementData[item]["level"] <0 : self.achievementData[item]["level"] = BigNumber(0)
            else:
                self.achievementData[item]["level"] = BigNumber(0)
            self.achievementData[item]["boost"] = f"X{(self.achievementData[item]["level"]* 0.2 +1) .__repr__(True)} {text[count -1]}"
            self.achievementData[item]["nextlevelreq_value"] = c +1
            self.achievementData[item]["nextlevelreq"] = f"{self.achievementData[item]["nextlevelreq_value"].__repr__(True)} {item}"
            self.achievementData[item]["last_level"] = c
            self.screen.inventory.item_list[text[count -1]].Achievement_boost = self.achievementData[item]["level"]* 0.2 +1

        # pi 系列----------------------------------------------------------------------------------------------------------
        inventoryData = self.screen.inventory.inventoryData
        text = ["pi" , "hard pi","insane pi","terrifying pi","impossible pi"]
        for item in text:
            if item == "pi" : continue # 這東西是用來演算的，沒有他
            if item in inventoryData["normalItem"]:
                c = inventoryData["normalItem"][item]
            else:
                c = BigNumber(0)
            count = text.index(item)
            self.achievementData[item]["now_value"] = c
            self.achievementData[item]["now_state"] = f"{c.__repr__()} {item}"
            if c != 0:
                self.achievementData[item]["level"] = c
                if self.achievementData[item]["level"] <0 : self.achievementData[item]["level"] = BigNumber(0)
            else:
                self.achievementData[item]["level"] = BigNumber(0)
            self.achievementData[item]["boost"] = f"X{self.achievementData[item]["level"]* 5 +1 } {text[count -1]}"
            self.achievementData[item]["nextlevelreq_value"] = c +1
            self.achievementData[item]["nextlevelreq"] = f"{self.achievementData[item]["nextlevelreq_value"]} {item}"
            self.achievementData[item]["last_level"] = c
            self.screen.inventory.item_list[text[count -1]].Achievement_boost = self.achievementData[item]["level"]*5 +1
        

        # reset
        self.totalLuckBoost = BigNumber(1)

        self.totalLuckBoost *= self.achievementData["roll"]["level"]* 0.1 +1
        self.totalLuckBoost *= self.achievementData["Effortless"]["level"] *0.1 +1
        self.totalTimeReduce = self.achievementData["time"]["level"]* 0.1# 抽取速度僅此一加成
        if self.totalTimeReduce > 1.5 : self.totalTimeReduce = 1.5 

    def draw(self):
        if self.screen.scene == SCENE_ACHIEVEMENT :
            self.screen.screen.blit(self.bg_image,self.bg_rect)
            for p in self.parts:
                self.parts[p] . draw(self.move_value)

            self.closeButton.draw(self.screen.screen)

        if self.screen.scene == SCENE_MAIN : self.openButton.draw(self.screen.screen)