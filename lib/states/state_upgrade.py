import pygame
from config import *

#from lib.GUI.button import Button
from lib.GUI.label import label
#from lib.functions.bigNumber import BigNumber

class state_upgrade:
    def __init__(self , screen , text:str , x , y , textcolor , bgcolor , text_font = "./font/Lato/Lato-Light.ttf"):
        """
        寬度訂畫面的一半
        高度定畫面高度的1/20
        :param x: 限0~1 左邊右邊
        :param y: 由上至下
        """
        self.screen = screen
        self.text = text
        self.x = x
        self.y = y
        self.textcolor = textcolor
        self.bgcolor = bgcolor

        self.button_maincolor = (94, 216, 117)
        self.button_mainHovercolor = (85, 183, 103)
        self.bg_color = bgcolor

        # states
        self.click = False
        self.max_click = False

        # image
        self.size = (self.screen.size[0]//2 , self.screen.size[1] // 20)
        self.image = pygame.Surface(self.size , pygame.SRCALPHA)

        self.text_label = label(self.text , (5,5,self.size[0] - 10 , self.size [1] - 10) , self.textcolor , -1 , "left" , text_font )

        #self.buy_button = Button(self.size[0]/10*8 +5 , 5 , self.size[0]//10 - 10 , self.size[1] - 10 , "Buy" , self.button_maincolor , (255,255,255) , self.button_mainHovercolor , border_radius= 5)

        # rect
        self.rect = self.image.get_rect()
        self.rect.x = self.size[0] * self.x
        self.rect.y = self.size[1] * self.y

    def update(self , move):
        # reset
        self.click = False
        self.max_click = False

        for event in self.screen.event:
            if event.type == pygame.MOUSEMOTION:
                # 檢查滑鼠是否在按鈕範圍內
                if self.rect.collidepoint(event.pos[0] - move[0],event.pos[1] - move[1]): 
                    self.bg_color = (100,100,100,100)
                else:
                    self.bg_color = self.bgcolor
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.rect.collidepoint(event.pos[0] - move[0],event.pos[1] - move[1]):
                        self.click = True
                if event.button == 3:
                    if self.rect.collidepoint(event.pos[0] - move[0],event.pos[1] - move[1]):
                        self.max_click = True

    def draw(self , screen):
        #self.image.fill((0,0,0))
        self.image.fill((0,0,0,0))

#        self.buy_button.draw(self.image)
        pygame.draw.rect(self.image , self.bg_color , (0,0,self.size[0] , self.size[1]) , border_radius= 5)
        self.text_label.draw(self.image)

        screen.blit(self.image,self.rect)
