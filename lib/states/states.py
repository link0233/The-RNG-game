import pygame
import json
import time

from lib.states.buttons import *

class states:
    def __init__(self,screen):
        pygame.font.init()
        self.states = {"rolls" : 0 , "playtime":0}# playtime : s
        self.last_time = time.time()
        self.screen = screen

        arial = pygame.font.match_font("arial")
        self.statesFont = pygame.font.Font(arial,30)

        #圖案
        self.bgImage = pygame.Surface(SCREENSIZE)
        self.bgImage.fill((100,100,100))
        self.bgrect = self.bgImage.get_rect()
        self.bgrect.x = 0
        self.bgrect.y = 0
        self.bgImage.set_alpha(150)
    
        self.openButton : openStateButton = openStateButton()
        self.closeButton: closeStatesButton = closeStatesButton(self.screen)

    def update(self):
        #計算時間
        current_time = time.time()
        self.states["playtime"] += current_time - self.last_time
        self.last_time = current_time

        #處理按鈕
        if self.screen.scene == 0 : 
            if self.openButton.handle_event(self.screen.event) : self.screen.scene = 2

        if self.screen.scene == 2:
            if self.closeButton.handle_event(self.screen.event) : self.screen.scene = 0

    def draw(self):
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
        if "rolls" in stateData   : self.states["rolls"]    = stateData["rolls"]
        if "playtime" in stateData: self.states["playtime"] = stateData["playtime"]

    def save(self): 
        #print(self.states)
        with open("./saves/states.json" , "w") as f: 
            json.dump(self.states,f)