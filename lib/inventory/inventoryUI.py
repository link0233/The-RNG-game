import pygame
from config import *

from lib.GUI.inventoryButton import *

class ItemUI:
    def __init__(self,screen):
        self.screen = screen
        self.bgColor = INVENTORY_BGC
        self.open = False

        #處理滑鼠滾輪
        self.normal_move_value = SCREENSIZEY//10
        self.special_move_value = SCREENSIZEY//10
        self.extra_move_value = SCREENSIZEY//10

        self.move_step = 75          #物品數輛，反向
        self.normal_move_max = SCREENSIZEY//5 * 3 * -1      
        self.special_move_max = SCREENSIZEY//5 * 1 * -1        
        self.extra_move_max = SCREENSIZEY//5 * 1 * -1

        #場景
        self.scene = 1
        #1 : normal
        #2 : special
        #3 : extra

        self.image = pygame.Surface(SCREENSIZE)#全螢幕
        self.image.fill(self.bgColor)
        self.image.set_alpha(200)
        self.rect = self.image.get_rect()
        self.rect.x = 0; self.rect.y = 0

        self.openButton       :openitemButton  = openitemButton(screen)
        self.closeButton      :closeitemButton = closeitemButton(screen)
        self.normalButton     :normalButton  = normalButton(screen)
        self.specialButton    :specialButton        = specialButton(screen)
        self.extraButton      :extraButton          = extraButton(screen)

    def draw(self):
        #if self.open:
        if self.screen.scene == 1:
            self.screen.screen.blit(self.image,self.rect)
            if self.scene == 1:
                Normal_itemData = self.screen.inventory.inventoryData["normalItem"]
                itemlist = self.screen.inventory.item_list
                for item in itemlist:
                    if item in Normal_itemData:
                        itemlist[item].draw_itemList(Normal_itemData[item],True,self.normal_move_value)
                    else:
                        itemlist[item].draw_itemList(0,False,self.normal_move_value)
            
            if self.scene == 2:
                special_itemData = self.screen.inventory.inventoryData["specialItem"]
                itemlist = self.screen.inventory.item_list
                for item in itemlist:
                    if item in special_itemData:
                        itemlist[item].draw_itemList(special_itemData[item],True,self.special_move_value)
                    else:
                        itemlist[item].draw_itemList(0,False,self.special_move_value)

        if self.screen.scene == 0 :self.openButton.draw(self.screen.screen)
        if self.screen.scene == 1 : 
            self.closeButton.draw(self.screen.screen)
            self.normalButton.draw(self.screen.screen)
            self.specialButton.draw(self.screen.screen)
            self.extraButton.draw(self.screen.screen)

    def update(self):
        #處理開啟和關閉
        if self.openButton.handle_event(self.screen.event) and self.screen.scene == 0: 
            self.screen.scene = 1

        if self.closeButton.handle_event(self.screen.event) and self.screen.scene == 1:
            self.screen.scene = 0
        
        if self.normalButton.handle_event(self.screen.event) and self.screen.scene == 1:
            self.scene = 1
        if self.specialButton.handle_event(self.screen.event) and self.screen.scene == 1:
            self.scene = 2
        if self.extraButton.handle_event(self.screen.event) and self.screen.scene == 1:
            self.scene = 3
        
        for event in self.screen.event:
            #移動物品藍
            if event.type == pygame.MOUSEWHEEL:
                if self.screen.scene == 1:#只有開啟時使用

                    if self.scene == 1:
                        self.normal_move_value += event.y * self.move_step 
                        #調整溢出直
                        if self.normal_move_value > SCREENSIZEY//10 :         self.normal_move_value = SCREENSIZEY//10
                        if self.normal_move_value < self.normal_move_max : self.normal_move_value = self.normal_move_max
                    if self.scene == 2:
                        self.special_move_value += event.y * self.move_step 
                        if self.special_move_value > SCREENSIZEY//10 :         self.special_move_value = SCREENSIZEY//10
                        if self.special_move_value < self.normal_move_max : self.special_move_value = self.spcial_move_max
                    if self.scene == 3:
                        self.extra_move_value += event.y * self.move_step 
                        if self.extra_move_value > SCREENSIZEY//10 :         self.extra_move_value = SCREENSIZEY//10
                        if self.extra_move_value < self.normal_move_max : self.extra_move_value = self.extra_move_max
    
    def hide_allBeside(self):
        itemlist = self.screen.inventory.item_list
        for item in self.screen.inventory.item_list:
            itemlist[item] . beside_show_state = False