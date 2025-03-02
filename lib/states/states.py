import pygame
import json
import time

from lib.states.buttons import *
from lib.states.experience import *
from lib.states.point import *
from lib.GUI.label import label
from lib.GUI.imageButton import imageButtonChangeBg
from lib.functions.bigNumber import BigNumber

class states:
    def __init__(self,screen):
        pygame.font.init()
        self.states = {"rolls" : 0 , "playtime":0 , "experience" :0 , "level":0 , "point" : 0 , "point_exp" : 0}# playtime : s
        self.last_time = time.time()
        self.screen = screen

        # state classes
        self.experience = experience(self.screen)
        self.point      = point(self.screen)

        arial = pygame.font.match_font("arial")
        self.statesFont = pygame.font.Font(arial,30)

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

    def draw(self):
        # 其他的交給他自己處理
        self.experience.draw()
        
        if self.screen.scene == 0 : self.openButton.draw(self.screen.screen)
        if self.screen.scene == 2 :
            self.screen.screen.blit(self.bgImage,self.bgrect)
            self.closeButton.draw(self.screen.screen)
            # 顯示的states
            rollImage = self.statesFont.render(f"total rolls : {self.states["rolls"]}",True,(255,255,255))
            playtime = self.states["playtime"]
            s = playtime%60
            m = (playtime-s) //60 %60
            h = (playtime-s-m*60) // 3600
            timeplayImage = self.statesFont.render(f"total playing time : {h:.0f}h {m:.0f}m {s:.2f}s",True,(255,255,255))

            rollrect = rollImage.get_rect()
            timeplayrect = timeplayImage.get_rect()
            rollrect.x = 0
            timeplayrect.x = 0
            rollrect.y = SCREENSIZEY//10
            timeplayrect.y = rollrect.y + rollImage.get_height()

            self.screen.screen.blit(rollImage,rollrect)
            self.screen.screen.blit(timeplayImage,timeplayrect)

    def load(self):
        with open("./saves/states.json","r") as f : stateData = json.load(f)
        for state_name in self.states:
            if state_name in stateData   : self.states[state_name]    = stateData[state_name]
        # if "playtime" in stateData: self.states["playtime"] = stateData["playtime"]

        # experience
        self.experience.xp = BigNumber(self.states["experience"])
        self.experience.level = self.states["level"]

        # point
        self.point.point = BigNumber(self.states["point"])
        #self.point.point_exp = BigNumber(self.states["point_exp"])
        

    def save(self): 
        self.states["point"] = self.point.point.__repr__()
        self.states["experience"]    = self.experience.xp.__repr__()
        #self.states["point_exp"] = self.point.point_exp
 
        with open("./saves/states.json" , "w") as f: 
            json.dump(self.states,f)