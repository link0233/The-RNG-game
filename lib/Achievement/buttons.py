import pygame
from config import *
from lib.GUI.button import *
# from lib.GUI.imageButton import imageButtonChangeBg

# class openAchievementButton(imageButtonChangeBg):
#     def __init__(self,screen):
#         w = SCREENSIZEX//10
#         h = SCREENSIZEY//15
#         #self.mainScreen = screen
#         super().__init__("./images/button/Anchievement.png",0,600,100,100)

class closeAchievementButton(Button):
    def __init__(self,screen):
        self.mainScreen = screen
        w = SCREENSIZEY//10
        h = w
        super().__init__(0,0,w,h,"X",(255,0,0),(0,0,0),(200,0,0))