import pygame
from config import *
import math

from lib.GUI.button import Button

class ChangeLuckBoost:
    def __init__(self,screen):
        self.screen = screen
        self.downLuck = 1
        self.ItemGetBoost = 1

        self.image_h = self.screen.size[1]//15
        self.image_w = self.screen.size[0]//2
        self.image = pygame.Surface((self.image_w,self.image_h))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = self.screen.size[1]//2

        self.font = pygame.font.Font("./font/Ubuntu/Ubuntu-Medium.ttf",self.image_h -15)
        self.text = self.font.render("X1luck",False,(255,255,255))
        self.textrect = self.text.get_rect()# 3個按鈕ↆ
        self.textbg_size = (self.image_w - 3*self.image_h -6,self.image_h -6)
        self.textrect.center = (self.image_h*2+3 + self.textbg_size[0]//2,self.image_h//2)

        self.addButton = Button(3,3,self.image_h-6,self.image_h-6,"+",(90,90,90),(255,255,255),(30,30,30),20,border_radius=10)
        self.reduceButton = Button(3+self.image_h,3,self.image_h-6,self.image_h-6,"-",(90,90,90),(255,255,255),(30,30,30),20,border_radius=10)
        self.resetButton = Button(self.image_w - self.image_h +3,3,self.image_h-6,self.image_h-6,"reset",(90,90,90),(255,255,255),(30,30,30),20,border_radius=10)

    def update(self):
        if self.screen.scene == SCENE_SETTING:
            luckboost = self.screen.roll.baseLuckBoost
            if self.addButton.handle_event(self.screen.event,(self.rect.x,self.rect.y)) :
                self.downLuck *= 2
                if self.downLuck >1: self.downLuck = 1

            if self.reduceButton.handle_event(self.screen.event,(self.rect.x,self.rect.y)):
                self.downLuck /= 2
                if self.downLuck * luckboost <1:
                    self.downLuck = 1/luckboost

            if self.resetButton.handle_event(self.screen.event,(self.rect.x,self.rect.y)):
                self.downLuck = 1

            self.ItemGetBoost = abs(math.log10(self.downLuck) *-1 +1)

            self.text = self.font.render(f"x{self.downLuck * luckboost:.2f} Luck , x{self.ItemGetBoost:.2f}item",False,(0,0,0))
            self.textrect = self.text.get_rect()
            self.textrect.center = (self.image_h*2+3 + self.textbg_size[0]//2,self.image_h//2)

    def draw(self):
        if self.screen.scene == SCENE_SETTING:
            self.image.fill((0,0,0))
            self.image.set_colorkey((0,0,0))

            self.addButton.draw(self.image)
            self.reduceButton.draw(self.image)
            self.resetButton.draw(self.image)
            pygame.draw.rect(self.image,(50,50,50),(self.image_h*2+3,3,self.textbg_size[0],self.textbg_size[1]),border_radius= 10)
            self.image.blit(self.text,self.textrect)

            self.screen.screen.blit(self.image,self.rect)