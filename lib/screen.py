import pygame
from config import *

from lib.key import *
from lib.GUI.quitButton import *
from lib.Roll.roll import *
from lib.item.item import *

class screen():
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(SCREENSIZE)
        self.clock = pygame.time.Clock()
        self.key = JsonEncryptor("./saves/open.rng")

        #create objects
        self.quitButton :quitButton= quitButton(self)
        self.roll : rollUI = rollUI(self)
        self.item :item   = item(self)

        #load
        self.load()
        
    def draw(self):
        self.screen.fill(SCREEN_BGCOLOR)
        self.quitButton.draw(self.screen)
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

        if AUTOROLL:
            self.roll.Roll()
        
        self.clock.tick(60)
    

    def quit(self): 
        self.save()
        pygame.quit()
        import sys ; sys.exit()

    def load(self):
        #讀取物品
        itemData = self.key.decrypt_file_to_dict("./saves/item.rng")
        self.item.itemData = itemData
        print(itemData)

    def save(self):
        #物品存檔
        self.key.new_key()
        self.key.encrypt_dict_to_file(self.item.itemData,"./saves/item.rng")