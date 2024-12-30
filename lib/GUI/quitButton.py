import pygame
from lib.GUI.imageButton import *
from config import *

class quitButton(ImageButton):
    def __init__(self,screen):
        w = SCREENSIZEX //16
        h = SCREENSIZEY //20
        center = (SCREENSIZEX - w//2,h//2)
        #center = (600,600)
        super().__init__(screen.screen,"./images/button/quitButton.png","./images/button/hover_quitButton.png",center,150)
        self._screen = screen

    def update(self):
        self.update_hover_state(self._screen.event)
        self.check_clicked(self._screen.event)
        print(self.is_hovered)
        if self.is_clicked : import sys ; sys.exit() #退出
