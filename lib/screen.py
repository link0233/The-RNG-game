import pygame
import json
from config import *

#from lib.key import *
from lib.GUI.quitButton import *
from lib.Roll.roll import *
from lib.inventory.inventory import *
from lib.functions.RateLimitedFunction import RateLimitedFunction
from lib.functions.functions import returnTrue

class screen():
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(SCREENSIZE)
        self.clock = pygame.time.Clock()

        #場景
        self.scene = 0
        # 主畫面 : 0
        # 背包   : 1

        #back ground
        self.bg_image = pygame.image.load("./images/background.jpg").convert_alpha()
        self.bg_rect  = self.bg_image.get_rect()
        self.bg_rect.x = 0
        self.bg_rect.y = 0

        #create objects
        self.quitButton :quitButton= quitButton(self)
        self.roll : rollUI = rollUI(self)
        self.inventory :inventory   = inventory(self)
        self.autoSave : RateLimitedFunction = RateLimitedFunction(10,returnTrue)

        #load
        self.load()
        
    def draw(self):
        self.screen.fill(SCREEN_BGCOLOR)
        self.screen.blit(self.bg_image,self.bg_rect)
        if self.scene == 0:self.quitButton.draw()
        self.roll.draw()
        self.inventory.draw()
        
        pygame.display.update()

    def update(self):
        self.event = pygame.event.get()

        if self.scene == 0 : self.quitButton.update()
        self.roll.update()
        self.inventory.update()

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
        with open("./saves/item.json","r") as f:
            inventoryData = json.load(f)
        #包含更興處理 item -> normal item
        if "normalItem"  in inventoryData:    self.inventory.inventoryData["normalItem"] = inventoryData["normalItem"]
        elif "item"      in inventoryData:    self.inventory.inventoryData["normalItem"] = inventoryData["item"]#優先選normalItem
        if "specialItem" in inventoryData:    self.inventory.inventoryData["specialItem"] = inventoryData["specialItem"]
        if "extraItem"   in inventoryData:    self.inventory.inventoryData["extraItem"] = inventoryData["extraItem"]
        print(inventoryData)

    def save(self):
        #物品存檔
        with open("./saves/item.json","w") as f:
            json.dump(self.inventory.inventoryData,f)