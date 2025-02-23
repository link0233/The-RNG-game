import pygame
from config import *
import json

from lib.GUI.imageButton import imageButtonChangeBg
from lib.Upgrade.part import *

class upgrade:
    def __init__(self,screen):
        self.screen = screen
        pygame.font.init()

        # states
        self.map_pos = [0,0]
        self.map_move = [0,0] # 每個tick移動後的距離
        self.last_mouse_pos = [0,0]
        self.clicking = False

        size = self.screen.size
        # button
        self.open_button = imageButtonChangeBg("./images/button/Upgrade.png" , 0,size[1]//2+ 2* size[1]//10 , size[1]//10-5 , size[1]//10-5,50,border_radius=10)
        self.closeButton = imageButtonChangeBg("./images/button/close.png",0,0,size[1]//10,size[1]//10,255,border_radius=10,bg_color=(255, 0, 0),hover_bg_color=(104, 6, 6))
        self.homeButton  = imageButtonChangeBg("./images/button/upgrade_home.png",0 , size[1] //10*9,size[1]//10,size[1]//10,50,bg_color=(200,200,200),hover_bg_color=(100,100,100) , border_radius=10)

        # boost
        self.luckboost = 1
        self.cashboost = 1

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
            "first upgrade" : part(screen,(0,0),"first upgrade" , "the first upgrade, It's boost your luck" , "$100",[],[["cash" , 100]],"luck"),#firstUpd(self.screen),
            "second upgrade": part(screen,(1,1),"second upgrade" , "the second upgrade, It's boost your cash" , "$100" , ["first upgrade"] , [["cash",100]] , "cash")
        }

    def update(self):
        if self.screen.scene == SCENE_MAIN :
            if self.open_button.check_clicked(self.screen.event) : self.screen.scene = SCENE_UPGRADE
        
        if self.screen.scene == SCENE_UPGRADE:
            # events
            for event in self.screen.event:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                if event.type == pygame.MOUSEMOTION:
                    # 移動整個地圖
                    if self.clicking :
                        self.map_move[0] = -self.last_mouse_pos[0] + event.pos[0]
                        self.map_move[1] = -self.last_mouse_pos[1] + event.pos[1]

                    self.last_mouse_pos = event.pos

            # move map
            #print(self.map_move)
            self.map_pos[0] += self.map_move[0]
            self.map_pos[1] += self.map_move[1]
            try:
                self.map_move[0] *= (0.9 ** (self.screen.delta_time+1))
                self.map_move[1] *= (0.9 ** (self.screen.delta_time+1))
            except:
                # 會換成complex，落換成則直接歸0
                self.map_move = [0,0]

            # button
            if self.closeButton.check_clicked(self.screen.event): self.screen.scene = SCENE_MAIN
            if self.homeButton.check_clicked(self.screen.event) : self.map_pos = [0,0]
            # parts
            for upd in self.main_upgrades :
                self.main_upgrades[upd].check_unlock()
            for _upgrade in self.main_upgrades:
                self.main_upgrades[_upgrade] .update(self.map_pos)
            
    def draw(self):
        if self.screen.scene == SCENE_MAIN :
            self.open_button.draw(self.screen.screen)

        if self.screen.scene == SCENE_UPGRADE:
            self.image = pygame.Surface(self.screen.size)
            self.image.fill((0,0,0))

            self.screen.screen.blit(self.image,self.rect)

            # parts
            for _upgrade in self.main_upgrades:
                self.main_upgrades[_upgrade] .draw_line()
            for _upgrade in self.main_upgrades:
                self.main_upgrades[_upgrade] .draw()

            self.screen.screen.blit(self.title_image , self.title_rect)

            for _upgrade in self.main_upgrades:
                self.main_upgrades[_upgrade] .draw_side()

            self.closeButton.draw(self.screen.screen)
            self.homeButton.draw(self.screen.screen)

    def load(self):
        with open("./saves/upgrade.json" , "r") as f:
            data = json.load(f)
            if "first upgrade" in data:
                if data["first upgrade"] > 0:
                    self.main_upgrades["first upgrade"].bought = True

        self.update_boost()

    def save(self):
        data = {}
        for upg in self.main_upgrades:
            if self.main_upgrades [upg] .bought:
                data[upg] = 1

        with open("./saves/upgrade.json" , "w") as f:
            json.dump(data,f)

    def update_boost(self):
        # reset
        self.luckboost = 1
        self.cashboost = 1

        # set
        if self.main_upgrades["first upgrade"].bought:
            self.luckboost *= 1.05
        if self.main_upgrades["second upgrade"].bought:
            self.cashboost *= 1.5
