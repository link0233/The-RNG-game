import pygame
from config import *

from lib.GUI.quitButton import *
from lib.Roll.roll import *

class screen():
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(SCREENSIZE)
        self.clock = pygame.time.Clock()

        #create objects
        self.quitButton = quitButton(self)
        self.roll : rollUI = rollUI(self)
        
    def draw(self):
        self.screen.fill(SCREEN_BGCOLOR)
        self.quitButton.draw(self.screen)
        self.roll.draw()
        
        pygame.display.update()

    def update(self):
        self.event = pygame.event.get()

        self.quitButton.update()
        self.roll.update()
        #quit
        for event in self.event:
            if event.type == pygame.QUIT:
                self.quit()
        
        self.clock.tick(60)
    

    def quit(self): 
        pygame.quit()
        import sys ; sys.exit()