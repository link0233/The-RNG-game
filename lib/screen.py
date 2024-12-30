import pygame
import json
from config import *

#from lib.key import *
from lib.GUI.quitButton import *
from lib.Roll.roll import *
from lib.item.item import *

class screen():
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(SCREENSIZE)
        self.clock = pygame.time.Clock()

        #back ground
        self.bg_image = pygame.image.load("./images/background.jpg").convert_alpha()
        self.bg_rect  = self.bg_image.get_rect()
        self.bg_rect.x = 0
        self.bg_rect.y = 0

        #create objects
        self.quitButton :quitButton= quitButton(self)
        self.roll : rollUI = rollUI(self)
        self.item :item   = item(self)

        #load
        self.load()
        
    def draw(self):
        self.screen.fill(SCREEN_BGCOLOR)
        self.screen.blit(self.bg_image,self.bg_rect)
        self.quitButton.draw()
        self.roll.draw()
        
        pygame.display.update()

    def update(self):
        self.event = pygame.event.get()

        self.quitButton.update()
        self.roll.update()
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
        with open("./saves/item.rng","r") as f:
            itemData = json.load(f)
        self.item.itemData = itemData
        print(itemData)

    def save(self):
        #物品存檔
        with open("./saves/item.rng","w") as f:
            json.dump(self.item.itemData,f)