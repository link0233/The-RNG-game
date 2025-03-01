import pygame
from config import *
import json
import math

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
        self.map_move_maxspeed = 50

        size = self.screen.size
        # button
        self.open_button = imageButtonChangeBg("./images/button/Upgrade.png" , 0,size[1]//2+ 2* size[1]//10 , size[1]//10-5 , size[1]//10-5,50,border_radius=10)
        self.closeButton = imageButtonChangeBg("./images/button/close.png",0,0,size[1]//10,size[1]//10,255,border_radius=10,bg_color=(255, 0, 0),hover_bg_color=(104, 6, 6))
        self.homeButton  = imageButtonChangeBg("./images/button/upgrade_home.png",0 , size[1] //10*9,size[1]//10,size[1]//10,50,bg_color=(200,200,200),hover_bg_color=(100,100,100) , border_radius=10)

        # boost
        self.luckboost = 1
        self.cashboost = 1
        self.xpboost = 1
        self.point_boost = 1
        self.point_index_boost = 1

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

            "cash upgrade #1" : part(screen,(2,1),"cash upgrade #1" , "It's boost your cash" , "$150",["second upgrade"],[["cash" , 150]],"cash"),
            "cash upgrade #2" : part(screen,(3,1),"cash upgrade #2" , "It's boost your cash" , "$300",["cash upgrade #1"],[["cash" , 300]],"cash"),
            "cash upgrade #3" : part(screen,(4,1),"cash upgrade #3" , "It's boost your cash" , "$400",["cash upgrade #2" ,"first xp upgrade"],[["cash" , 400]],"cash"),
            "second upgrade": part(screen,(1,1),"second upgrade" , "the second upgrade, It's boost your cash" , "$100" , ["first upgrade"] , [["cash",100]] , "cash"),

            "first xp upgrade": part(screen,(1,-1),"first xp upgrade" , "It's boost your experience" , "$150" , ["first upgrade"] , [["cash",150]] , "xp"),
            "xp upgrade #2" : part(screen,(2,-1),"xp upgrade #2" , "It's boost your xp" , "$200",["first xp upgrade"],[["cash" , 200]],"xp"),
            "xp upgrade #3" : part(screen,(3,-1),"xp upgrade #3" , "It's boost your xp" , "$400",["xp upgrade #2"],[["cash" , 400]],"xp"),
            "xp upgrade #4" : part(screen,(4,-1),"xp upgrade #4" , "It's boost your xp" , "$800",["xp upgrade #3"],[["cash" , 800]],"xp"),

            "unlock point" : part(screen,(4,-9),"unlock point" , "Unlock Point , point have a lot of upgrades , have fun ~" , "$2500",["xp upgrade #4"],[["cash" , 2500]],"point"),
            "point upgrade #1" : part(screen,(5,-10),"point upgrade #1" , "It's boost your point" , "10 * level+1 point",["unlock point"],[["point" , [10,0]]],"point" , 10),
            "point upgrade #2" : part(screen,(5,-9),"point upgrade #2" , "It's boost your point" , "500 point",["unlock point"],[["point" , [5,2]]],"point"),
            "point upgrade #3" : part(screen,(5,-8),"point upgrade #3" , "It's boost your point" , "800 point",["unlock point"],[["point" , [8,2]]],"point"),
            "point upgrade #4" : part(screen,(6,-10),"point upgrade #4" , "It's boost your point" , "3000 point",["point upgrade #1"],[["point" ,[3,3]]],"point"),
            "point upgrade #5" : part(screen,(6,-9),"point upgrade #5" , "It's boost your point" , "6000 point",["point upgrade #1"],[["point" , [6,3]]],"point"),
            "point upgrade #6" : part(screen,(6,-8),"point upgrade #6" , "It's boost your point" , "10000 point",["point upgrade #3"],[["point" , [1,4]]],"point"),
            "point upgrade #7" : part(screen,(6,-7),"point upgrade #7" , "It's boost your point" , "15000 point",["point upgrade #3"],[["point" ,[1.5,4]]],"point"),
            "point upgrade #8" : part(screen,(7,-10),"point upgrade #8" , "It's boost your point" , "26000 point",["point upgrade #5"],[["point" ,[2.6,4]]],"point"),
            "point upgrade #9" : part(screen,(7,-9),"point upgrade #9" , "It's boost your point" , "100000 point",["point upgrade #5"],[["point" , [1,5]]],"point")
        }

    def update(self):
        # point
        if not self.main_upgrades["unlock point"].bought:
            # 沒購買時point 歸0
            self.screen.states.point.point = 0
            self.screen.states.point.point_index = 0

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
            if self.map_move[0] > self.map_move_maxspeed :self.map_move[0] = self.map_move_maxspeed
            if self.map_move[1] > self.map_move_maxspeed :self.map_move[1] = self.map_move_maxspeed
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
            for upgrade in self.main_upgrades:
                if upgrade in data:
                    if data[upgrade] > 0:
                        self.main_upgrades[upgrade].bought = True
                        self.main_upgrades[upgrade].level = data[upgrade]

        for upgrade in self.main_upgrades:
            self.main_upgrades[upgrade].all_set_update()

        self.update_boost()

    def save(self):
        data = {}
        for upg in self.main_upgrades:
            if self.main_upgrades [upg] .bought:
                data[upg] = self.main_upgrades[upg].level

        with open("./saves/upgrade.json" , "w") as f:
            json.dump(data,f)

    def update_boost(self):
        # reset
        self.luckboost = 1
        self.cashboost = 1
        self.xpboost = 1
        self.point_boost = 1
        self.point_index_boost = 0

        # set
        # cash
        if self.main_upgrades["first upgrade"].bought:
            self.luckboost *= 1.05
        if self.main_upgrades["second upgrade"].bought:
            self.cashboost *= 1.5
        if self.main_upgrades["cash upgrade #1"].bought:
            self.cashboost += 1.5
        if self.main_upgrades["cash upgrade #2"].bought:
            self.cashboost += 1.5
        if self.main_upgrades["cash upgrade #3"].bought:
            self.cashboost += 1.5
        # if self.main_upgrades["second upgrade"].bought:
        #     self.cashboost *= 1.5
        # xp
        if self.main_upgrades["first xp upgrade"].bought:
            self.xpboost *= 1.5
        if self.main_upgrades["xp upgrade #2"].bought:
            self.xpboost *= 1.5
        if self.main_upgrades["xp upgrade #3"].bought:
            self.xpboost *= 1.5
        if self.main_upgrades["xp upgrade #4"].bought:
            self.xpboost *= 1.5

        # point
        if not self.main_upgrades["unlock point"].bought:
            # 沒購買時point 歸0
            self.screen.states.point.point = 0
            self.screen.states.point.point_index = 0

        if self.main_upgrades["point upgrade #1"].bought:
            self.point_boost *= 1.5 * self.main_upgrades["point upgrade #1"].level
        if self.main_upgrades["point upgrade #2"].bought:
            self.point_boost *= 2 * self.main_upgrades["point upgrade #2"].level
        if self.main_upgrades["point upgrade #3"].bought:
            self.point_boost *= 2 * self.main_upgrades["point upgrade #3"].level
        if self.main_upgrades["point upgrade #4"].bought:
            self.point_boost += 10 * self.main_upgrades["point upgrade #4"].level
        if self.main_upgrades["point upgrade #5"].bought:
            self.point_boost *= 1.5 * self.main_upgrades["point upgrade #5"].level
        if self.main_upgrades["point upgrade #6"].bought:
            self.point_boost *= 2 * self.main_upgrades["point upgrade #6"].level
        if self.main_upgrades["point upgrade #7"].bought:
            self.point_boost *= 5 * self.main_upgrades["point upgrade #7"].level
        if self.main_upgrades["point upgrade #8"].bought:
            self.point_boost += 30 * self.main_upgrades["point upgrade #8"].level
        if self.main_upgrades["point upgrade #9"].bought:
            self.point_boost += 50 * self.main_upgrades["point upgrade #9"].level

        try:
            a = int(math.log10(self.point_boost))
        except:
            a = 0
        self.point_index_boost += a
        self.point_boost /= 10 ** a
