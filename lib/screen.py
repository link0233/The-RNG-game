import pygame
import json
from config import *
import time

#from lib.key import *
from lib.GUI.quitButton import *
from lib.Roll.roll import *
from lib.inventory.inventory import *
from lib.states.states import *
from lib.Achievement.Achievement import Achievement
from lib.setting.setting import setting
from lib.Upgrade.upgrade import upgrade
from lib.functions.RateLimitedFunction import RateLimitedFunction
from lib.functions.functions import returnTrue

class screen():
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.size = self.screen.get_size()
        self.clock = pygame.time.Clock()
        self.now_time = time.time()
        self.delta_time = 0
        self.last_time = time.time()

        loadingfont = pygame.font.Font("./font/Ubuntu/Ubuntu-Bold.ttf",100)
        loadingimage = loadingfont.render("Loading",True,(255,255,255))
        rect = loadingimage.get_rect()
        rect.centerx = self.size[0]//2
        rect.centery = self.size[1]//2
        self.screen.fill((0,0,0))
        self.screen.blit(loadingimage,rect)
        pygame.display.update()

        #場景
        self.scene = 0
        # 主畫面 : 0
        # 背包   : 1
        # states : 2

        #back ground
        self.bg_image = pygame.image.load("./images/background.jpg").convert_alpha()
        self.bg_rect  = self.bg_image.get_rect()
        self.bg_rect.x = 0
        self.bg_rect.y = 0

        #create objects
        self.quitButton :quitButton= quitButton(self)
        self.roll : rollUI = rollUI(self)
        self.inventory :inventory   = inventory(self)
        self.states : states = states(self)
        self.autoSave : RateLimitedFunction = RateLimitedFunction(10,returnTrue)
        self.Achievement = Achievement(self)
        self.setting : setting = setting(self)
        self.upgrade : upgrade = upgrade(self)

        #load
        self.load()

        loadingfont = None
        loadingimage = None
        rect = None

        self.states.all_set_update()
        
    def draw(self):
        self.screen.fill(SCREEN_BGCOLOR)
        self.screen.blit(self.bg_image,self.bg_rect)
        if self.scene == 0:self.quitButton.draw()
        self.roll.draw()
        self.inventory.draw()
        self.states.draw()
        self.Achievement.draw()
        self.setting.draw()
        self.upgrade.draw()
        
        pygame.display.update()

    def update(self):
        self.event = pygame.event.get()
        self.now_time = time.time()
        self.delta_time = self.now_time - self.last_time
        self.last_time = self.now_time

        if self.scene == 0 : self.quitButton.update()
        self.roll.update()
        self.inventory.update()
        self.states.update()
        self.Achievement.update()
        self.setting.update()
        self.upgrade.update()

        self.autoSave.execute(self.save)
        #quit
        for event in self.event:
            if event.type == pygame.QUIT:
                self.quit()
        
        self.clock.tick(60)
    

    def quit(self): 
        self.save()
        pygame.quit()
        import sys ; sys.exit()

    def load(self):
        #讀取物品
        self.states.load()
        self.upgrade.load()

        with open("./saves/item.json","r") as f:
            inventoryData = json.load(f)
        #包含更興處理 item -> normal item
        if "normalItem"  in inventoryData:    
            for name in inventoryData["normalItem"]:
                self.inventory.inventoryData["normalItem"][name] = BigNumber(inventoryData["normalItem"][name])
        elif "item"      in inventoryData:    
            for name in inventoryData["item"]:
                self.inventory.inventoryData["normalItem"][name] = BigNumber(inventoryData["item"][name])
        if "specialItem" in inventoryData:
            for name in inventoryData["specialItem"]:
                self.inventory.inventoryData["specialItem"][name] = BigNumber(inventoryData["specialItem"][name])
        if "extraItem"   in inventoryData:
            for name in inventoryData["extraItem"]:
                self.inventory.inventoryData["extraItem"][name] = BigNumber(inventoryData["extraItem"][name])
        if "cash"        in inventoryData:    self.inventory.inventoryData["cash"]        = inventoryData["cash"]
        # 活動限定處理
        if "specialItem" in inventoryData:
            if "2025HappyNewYear" in inventoryData["specialItem"]:
                self.inventory.inventoryData["extraItem"]["2025HappyNewYear"] = BigNumber(1)
        print(inventoryData)

    def save(self):
        #物品存檔
        self.states.save()
        self.upgrade.save()

        data = {"normalItem" : {} , "specialItem" : {} , "extraItem" : {}}
        data["cash"] = self.inventory.inventoryData["cash"]
        for d in self.inventory.inventoryData["normalItem"]:
            data["normalItem"][d] = self.inventory.inventoryData["normalItem"][d].__repr__()
        for d in self.inventory.inventoryData["specialItem"]:
            data["specialItem"][d] = self.inventory.inventoryData["specialItem"][d].__repr__()
        for d in self.inventory.inventoryData["extraItem"]:
            data["extraItem"][d] = self.inventory.inventoryData["extraItem"][d].__repr__()

        with open("./saves/item.json","w") as f:
            json.dump(data,f)