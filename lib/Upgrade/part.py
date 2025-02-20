import pygame
from config import *

from lib.GUI.button import Button
from lib.functions.functions import draw_text

class part:              
    def __init__(self , screen , pos :list , title: str , Description : str , cost :str ):
        """
        screen : screen
        pos : (x ,y) 所處位置
        title : 標題
        Description : 說明文字
        cost : 需要的錢錢文字
        必須附上 ， check_can_buy 以及 pay 函式處理購買事件
        """
        self.screen = screen
        self.title = title
        self.Description = Description
        self.cost = cost

        # state
        self.hovering = False
        self.side_show = False
        self.bought = False
        #button
        self.buy_button = Button(self.screen.size[0] //3 *2.25 , self.screen.size[1] -(self.screen.size[1]//10 - 10) ,
                                 self.screen.size[0] //6,self.screen.size[1]//10 - 20,
                                 "Buy" , border_radius= 10)
        # position
        self.part_x = pos[0] * self.screen.size[0]//15 +100
        self.part_y = pos[1] * (self.screen.size[0]//15 + 20) + self.screen.size[1] //2
        # image
        self.part_width                = self.part_height = self.screen.size[0]//15
        self.side_width                = self.screen.size[0] //3
        self.side_height               = self.screen.size[1]
        self.side_title_height         = self.screen.size[1]//10
        self.side_buy_button_height    = self.screen.size[1]//10
        self.side_Description_height   = (self.screen.size[1] - self.side_title_height - self.side_buy_button_height)//2
        self.side_cost_height          = self.side_Description_height

        self.part_image                = pygame.Surface((self.part_width,self.part_height))
        self.side_image                = pygame.Surface((self.side_width,self.side_height))
        self.part_hover_cover_image    = pygame.Surface((self.part_width,self.part_height))
        self.not_buy_image             = pygame.Surface((self.part_width,self.part_height))

        self.part_image               .fill((255,255,255))
        self.side_image               .fill((150,150,150))
        self.part_hover_cover_image   .fill((90,90,90))
        self.not_buy_image            .fill((90,90,90))

        self.part_hover_cover_image   .set_alpha(150)
        self.not_buy_image            .set_alpha(150)

        # text
        pygame.font.init()
        self.side_title_font          = pygame.font.Font("./font/Ubuntu/Ubuntu-Bold.ttf" , self.side_title_height - 40)
        self.side_Description_font    = pygame.font.Font("./font/Lato/Lato-Regular.ttf" , 40)
        self.side_cost_font           = self.side_Description_font

        self.side_title_image         = self.side_title_font        .render(self.title         , True , (255,255,255))
        self.side_Description_image   = self.side_Description_font  .render(self.Description   , True , (255,255,255))
        self.side_cost_image          = self.side_cost_font         .render(self.cost          , True , (255,255,255))

        # rect
        self.part_rect                = self.part_image.get_rect()
        self.side_rect                = self.side_image.get_rect()
        self.side_title_rect          = self.side_title_image.get_rect()
        # self.side_Description_rect    = self.side_Description_image.get_rect()
        # self.side_cost_rect           = self.side_cost_image.get_rect()

        self.side_rect.topright       = (self.screen.size[0] , 0)
        self.side_title_rect.center   = (self.side_width // 2 + self.side_rect.x ,self.side_title_height //2)

    def update(self , mapPos:list):
        # 處理按鈕顏色
        # 沒有購買時
        if not self.bought:
            canbuy = self.check_can_buy()
            if canbuy :
                self.buy_button.color = (0,255,0)
                self.buy_button.hover_color = (0,150,0)
            else:
                self.buy_button.color = (255,0,0)
                self.buy_button.hover_color = (150,0,0)
        # else:
        #     self.buy_button.text
        # rect
        self.part_rect.x = self.part_x + mapPos[0]
        self.part_rect.y = self.part_y + mapPos[1]
        # 自己的滑鼠事件爭測
        for event in self.screen.event:
            if event.type == pygame.MOUSEMOTION:
                # 檢查滑鼠是否在按鈕範圍內
                if self.part_rect.collidepoint(event.pos[0],event.pos[1]):
                    self.hovering = True
                else:
                    self.hovering = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.part_rect.collidepoint(event.pos[0],event.pos[1]):
                        self.side_show = True
                    else:# 點到旁邊
                        # 點到旁邊顯示的不算
                        if self.side_show:
                            if not self.side_rect.collidepoint(event.pos[0],event.pos[1]):
                                self.side_show = False
                        else:
                            self.side_show = False
                        
        # 按鈕
        if self.buy_button.handle_event(self.screen.event) and  self.check_can_buy():
            self.bought = True
            self.buy()
            self.buy_button.create_text("bought")
            self.buy_button.color = (200,200,200)
            self.buy_button.color = (100,100,100)

    def draw(self):
        self.screen.screen.blit(self.part_image,self.part_rect)

        if self.hovering :
            self.screen.screen.blit(self.part_hover_cover_image,self.part_rect)

        if not self.bought:
            self.screen.screen.blit(self.not_buy_image,self.part_rect)

    def draw_side(self):
        """
        側邊因為必須要顯示於所有升級之上，所以得拉出來
        """
        if self.side_show :
            self.screen.screen.blit(self.side_image,self.side_rect)
            self.buy_button.draw(self.screen.screen)
            self.screen.screen.blit(self.side_title_image,self.side_title_rect)
            draw_text(self.screen.screen,self.Description,self.side_Description_font,(255,255,255) , (self.side_rect.x +20 , self.side_title_height,self.side_width,self.side_Description_height) , 30)
            draw_text(self.screen.screen,self.cost       ,self.side_cost_font       ,(255,255,255) , (self.side_rect.x +20 , self.side_title_height + self.side_Description_height ,self.side_width,self.side_cost_height) , 30)
