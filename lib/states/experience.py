import pygame
from config import *

from lib.GUI.label import label

class experience:
    def __init__(self,screen):
        self.screen = screen

        # state
        self.xp = 0 # xp 為此等到下等的所獲得的經驗值，而非全部的經驗值
        self.level = 0 
        self.next_level_req = 0
        self.xp_boost = 1 
        self.test_xp_boost = 1
        self.schedule : float = 0 # 進度

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
    def update(self):
        if self.xp >= self.next_level_req:
            self.update_level()

        # schedule
        self.schedule = self.xp / self.next_level_req

    def draw(self):
        if self.screen.scene == SCENE_MAIN:
            self.level_label.draw(self.screen.screen)

            # progress bar
            pygame.draw.rect(self.screen.screen , self.progress_bar_bg_color ,(self.progress_bar_x,self.progress_bar_y,self.progress_bar_w,self.progress_bar_h) , border_radius= self.progress_bar_h //2)
            pygame.draw.rect(self.screen.screen , self.progress_bar_color    ,(self.progress_bar_x,self.progress_bar_y,self.progress_bar_w * self.schedule,self.progress_bar_h ) , border_radius= self.progress_bar_h //2)

    def update_level(self):
        self.next_level_req = 1.25 ** self.level
        while self.xp >= self.next_level_req:
            if self.xp >= self.next_level_req:
                self.xp -= self.next_level_req
                self.level += 1
                self.next_level_req = 1.25 ** (self.level +1)

        self.level_label.change_text(str(self.level))

    def add_xp(self , xp : int):
        """
        輸入xp 並且 xp 未加成，會自動計算加成並且進行升等等作業
        """
        self.xp_boost = 1
        self.xp_boost *= self.screen.updgrade.xpboost
        self.xp += xp * self.xp_boost * self.test_xp_boost