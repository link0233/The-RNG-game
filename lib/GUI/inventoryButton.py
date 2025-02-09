import pygame
from lib.GUI.button import *
from lib.GUI.imageButton import imageButtonChangeBg
from config import *

class openitemButton(imageButtonChangeBg):
    def __init__(self,screen):
        w = SCREENSIZEX//10
        h = SCREENSIZEY//15
        self.mainScreen = screen
        size = screen.size
        super().__init__("./images/button/inventory.png",0,size[1]//2 - 2*size[1]//10,size[1]//10-5,size[1]//10-5,50,border_radius=10)

class closeitemButton(Button):
    def __init__(self,screen):
        self.mainScreen = screen
        w = SCREENSIZEY//10
        h = w
        super().__init__(0,0,w,h,"X",(255,0,0),(0,0,0),(200,0,0))

class normalButton(Button):
    def __init__(self,screen):
        self.mainScreen = screen
        h = SCREENSIZEY//10
        w = (SCREENSIZEX-h)//3
        super().__init__(0+h,0,w,h,"normal item")

class specialButton(Button):
    def __init__(self,screen):
        self.mainScreen = screen
        h = SCREENSIZEY//10
        w = (SCREENSIZEX-h)//3
        super().__init__(0+h+w,0,w,h,"special item")

class extraButton(Button):
    def __init__(self,screen):
        self.mainScreen = screen
        h = SCREENSIZEY//10
        w = (SCREENSIZEX-h)//3
        super().__init__(0+h+2*w,0,w,h,"extra item")