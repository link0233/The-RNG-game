import pygame
import math
from config import *

from lib.GUI.label import label
from lib.functions.bigNumber import BigNumber
from lib.states.state_upgrade import state_upgrade

class experience:
    def __init__(self,screen):
        self.screen = screen

        # state
        self.xp = BigNumber(0) # xp 為此等到下等的所獲得的經驗值，而非全部的經驗值
        self.level = BigNumber(0)
        self.next_level_req = BigNumber(0)
        self.xp_boost = BigNumber(1) 
        self.test_xp_boost = BigNumber(1)
        self.schedule : float = 0 # 進度
        self.log10_1_25 = math.log10(1.25)
        self.point_boost = BigNumber(1)

        # images
        self.show_w = self.screen.size[0]//2
        self.show_h = self.screen.size[1]//20
        self.level_label = label("1234",(self.screen.size[0]//4 , self.screen.size[1] - self.show_h , self.show_w // 8,self.show_h) )

        self.progress_bar_h = self.show_h //2 - 10
        self.progress_bar_w = self.show_w //8*7 - 50

        self.progress_bar_bg_color = (72, 96, 107)
        self.progress_bar_color = (157, 206, 227)

        # position
        self.progress_bar_x = self.screen.size[0]//4 + self.show_w //8 + 25
        self.progress_bar_y = self.screen.size[1] - self.progress_bar_h - 15

        # state upgrades
        self.state_size = (self.screen.size[0], self.screen.size[1])
        self.state_unlock = False

        self.state_image = pygame.Surface(self.state_size , pygame.SRCALPHA)
        self.state_rect = self.state_image.get_rect()
        self.state_rect.x = 0
        self.state_rect.y = self.screen.size[1]

        self.state_top_h = self.state_size[1]//10 + self.state_size[1]//20

        # 個個升級
        self.state_upgrades = {
            "0" : {"image" :state_upgrade(self.screen , "123456789" , 0,  4,(255,255,255),(200,200,200,100) ) , "cost" :BigNumber(0) , "level" : BigNumber(0) , "boost" :BigNumber(1)},
            "1" : {"image" :state_upgrade(self.screen , "123456789" , 1,  4,(255,255,255),(200,200,200,100) ) , "cost" :BigNumber(0) , "level" : BigNumber(0) , "boost" :BigNumber(1)}
        }

        self.clear_image()

    def all_set_update(self):
        upgrade = "0"
        self.state_upgrades[upgrade]["level"] += 1
        self.state_upgrades[upgrade]["cost"] = BigNumber(5)+ BigNumber(5) * self.state_upgrades[upgrade]["level"]
        self.state_upgrades[upgrade]["boost"] = BigNumber(1.5) ** self.state_upgrades[upgrade]["level"]
        self.state_upgrades[upgrade]["image"].text_label.change_text(f"x{self.state_upgrades[upgrade]["boost"]} xp , cost:{self.state_upgrades[upgrade]["cost"]} level")

        upgrade = "1"
        self.state_upgrades[upgrade]["level"] += 1
        self.state_upgrades[upgrade]["cost"] = BigNumber(5) +BigNumber(3) * self.state_upgrades[upgrade]["level"]
        self.state_upgrades[upgrade]["boost"] = BigNumber(2) ** self.state_upgrades[upgrade]["level"]
        self.state_upgrades[upgrade]["image"].text_label.change_text(f"x{self.state_upgrades[upgrade]["boost"]} points , cost:{self.state_upgrades[upgrade]["cost"]} level")

    def update(self):
        if self.xp >= self.next_level_req:
            self.update_level()

        # state upgrade
        if self.state_unlock and self.screen.scene == SCENE_STATE:
            if not self.state_level_label:
                self.load_image()

            for upgrade in self.state_upgrades:
                self.state_upgrades[upgrade]["image"].update((0,self.state_rect.y))
                #if upgrade == "0":
                if self.state_upgrades[upgrade]["image"].click : self.buy(upgrade)


             # 結算最後並更改數值
            if self.state_rect.y < self.screen.size[1] : self.state_level_label.change_text(f"Level : {self.level.__repr__()} ")

        

        # schedule
        self.schedule = self.xp / self.next_level_req

    def draw(self):
        if self.screen.scene == SCENE_MAIN:
            self.level_label.draw(self.screen.screen)

            # progress bar
            pygame.draw.rect(self.screen.screen , self.progress_bar_bg_color ,(self.progress_bar_x,self.progress_bar_y,self.progress_bar_w,self.progress_bar_h) , border_radius= self.progress_bar_h //2)
            pygame.draw.rect(self.screen.screen , self.progress_bar_color    ,(self.progress_bar_x,self.progress_bar_y,self.progress_bar_w * float(self.schedule.__repr__()),self.progress_bar_h ) , border_radius= self.progress_bar_h //2)

        # state upgrade
        if self.screen.scene == SCENE_STATE:
            if self.state_rect.y < self.screen.size[1] and self.state_rect.bottomleft[1] >0 and self.state_unlock:
                if self.state_title == None :
                    self.load_image()
                self.state_image = pygame.Surface(self.state_size , pygame.SRCALPHA)

                self.state_title.draw(self.state_image)
                self.state_level_label.draw(self.state_image)

                for upgrade in self.state_upgrades:
                    self.state_upgrades[upgrade]["image"] .draw(self.state_image)

                self.screen.screen.blit(self.state_image , self.state_rect)

    def update_level(self):
        self.next_level_req = BigNumber(1.25) ** self.level
        while self.xp >= self.next_level_req:
            if self.xp >= self.next_level_req:
                self.xp -= self.next_level_req
                self.level += 1
                self.next_level_req = BigNumber(1.25) ** (self.level +1)

        self.level_label.change_text(str(self.level))
        if self.state_level_label: self.state_level_label.change_text(f"level : {self.level}")

    def add_xp(self , xp : int):
        """
        輸入xp 並且 xp 未加成，會自動計算加成並且進行升等等作業
        """
        self.xp_boost = 1
        self.xp_boost *= self.screen.updgrade.xpboost
        self.xp_boost *= self.state_upgrades["0"]["boost"]
        self.xp += xp * self.xp_boost * self.test_xp_boost

    def load_image(self):
        if self.state_unlock:
            self.state_size = (self.screen.size[0], self.screen.size[1])
            #self.state_unlock = False

            self.state_image = pygame.Surface(self.state_size , pygame.SRCALPHA)

            self.state_top_h = self.state_size[1]//10 + self.state_size[1]//20
            self.state_title       = label("Experience" , (0,0,self.state_size[0] , self.state_size[1]//10) ,text_color= (0,0,255), text_font= "./font/Ubuntu/Ubuntu-Bold.ttf")
            self.state_level_label = label("123456" , (0 , self.state_size[1]//10 , self.state_size[0] , self.state_size[1]//20) , text_font= "./font/Lato/Lato-Light.ttf")

            self.state_rect = self.state_image.get_rect()
            self.state_rect.x = 0
            self.state_rect.y = self.screen.size[1]

        #self.state_rect  = self.state_image.get_rect()

    def clear_image(self):

        #self.state_image = None#pygame.Surface(self.state_size , pygame.SRCALPHA)

        #self.state_top_h = self.state_size[1]//10 + self.state_size[1]//20
        self.state_title       = None
        self.state_level_label = None

    def buy(self,upgrade):
        if upgrade == "0":
            if self.level >= self.state_upgrades[upgrade]["cost"]:
                self.level -= self.state_upgrades[upgrade]["cost"]
                self.state_upgrades[upgrade]["level"] += 1
                self.state_upgrades[upgrade]["cost"] = BigNumber(5)+ BigNumber(5) * self.state_upgrades[upgrade]["level"]
                self.state_upgrades[upgrade]["boost"] = BigNumber(1.5) ** self.state_upgrades[upgrade]["level"]
                self.state_upgrades[upgrade]["image"].text_label.change_text(f"x{self.state_upgrades[upgrade]["boost"]} xp , cost:{self.state_upgrades[upgrade]["cost"]} level")
        if upgrade == "1":
            if self.level >= self.state_upgrades[upgrade]["cost"]:
                self.level -= self.state_upgrades[upgrade]["cost"]
                self.state_upgrades[upgrade]["level"] += 1
                self.state_upgrades[upgrade]["cost"] =  BigNumber(5)+BigNumber(3) * self.state_upgrades[upgrade]["level"]
                self.state_upgrades[upgrade]["boost"] = BigNumber(2) ** self.state_upgrades[upgrade]["level"]
                self.state_upgrades[upgrade]["image"].text_label.change_text(f"x{self.state_upgrades[upgrade]["boost"]} points , cost:{self.state_upgrades[upgrade]["cost"]} level")

        self.update_level()

    def get_point_boost(self):
        self.point_boost = BigNumber(1)
        self.point_boost *= self.state_upgrades["1"]["boost"]

        return self.point_boost
