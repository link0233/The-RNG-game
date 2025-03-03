import pygame
from config import *

from lib.GUI.button import Button
from lib.Upgrade.buypart_animation import buypart_animation
from lib.functions.functions import draw_text
from lib.GUI.label import label
from lib.functions.bigNumber import BigNumber

class part:              
    def __init__(self , screen , pos :list , title: str , Description : str , cost :str , unlockneed :list , pay_need :list , type: str , max_level :int = 1):
        """
        :param screen : screen
        :param pos : (x ,y) 所處位置
        :param title : 標題
        :param Description : 說明文字
        :param cost : 需要的錢錢文字
        :param unlockneed : 解鎖需要升級 ["升級名稱"] ,若為空則直接解鎖
        :param pay_need : 購買所需要的物品 [ "物品名稱" , 數量 ]
        :param type : 升級類型，會有不同的升級特效和圖案
            cash : 錢錢
            luck : 幸運
            xp   : xp
            point: point
        :param max_level: 最高等級上限
        """
        self.screen = screen
        self.title = title
        self.Description = Description
        self.cost = cost
        self.unlockneed = unlockneed
        self.pos = pos
        self.pay_need = pay_need
        self.type = type
        self.level = 0
        self.max_level = max_level

        # state
        self.hovering = False
        self.side_show = False
        self.bought = False
        self.unlock = False
        # animation
        self.buy_animation = None
        #button
        self.buy_button = Button(self.screen.size[0] //3 *2.25 , self.screen.size[1] -(self.screen.size[1]//10 - 10) ,
                                 self.screen.size[0] //6,self.screen.size[1]//10 - 20,
                                 "Buy" , border_radius= 10,font = "./font/Ubuntu/Ubuntu-Light.ttf")
        # position
        self.part_x = (pos[0]*2+1) * self.screen.size[0]//15 +100
        self.part_y = pos[1] * (self.screen.size[0]//15 + 20) + self.screen.size[1] //2
        # image
        self.part_width                = self.part_height = self.screen.size[0]//15
        self.side_width                = self.screen.size[0] //3
        self.side_height               = self.screen.size[1]
        self.side_title_height         = self.screen.size[1]//10
        self.side_buy_button_height    = self.screen.size[1]//10
        self.side_level_h              = self.screen.size[1]//15
        self.side_Description_height   = (self.screen.size[1] - self.side_title_height - self.side_buy_button_height - self.side_level_h)//2
        self.side_cost_height          = self.side_Description_height

        self.part_image                = pygame.Surface((self.part_width,self.part_height))
        self.side_image                = pygame.Surface((self.side_width,self.side_height))
        self.part_hover_cover_image    = pygame.Surface((self.part_width,self.part_height))
        self.not_buy_image             = pygame.Surface((self.part_width,self.part_height))

        

        type_image                     = pygame.transform.smoothscale(pygame.image.load(f"./images/upgrade/{self.type}.png"),(self.part_width,self.part_height))

        type_image.set_colorkey((255,255,255))
        self.side_image               .fill((150,150,150))

        pygame.draw.rect(self.part_image,(255,255,255) , (0,0,self.part_width , self.part_height),border_radius = 10)
        self.part_image                .blit(type_image,(0,0,self.part_width,self.part_height))
        pygame.draw.rect(self.part_hover_cover_image,(90,90,90) , (0,0,self.part_width , self.part_height),border_radius = 10)
        pygame.draw.rect(self.not_buy_image,(90,90,90) , (0,0,self.part_width , self.part_height),border_radius = 10)

        self.part_hover_cover_image   .set_alpha(100)
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

        self.side_rect.topright       = (self.screen.size[0] , 0)
        self.side_title_rect.center   = (self.side_width // 2 + self.side_rect.x ,self.side_title_height //2)
        # label
        self.side_level_label          = label("[0/1]" , (self.side_rect.x,self.side_title_height , self.side_width , self.side_level_h) , (255,255,255),-1,"center","./font/Ubuntu/Ubuntu-Bold.ttf")

    def all_set_update(self):
        """
        全部設置好後所進行更改部分資訊
        """
        self.side_level_label.change_text(f"[{self.level}/{self.max_level}]")
        if self.level > 0:
            self.buy_button.color = (200,200,200)
            self.buy_button.hover_color = (100,100,100)
            if self.max_level == 1:
                self.buy_button.create_text("bought")
            elif self.max_level == self.level:
                self.buy_button.create_text("maxed")

    def update(self , mapPos:list):
        # 更興動畫
        if self.buy_animation:
            self.buy_animation.update()
        # 處理按鈕顏色
        # 沒有購買時
        if self.level < self.max_level:
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
                if event.button == 1:                                           # 解鎖後才可以點
                    if self.part_rect.collidepoint(event.pos[0],event.pos[1]) and self.unlock:
                        self.side_show = True
                    else:# 點到旁邊
                        # 點到旁邊顯示的不算
                        if self.side_show:
                            if not self.side_rect.collidepoint(event.pos[0],event.pos[1]):
                                self.side_show = False
                        else:
                            self.side_show = False
                        
        # 按鈕                                                                              顯示時才可按
        if self.buy_button.handle_event(self.screen.event) and  self.check_can_buy() and self.side_show:
            self.bought = True
            self.level += 1
            self.side_level_label.change_text(f"[{self.level}/{self.max_level}]")
            self.buy()

            if self.max_level == 1:
                self.buy_button.color = (200,200,200)
                self.buy_button.hover_color = (100,100,100)
                self.buy_button.create_text("bought")
            elif self.max_level == self.level:
                self.buy_button.color = (200,200,200)
                self.buy_button.hover_color = (100,100,100)
                self.buy_button.create_text("maxed")
            # if self.level< self.max_level :
            #     self.buy_button.color = (200,200,200)
            #     self.buy_button.hover_color = (100,100,100)
            #     self.buy_button.create_text("buy")

            
            self.screen.upgrade.update_boost() # 購買後載入
            self.buy_animation = buypart_animation(self.type) # 放動畫

        # 山動畫
        if self.buy_animation:
            if self.buy_animation.end:
                self.buy_animation = None

    def draw(self):
        if self.unlock :
            self.screen.screen.blit(self.part_image,self.part_rect)
            if self.hovering :
                self.screen.screen.blit(self.part_hover_cover_image,self.part_rect)

            if not self.bought:
                self.screen.screen.blit(self.not_buy_image,self.part_rect)

            if self.buy_animation:
                self.buy_animation.draw(self.screen.screen,self.part_rect.center)

        # else:
        #     self.screen.screen.blit(self.locked_image , self.part_rect)

    def draw_line(self):
        """
        最底層
        """
        if self.unlock:
            for nupd in self.unlockneed:
                if nupd in self.screen.upgrade.main_upgrades:
                    p1 = self.screen.upgrade.main_upgrades[nupd] .part_rect.center
                    p2 = self.part_rect.center
                    pygame.draw.line(self.screen.screen,(100,100,100),p1,p2,5)

    def draw_side(self):
        """
        側邊因為必須要顯示於所有升級之上，所以得拉出來
        """
        if self.side_show :
            self.screen.screen.blit(self.side_image,self.side_rect)
            self.buy_button.draw(self.screen.screen)
            self.screen.screen.blit(self.side_title_image,self.side_title_rect)
            draw_text(self.screen.screen,self.Description,self.side_Description_font,(255,255,255) , (self.side_rect.x +20 , self.side_title_height + self.side_level_h,self.side_width-40,self.side_Description_height) , 30)
            draw_text(self.screen.screen,self.cost       ,self.side_cost_font       ,(255,255,255) , (self.side_rect.x +20 , self.side_title_height + self.side_level_h + self.side_Description_height ,self.side_width-40,self.side_cost_height) , 30)
            self.side_level_label.draw(self.screen.screen)

    def check_unlock(self ):
        """
        確定是否解鎖
        """
        self.unlock = True
        upgrade_state = self.screen.upgrade.main_upgrades
        for needupd in self.unlockneed:
            if needupd in upgrade_state :
                if upgrade_state[needupd] . bought == False:
                    self.unlock = False
            
    def check_can_buy(self):
        for p in self.pay_need:
            if p[0] == "cash":
                if not self.screen.inventory.inventoryData["cash"] >= p[1] * (self.level +1): return False

            if p[0] == "point":
                # if self.title == "point upgrade #1" :
                #     print(self.screen.states.point.size(p[1][0] * (self.level +1),p[1][1]))
                #if self.screen.states.point.size(p[1][0] * (self.level +1),p[1][1]) == 1 : return False
                #print(p)
                if self.screen.states.point.point <= BigNumber(p[1]) * (self.level +1) : return False 
                #else: return False
        if self.level >= self.max_level: return False

        return True
    
    def buy(self):
        for p in self.pay_need:
            if p[0] == "cash":
                self.screen.inventory.inventoryData["cash"] -= p[1]
            if p[0] == "point":
                self.screen.states.point.point -= BigNumber(p[1]) * (self.level +1)
               