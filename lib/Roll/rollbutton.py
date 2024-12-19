import pygame
from config import *
from lib.GUI.button import *

class rollbutton(Button):
    def __init__(self,screen):
        w = SCREENSIZEX//10
        h = SCREENSIZEY//20
        super().__init__((SCREENSIZEX - w)//2 , SCREENSIZEY- 2*h,w,h,"Roll!")
        self.screen = screen