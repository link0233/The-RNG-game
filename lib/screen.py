import pygame
from config import *

from lib.GUI.quitButton import *

class screen():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE)

        #create objects
        self.quitButton = quitButton(self)
        
    def draw(self):
        self.screen.fill(SCREEN_BGCOLOR)
        self.quitButton.draw(self.screen)
        
        pygame.display.update()

    def update(self):

        self.quitButton.update()
        #quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
    

    def quit(self): 
        pygame.quit()
        import sys ; sys.exit()