import pygame
from lib.GUI.button import *
from config import *

class openinventoryButton(Button):
    def __init__(self,screen):
        w = SCREENSIZEX//10
        h = SCREENSIZEY//15
        self.mainScreen = screen
        super().__init__(0,SCREENSIZEY//2,w,h,"Inventory")

