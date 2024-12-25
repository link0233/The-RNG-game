from lib.GUI.button import *
from config import *
import pygame

class autoRollButton(Button):
    def __init__(self,screen):
        w = SCREENSIZEX//10-20
        h = SCREENSIZEY//20-10
        self.toggle = False# 設定是否有在自動抽
        super().__init__((SCREENSIZEX - w)//2 -w-30, SCREENSIZEY- 2*h,w,h,"autoRoll!",hover_color= (100,100,100))
        self.screen = screen

    def update(self):
        click = self.handle_event(self.screen.event)
        if click: self.toggle = not self.toggle
        #更改顏色
        if self.toggle : self.color = (0, 121, 158)#案藍綠
        else: self.color = (200, 200, 200)#灰
        