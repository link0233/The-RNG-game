import pygame
from lib.GUI.button import *
from config import *

class quitButton(Button):
    def __init__(self,screen):
        w = SCREENSIZEX //16
        h = SCREENSIZEY //20
        super().__init__(SCREENSIZEX - w,0,w,h,"QUIT",hover_color= (124, 124, 124))
        self.screen = screen

    def update(self):
        onHandle = self.handle_event()
        if onHandle :
            self.screen.quit()