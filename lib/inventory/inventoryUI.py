import pygame
from config import *

from lib.GUI.inventoryButton import *

class inventoryUI:
    def __init__(self,screen):
        self.screen = screen
        self.bgColor = INVENTORY_BGC
        self.open = False

        #處理滑鼠滾輪
        self.move_value = 0
        self.move_step = 50          #物品數輛，反向
        self.move_max = SCREENSIZEY//5 * 3 * -1

        self.image = pygame.Surface(SCREENSIZE)#全螢幕
        self.image.fill(self.bgColor)
        self.image.set_alpha(200)
        self.rect = self.image.get_rect()
        self.rect.x = 0; self.rect.y = 0

        self.openButton :openinventoryButton = openinventoryButton(screen)

    def draw(self):
        if self.open:
            self.screen.screen.blit(self.image,self.rect)
            itemData = self.screen.inventory.inventoryData["item"]
            itemlist = self.screen.inventory.item_list
            for item in itemlist:
                if item in itemData:
                    itemlist[item].draw_itemList(itemData[item],True,self.move_value)
                else:
                    itemlist[item].draw_itemList(0,False,self.move_value)

        self.openButton.draw(self.screen.screen)

    def update(self):
        ifclick = self.openButton.handle_event(self.screen.event)
        if ifclick: self.open = not self.open
        
        for event in self.screen.event:
            #移動物品藍
            if event.type == pygame.MOUSEWHEEL:
                if self.open :#只有開啟時使用
                    self.move_value += event.y * self.move_step 
                    #調整溢出直
                    if self.move_value > 0 :             self.move_value = 0
                    if self.move_value < self.move_max : self.move_value = self.move_max
    