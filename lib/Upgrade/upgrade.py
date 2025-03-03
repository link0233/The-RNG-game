import pygame
from config import *
import json
import math

from lib.GUI.imageButton import imageButtonChangeBg
from lib.Upgrade.part import *
from lib.GUI.label import label
from lib.functions.RateLimitedFunction import RateLimitedFunction
from lib.functions.functions import returnTrue
from lib.functions.bigNumber import BigNumber

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
        self.states_update_speed = 0.5 #每秒更新兩次

        size = self.screen.size
        # button
        self.open_button = imageButtonChangeBg("./images/button/Upgrade.png" , 0,size[1]//2+ 2* size[1]//10 , size[1]//10-5 , size[1]//10-5,50,border_radius=10)
        self.closeButton = imageButtonChangeBg("./images/button/close.png",10,10,size[1]//10,size[1]//10,255,border_radius=10,bg_color=(190, 235, 255),hover_bg_color=(142, 179, 195))
        self.homeButton  = imageButtonChangeBg("./images/button/upgrade_home.png",size[1]//10 +20,10,size[1]//10,size[1]//10,255,bg_color=(190, 235, 255),hover_bg_color=(142, 179, 195) , border_radius=10)

        # boost
        self.luckboost = 1
        self.cashboost = 1
        self.xpboost = 1
        self.point_boost = BigNumber(0)
        #self.point_exp_boost = 1

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
            "first upgrade" : part(screen,(0,0),"first upgrade" , "the first upgrade, It's boost your luck" , "$100",[],[["cash" , 100]],"luck"),
            "luck upgrade #2" : part(screen,(8,-8),"luck upgrade #2" , "It's boost your luck" , "$1,000,000 and 1e9 points",["point upgrade #6","point upgrade #7","point upgrade #9"],[["cash" , 1_000_000],["point" , "1e9"]],"luck"),

            "cash upgrade #1" : part(screen,(2,1),"cash upgrade #1" , "It's boost your cash" , "$150",["second upgrade"],[["cash" , 150]],"cash"),
            "cash upgrade #2" : part(screen,(3,1),"cash upgrade #2" , "It's boost your cash" , "$300",["cash upgrade #1"],[["cash" , 300]],"cash"),
            "cash upgrade #3" : part(screen,(4,1),"cash upgrade #3" , "It's boost your cash" , "$400",["cash upgrade #2" ,"first xp upgrade"],[["cash" , 400]],"cash"),
            "second upgrade": part(screen,(1,1),"second upgrade" , "the second upgrade, It's boost your cash" , "$100" , ["first upgrade"] , [["cash",100]] , "cash"),

            "first xp upgrade": part(screen,(1,-1),"first xp upgrade" , "It's boost your experience" , "$150" , ["first upgrade"] , [["cash",150]] , "xp"),
            "xp upgrade #2" : part(screen,(2,-1),"xp upgrade #2" , "It's boost your xp" , "$200",["first xp upgrade"],[["cash" , 200]],"xp"),
            "xp upgrade #3" : part(screen,(3,-1),"xp upgrade #3" , "It's boost your xp" , "$400",["xp upgrade #2"],[["cash" , 400]],"xp"),
            "xp upgrade #4" : part(screen,(4,-1),"xp upgrade #4" , "It's boost your xp" , "$800",["xp upgrade #3"],[["cash" , 800]],"xp"),
            "xp upgrade #5" : part(screen,(5,-1),"xp upgrade #5" , "It's boost your xp" , "$1000",["xp upgrade #4"],[["cash" , 1000]],"xp"),
            "xp upgrade #6" : part(screen,(6,-1),"xp upgrade #6" , "It's boost your xp" , "$5000",["xp upgrade #5"],[["cash" , 5000]],"xp"),
            "xp upgrade #7" : part(screen,(6,-2),"xp upgrade #7" , "It's boost your xp" , "$10m and 9e7 points",["xp upgrade #5" , "point upgrade #7"],[["cash" , 10_000_000] , ["point" , "9e7"]],"xp" , 10),

            "unlock point" : part(screen,(4,-9),"unlock point" , "Unlock Point , point have a lot of upgrades , have fun ~" , "$2500",["xp upgrade #4"],[["cash" , 2500]],"point"),
            "point upgrade #1" : part(screen,(5,-10),"point upgrade #1" , "It's boost your point" , "10 * level+1 point",["unlock point"],[["point" , "10"]],"point" , 10),
            "point upgrade #2" : part(screen,(5,-9),"point upgrade #2" , "It's boost your point" , "500 point",["unlock point"],[["point" , "5e2"]],"point"),
            "point upgrade #3" : part(screen,(5,-8),"point upgrade #3" , "It's boost your point" , "800 point",["unlock point"],[["point" , "8e2"]],"point"),
            "point upgrade #4" : part(screen,(6,-10),"point upgrade #4" , "It's boost your point" , "3000 point",["point upgrade #1"],[["point" ,"3e3"]],"point"),
            "point upgrade #5" : part(screen,(6,-9),"point upgrade #5" , "It's boost your point" , "6000 point",["point upgrade #1"],[["point" , "6e3"]],"point"),
            "point upgrade #6" : part(screen,(6,-8),"point upgrade #6" , "It's boost your point" , "10000 point",["point upgrade #3"],[["point" , "1e4"]],"point"),
            "point upgrade #7" : part(screen,(6,-7),"point upgrade #7" , "It's boost your point" , "15000 point",["point upgrade #3"],[["point" ,"1.5e4"]],"point"),
            "point upgrade #8" : part(screen,(7,-10),"point upgrade #8" , "It's boost your point" , "26000 point",["point upgrade #5"],[["point" ,"2.6e4"]],"point"),
            "point upgrade #9" : part(screen,(7,-9),"point upgrade #9" , "It's boost your point" , "100000 point",["point upgrade #5"],[["point" , "1e5"]],"point"),
            "point upgrade #10" : part(screen,(8,-10),"point upgrade #10" , "It's boost your point" , "200000 point",["point upgrade #8"],[["point" , "2e5"]],"point"),
            "point upgrade #11" : part(screen,(9,-10),"point upgrade #11" , "It's boost your point" , "5e6 point",["point upgrade #10"],[["point" , "5e6"]],"point" , 20)
        }

        # left-bottom states show
        # states = self.screen.states.states
        self.states_update_rate = RateLimitedFunction(self.states_update_speed , returnTrue)
        self.lb_label_h    = self.screen.size[1]//20
        self.cash_label    = label("1234",(10 , self.screen.size[1] - (self.lb_label_h +10 ) * 1 , self.screen.size[0] , self.lb_label_h),(53, 255, 107) ,text_position= "left",text_font= "./font/Lato/Lato-Light.ttf")
        self.point_label   = label("1234",(10 , self.screen.size[1] - (self.lb_label_h +10 ) * 2 , self.screen.size[0] , self.lb_label_h),(255,255,255)  ,text_position= "left",text_font= "./font/Lato/Lato-Light.ttf")

    def update(self):
        # point
        if not self.main_upgrades["unlock point"].bought:
            # 沒購買時point 歸0
            self.screen.states.point.point = BigNumber(0)
            #self.screen.states.point.point_exp = 0

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

            # labels
            self.states_update_rate.execute(self.update_statesLabel)
            
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

            # labels
            self.cash_label.draw(self.screen.screen)
            self.point_label.draw(self.screen.screen)

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
        self.point_boost = BigNumber(1)
        #self.point_exp_boost = 0

        # set
        # cash
        if self.main_upgrades["first upgrade"].bought:
            self.luckboost *= 1.05
        if self.main_upgrades["luck upgrade #2"].bought:
            self.luckboost += 0.2

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
        if self.main_upgrades["xp upgrade #5"].bought:
            self.xpboost *= 2
        if self.main_upgrades["xp upgrade #6"].bought:
            self.xpboost *= 2
        if self.main_upgrades["xp upgrade #7"].bought:
            self.xpboost *= 20 * self.main_upgrades["xp upgrade #7"].level

        # point
        if not self.main_upgrades["unlock point"].bought:
            # 沒購買時point 歸0
            self.screen.states.point.point = BigNumber(0)
            #self.screen.states.point.point_exp = 0

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
        if self.main_upgrades["point upgrade #10"].bought:
            self.point_boost *= 3 * self.main_upgrades["point upgrade #10"].level
        if self.main_upgrades["point upgrade #11"].bought:
            self.point_boost *= 2 * self.main_upgrades["point upgrade #11"].level

        # try:
        #     a = int(math.log10(self.point_boost))
        # except:
        #     a = 0
        # self.point_exp_boost += a
        # self.point_boost /= 10 ** a

    def update_statesLabel(self):
        cash = self.screen.inventory.inventoryData["cash"]
        state = self.screen.states.states
        self.cash_label.change_text(f"${cash:.0f}")
        self.point_label.change_text(f"{self.screen.states.point.point} points (+{self.screen.states.point.point_boost} points /s)")
