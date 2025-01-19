import pygame
from lib.GUI.button import *
from config import *

class openinventoryButton(Button):
    def __init__(self,screen):
        w = SCREENSIZEX//10
        h = SCREENSIZEY//15
        self.mainScreen = screen
        super().__init__(0,SCREENSIZEY//2,w,h,"Inventory")

class closeinventoryButton(Button):
    def __init__(self,screen):
        self.mainScreen = screen
        w = SCREENSIZEY//10
        h = w
        super().__init__(0,0,w,h,"X",(255,0,0),(0,0,0),(200,0,0))
