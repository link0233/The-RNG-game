from config import *
import math

from lib.states.state_upgrade import *
from lib.functions.RateLimitedFunction import RateLimitedFunction
from lib.functions.functions import returnTrue
from lib.functions.bigNumber import BigNumber
from lib.GUI.label import label

class point:
    def __init__(self,screen):
        self.point = BigNumber(0)
        self.point_boost = BigNumber(1)
        self.screen = screen

        self.point_gen_timer = RateLimitedFunction(1,returnTrue)

        # 統計值介面升級系統
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
        self.state_upgrades["0"]["cost"] = BigNumber("1e5") * BigNumber(4) ** self.state_upgrades["0"]["level"]
        self.state_upgrades["0"]["boost"] = BigNumber(2) ** self.state_upgrades["0"]["level"]
        self.state_upgrades["0"]["image"].text_label.change_text(f"x{self.state_upgrades["0"]["boost"]} points , cost:{self.state_upgrades["0"]["cost"]} points")

        self.state_upgrades["1"]["cost"] = BigNumber("1e8") * BigNumber(6) ** self.state_upgrades["1"]["level"]
        self.state_upgrades["1"]["boost"] = BigNumber(3) ** self.state_upgrades["1"]["level"]
        self.state_upgrades["1"]["image"].text_label.change_text(f"x{self.state_upgrades["1"]["boost"]} points , cost:{self.state_upgrades["1"]["cost"]} points")



    def update(self):
        self.point_gen_timer.execute(self.add_a_point)
        #print(self.state_unlock)

        if self.state_unlock:

            for upgrade in self.state_upgrades:
                self.state_upgrades[upgrade]["image"].update((0,self.state_rect.y))
                #if upgrade == "0":
                if self.state_upgrades[upgrade]["image"].click : self.buy(upgrade)


             # 結算最後並更改數值
            if self.state_rect.y < self.screen.size[1] : self.state_point_label.change_text(f"{self.point.__repr__()} (+{self.point_boost.__repr__()})")

    def draw(self):
        # 當在畫面中 且以解鎖
        if self.state_rect.y < self.screen.size[1] and self.state_rect.bottomleft[1] >0 and self.state_unlock:
            if self.state_title == None :
                self.load_image()
            self.state_image = pygame.Surface(self.state_size , pygame.SRCALPHA)

            self.state_title.draw(self.state_image)
            self.state_point_label.draw(self.state_image)

            for upgrade in self.state_upgrades:
                self.state_upgrades[upgrade]["image"] .draw(self.state_image)

            self.screen.screen.blit(self.state_image , self.state_rect)
        
            
    def add_a_point(self):
        self.point_boost = BigNumber(1)

        print(( self.state_upgrades["0"]["boost"], self.screen.upgrade.point_boost , self.screen.states.experience.get_point_boost()))

        self.point_boost *= self.state_upgrades["0"]["boost"]
        self.point_boost *= self.state_upgrades["1"]["boost"]
        self.point_boost *= self.screen.upgrade.point_boost
        self.point_boost *= self.screen.states.experience.get_point_boost()

        self.point_boost.normalize()
        #print(self.point)
        #print(self.point_boost)
        self.point = self.point + self.point_boost
        self.point.normalize()
        #print( (self.point * (10 ** self.point_exp) , self.point_exp))

    def buy(self,upgrade):
        if upgrade == "0":
            if self.point > self.state_upgrades[upgrade]["cost"]:
                self.point -= self.state_upgrades[upgrade]["cost"]
                self.state_upgrades[upgrade]["level"] += 1
                self.state_upgrades[upgrade]["cost"] = BigNumber("1e5") * BigNumber(4) ** self.state_upgrades[upgrade]["level"]
                self.state_upgrades[upgrade]["boost"] = BigNumber(2) ** self.state_upgrades[upgrade]["level"]
                self.state_upgrades[upgrade]["image"].text_label.change_text(f"x{self.state_upgrades[upgrade]["boost"]} points , cost:{self.state_upgrades[upgrade]["cost"]} points")
        if upgrade == "1":
            if self.point > self.state_upgrades[upgrade]["cost"]:
                self.point -= self.state_upgrades[upgrade]["cost"]
                self.state_upgrades[upgrade]["level"] += 1
                self.state_upgrades[upgrade]["cost"] = BigNumber("1e8") * BigNumber(6) ** self.state_upgrades[upgrade]["level"]
                self.state_upgrades[upgrade]["boost"] = BigNumber(3) ** self.state_upgrades[upgrade]["level"]
                self.state_upgrades[upgrade]["image"].text_label.change_text(f"x{self.state_upgrades[upgrade]["boost"]} points , cost:{self.state_upgrades[upgrade]["cost"]} points")
  

    def load_image(self):
        if self.state_unlock:
            self.state_size = (self.screen.size[0], self.screen.size[1])
            #self.state_unlock = False

            self.state_image = pygame.Surface(self.state_size , pygame.SRCALPHA)

            self.state_top_h = self.state_size[1]//10 + self.state_size[1]//20
            self.state_title       = label("Point" , (0,0,self.state_size[0] , self.state_size[1]//10) , text_font= "./font/Ubuntu/Ubuntu-Bold.ttf")
            self.state_point_label = label("123456" , (0 , self.state_size[1]//10 , self.state_size[0] , self.state_size[1]//20) , text_font= "./font/Lato/Lato-Light.ttf")

            self.state_rect = self.state_image.get_rect()
            self.state_rect.x = 0
            self.state_rect.y = self.screen.size[1]

        #self.state_rect  = self.state_image.get_rect()

    def clear_image(self):

        #self.state_image = None#pygame.Surface(self.state_size , pygame.SRCALPHA)

        #self.state_top_h = self.state_size[1]//10 + self.state_size[1]//20
        self.state_title       = None
        self.state_point_label = None