import pygame
import json
import time

from lib.states.buttons import *
from lib.states.experience import *
from lib.states.point import *
from lib.GUI.label import label
from lib.GUI.imageButton import imageButtonChangeBg
from lib.functions.bigNumber import BigNumber
from lib.functions.RateLimitedFunction import RateLimitedFunction

class states:
    def __init__(self,screen):
        pygame.font.init()
        self.states = {"rolls" : 0 , "playtime":0 , "experience" :0 , "level":0 , "point" : 0 , "point_exp" : 0}# playtime : s
        self.last_time = time.time()
        self.screen = screen

        # state classes
        self.experience = experience(self.screen)
        self.point      = point(self.screen)

        # arial = pygame.font.match_font("arial")
        # self.statesFont = pygame.font.Font(arial,30)
        self.update_rate = RateLimitedFunction(1, returnTrue)

        #移動
        self.move_step = 75
        self.move_max = SCREENSIZEY//5 * 15 * -1
        self.move_value = 0

        #圖案
        self.bgImage = pygame.Surface(SCREENSIZE)
        self.bgImage.fill((100,100,100))
        self.bgrect = self.bgImage.get_rect()
        self.bgrect.x = 0
        self.bgrect.y = 0
        self.bgImage.set_alpha(150)
    
        size = self.screen.size
        self.openButton : imageButtonChangeBg = imageButtonChangeBg("./images/button/state.png",0,size[1]//2-size[1]//10,size[1]//10-5,size[1]//10-5,50,border_radius=10)
        self.closeButton: closeStatesButton = closeStatesButton(self.screen)

        # 標題
        self.title = label("States" , (0 , 0 , self.screen.size[0] , self.closeButton.h) , text_font= "./font/Lato/Lato-BoldItalic.ttf")

        # 數值
        self.label_h = self.screen.size[1]//20
        self.main_state_w = self.screen.size[0]
        self.playtime_label = label("3" , [ 10 , self.closeButton.h + self.label_h * 0 +10 , self.main_state_w , self.label_h] , text_position= "left" , text_font= "./font/Lato/Lato-Light.ttf")
        self.roll_label     = label("3" , [ 10 , self.closeButton.h + self.label_h * 1 +10 , self.main_state_w , self.label_h] , text_position= "left" , text_font= "./font/Lato/Lato-Light.ttf")

    def all_set_update(self):
        self.point.all_set_update()
        self.experience.all_set_update()

    def update(self):
        # 其他資料
        self.experience.update()
        self.point.update()

        #print(self.states)
        self.states["experience"] = self.experience.xp
        self.states["level"]      = self.experience.level
        self.states["point"]      = self.point.point
        #計算時間
        current_time = time.time()
        self.states["playtime"] += current_time - self.last_time
        self.last_time = current_time
        

        #處理按鈕
        if self.screen.scene == 0 : 
            if self.openButton.check_clicked(self.screen.event) : self.screen.scene = 2

        if self.screen.scene == 2:
            if self.closeButton.handle_event(self.screen.event) : self.screen.scene = 0

        # 最後顯示
        if self.screen.scene == SCENE_STATE:
            # 位移
            for event in self.screen.event:
                if event.type == pygame.MOUSEWHEEL:
                    self.move_value += event.y * self.move_step 
                    #調整溢出直
                    if self.move_value > SCREENSIZEY//10 :self.move_value = SCREENSIZEY//10
                    if self.move_value < self.move_max :  self.move_value = self.move_max

            
            self.update_rate.execute(self.update_mainstate)
            # 物件位移
            self.playtime_label.image_rect.y = self.closeButton.h + self.label_h * 0 + 10 + self.move_value
            self.roll_label.image_rect.y     = self.closeButton.h + self.label_h * 1 + 10 + self.move_value
            self.point.state_rect . y        = self.screen.size[1] + self.move_value
            self.experience.state_rect . y        = self.screen.size[1]*2 + self.move_value

    def draw(self):
        # 其他的交給他自己處理
        #self.experience.draw()
        
        if self.screen.scene == 0 : self.openButton.draw(self.screen.screen)
        if self.screen.scene == 2 :
            self.screen.screen.blit(self.bgImage,self.bgrect)
            self.closeButton.draw(self.screen.screen)
            self.title.draw(self.screen.screen)

            self.playtime_label.draw(self.screen.screen)
            self.roll_label.draw(self.screen.screen)

            self.point.draw()
        self.experience.draw()

        

    def load(self):
        with open("./saves/states.json","r") as f : stateData = json.load(f)
        for state_name in self.states:
            if state_name in stateData   : self.states[state_name]    = stateData[state_name]
        # if "playtime" in stateData: self.states["playtime"] = stateData["playtime"]

        # experience
        self.experience.xp = BigNumber(self.states["experience"])
        self.experience.level = BigNumber(self.states["level"])

        # point
        self.point.point = BigNumber(self.states["point"])
        
        # state_upgrade
        with open("./saves/state_upgrade.json", "r") as f:
            data = json.load(f)

        if "point" in data:
            for upgrade in data["point"]:
                print(self.point.state_upgrades)
                self.point.state_upgrades[upgrade]["level"] = BigNumber(data["point"][upgrade])

        if "experience" in data:
            for upgrade in data["experience"]:
                print(self.point.state_upgrades)
                self.experience.state_upgrades[upgrade]["level"] = BigNumber(data["experience"][upgrade])
        

    def save(self): 
        self.states["point"] = self.point.point.__repr__()
        self.states["experience"]    = self.experience.xp.__repr__()
        self.states["level"] = self.experience.level.__repr__()
        #self.states["point_exp"] = self.point.point_exp
 
        with open("./saves/states.json" , "w") as f: 
            json.dump(self.states,f)

        state_upgrade_data = {}
        state_upgrade_data["point"] = {}
        for upgrade in self.point.state_upgrades:
            state_upgrade_data["point"][upgrade] = self.point.state_upgrades[upgrade]["level"].__repr__()
        state_upgrade_data["experience"] = {}
        for upgrade in self.point.state_upgrades:
            state_upgrade_data["experience"][upgrade] = self.experience.state_upgrades[upgrade]["level"].__repr__()

        with open("./saves/state_upgrade.json" , "w") as f:
            json.dump(state_upgrade_data , f)

    def update_mainstate(self):
        playtime = self.states["playtime"]
        s = playtime%60
        m = (playtime-s) //60 %60
        h = (playtime-s-m*60) // 3600
        self.roll_label.change_text(f"{self.states["rolls"]} rolls")
        self.playtime_label.change_text(f"total playing time : {h:.0f}h {m:.0f}m {s:.2f}s")
        