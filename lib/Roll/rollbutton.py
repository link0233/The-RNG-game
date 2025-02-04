import pygame
from config import *
from lib.GUI.button import *

class rollbutton(Button):
    def __init__(self,screen):
        w = SCREENSIZEX//10
        h = SCREENSIZEY//20
        super().__init__((SCREENSIZEX - w)//2 , SCREENSIZEY- 2*h,w,h,"Roll!",hover_color= (100,100,100),font = "./font/Ubuntu/Ubuntu-Bold.ttf",border_radius= 10)
        self.screen = screen
        self.roll = False

    def update(self):
        self.roll = self.handle_event(self.screen.event)

    def ifRoll(self): return self.roll or self.screen.roll.autoRollButton.toggle