import pygame
from config import *

from lib.setting.ChangeLuckBoost import *
from lib.GUI.imageButton import imageButtonChangeBg

class setting:
    def __init__(self,screen):
        self.screen = screen
        size = self.screen.size

        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.bgimage = pygame.Surface(size)
        self.bgimage.fill((200,200,200))
        self.bgrect = self.bgimage.get_rect()
        self.bgrect.x = 0
        self.bgrect.y = 0

        self.openButton = imageButtonChangeBg("./images/button/OpenSetting.png",0,size[1]//2+size[1]//10,size[1]//10-5,size[1]//10-5,50,border_radius=10)
        self.closeButton = imageButtonChangeBg("./images/button/close.png",0,0,size[1]//10,size[1]//10,50,border_radius=10,bg_color=(255, 0, 0),hover_bg_color=(104, 6, 6))
        self.ChangeLuckBoost = ChangeLuckBoost(self.screen)

    def update(self):
        self.ChangeLuckBoost.update()
        if self.screen.scene == SCENE_MAIN:
            if self.openButton.check_clicked(self.screen.event):
                self.screen.scene = SCENE_SETTING

        if self.screen.scene == SCENE_SETTING:
            if self.closeButton.check_clicked(self.screen.event) :
                self.screen.scene = SCENE_MAIN

    def draw(self):

        if self.screen.scene == SCENE_MAIN:
            self.openButton.draw(self.screen.screen)

        if self.screen.scene == SCENE_SETTING:
            # reset
            self.image = pygame.Surface(self.image.get_size())
            self.image.fill((0,0,0))
            self.image.set_colorkey((0,0,0))

            self.image.blit(self.bgimage,self.bgrect)
            self.screen.screen.blit(self.image,self.rect)
            self.closeButton.draw(self.screen.screen)

            self.ChangeLuckBoost.draw()