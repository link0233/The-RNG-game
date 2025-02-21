import pygame
from config import *
import json

from lib.GUI.imageButton import imageButtonChangeBg
from lib.Upgrade.mainUpgrades import *

class upgrade:
    def __init__(self,screen):
        self.screen = screen
        pygame.font.init()

        size = self.screen.size
        self.open_button = imageButtonChangeBg("./images/button/Upgrade.png" , 0,size[1]//2+ 2* size[1]//10 , size[1]//10-5 , size[1]//10-5,50,border_radius=10)
        self.closeButton = imageButtonChangeBg("./images/button/close.png",0,0,size[1]//10,size[1]//10,50,border_radius=10,bg_color=(255, 0, 0),hover_bg_color=(104, 6, 6))

        # images
        self.image = pygame.Surface(size)
        self.image.fill((0,0,0))

        self.title_font = pygame.font.Font("./font/Noto/Noto-Regular.ttf" , size[1]//10 -10)
        self.title_image = self.title_font.render("Upgrade",True,(255,255,255))

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        self.title_rect = self.title_image.get_rect()
        ##                                    關閉按鈕的寬
        self.title_rect.center = ((size [0]  - size[1]//10) // 2 , size[1]//10 //2)

        # Upgrades
        self.main_upgrades = {
            "first upgrade" : firstUpd(self.screen),
            "second upgrade": secondUpd(self.screen)
        }

    def update(self):
        if self.screen.scene == SCENE_MAIN :
            if self.open_button.check_clicked(self.screen.event) : self.screen.scene = SCENE_UPGRADE
        
        if self.screen.scene == SCENE_UPGRADE:
            # button
            if self.closeButton.check_clicked(self.screen.event): self.screen.scene = SCENE_MAIN
            # parts
            for upd in self.main_upgrades :
                self.main_upgrades[upd].check_unlock()
            for _upgrade in self.main_upgrades:
                self.main_upgrades[_upgrade] .update((0,0))
            
    def draw(self):
        if self.screen.scene == SCENE_MAIN :
            self.open_button.draw(self.screen.screen)

        if self.screen.scene == SCENE_UPGRADE:
            self.image = pygame.Surface(self.screen.size)
            self.image.fill((0,0,0))

            self.image.blit(self.title_image , self.title_rect)

            self.screen.screen.blit(self.image,self.rect)
            # parts
            for _upgrade in self.main_upgrades:
                self.main_upgrades[_upgrade] .draw_line()
            for _upgrade in self.main_upgrades:
                self.main_upgrades[_upgrade] .draw()

            for _upgrade in self.main_upgrades:
                self.main_upgrades[_upgrade] .draw_side()

            self.closeButton.draw(self.screen.screen)

    def load(self):
        with open("./saves/upgrade.json" , "r") as f:
            data = json.load(f)
            if "first upgrade" in data:
                if data["first upgrade"] > 0:
                    self.main_upgrades["first upgrade"].bought = True

    def save(self):
        data = {}
        for upg in self.main_upgrades:
            if self.main_upgrades [upg] .bought:
                data[upg] = 1

        with open("./saves/upgrade.json" , "w") as f:
            json.dump(data,f)
