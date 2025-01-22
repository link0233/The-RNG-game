import pygame
from config import *

class item:
    def __init__(self,name:str , rarity: int ,rarity_count: int,image_path: str, item_type: str,screen):
        """
        name: 物品名稱
        rarity : 該物品的稀有度
        rarity_count : 該物品稀有度排名
        image_path : 該物品的圖案路徑
        item_type : 物品型態，分為"normalItem" 以及 "specialItem" 以及 "extraItem"
        screen : 繪製的視窗
        """
        self.name = name
        self.rarity = rarity
        self.rarity_count = rarity_count
        self.rolled_image_path = image_path
        self.item_type = item_type
        self.screen = screen
        self.canRoll = True

        pygame.font.init()
        self.font = pygame.font.Font(None,50)

        # 創建圖片
        self.rolled_image = pygame.image.load(image_path).convert_alpha()
        self.rolled_image.set_colorkey((0,0,0))# 去背
        self.rolled_rect        = self.rolled_image.get_rect()
        self.rolled_rect.center = (SCREENSIZEX//2,SCREENSIZEY//2) #一律放在螢幕中間


        #顯示在物品欄中的
        if self.item_type == "normalItem":
            self.item_image_w      = SCREENSIZEX//4*3
            self.item_image_h      = SCREENSIZEY//5
            self.item_name_image_w = self.item_image_w//5*2
            self.rarity_image_w    = self.item_image_w //5 * 2
            self.count_w           = self.item_image_w //5

            self.item_image      = pygame.Surface((self.item_image_w,self.item_image_h))
            self.not_get_image   = self.font.render("???",True,(0,0,0))
            self.rarity_image    = self.font.render(f"1 in {self.rarity}",True,(0,0,0))
            self.item_name_image = self.font.render(self.name,True,(0,0,0))

            self.item_rect        = self.item_image.get_rect()
            self.item_name_rect   = self.item_name_image.get_rect()
            self.not_get_rect     = self.not_get_image.get_rect()
            self.rarity_rect      = self.rarity_image.get_rect()

            self.item_rect.x           = 0
            self.item_rect.y           = rarity_count * self.item_image_h
            self.item_name_rect.center = (self.item_name_image_w//2,self.item_image_h//2)
            self.not_get_rect.center   = (self.item_image_w//2,self.item_image_h//2)
            self.rarity_rect.center    = (self.item_name_image_w + self.rarity_image_w//2 ,self.item_image_h//2)

        if self.item_type == "specialItem":
            # 大小
            self.item_image_w      = SCREENSIZEX//2
            self.item_image_h      = SCREENSIZEY//6
            self.item_name_image_h = self.item_image_h//4-5
            self.rarity_image_h    = self.item_image_h//4-5
            #圖
            self.item_image      = pygame.Surface((self.item_image_w,self.item_image_h))
            self.not_get_image   = self.font.render("???",True,(0,0,0))
            self.rarity_image    = self.font.render(f"1 in {self.rarity}",True,(0,0,0))
            self.item_name_image = self.font.render(self.name,True,(0,0,0))
            #set rect
            self.item_rect        = self.item_image.get_rect()
            self.item_name_rect   = self.item_name_image.get_rect()
            self.not_get_rect     = self.not_get_image.get_rect()
            self.rarity_rect      = self.rarity_image.get_rect()
            #定位
            self.item_rect.x           = (self.rarity_count %2) * self.item_image_w
            self.item_rect.y           = 0
            self.item_name_rect.center = (self.item_image_w//4,self.item_image_h//2)
            self.not_get_rect.center   = (self.item_image_w//2,self.item_image_h//2)
            self.rarity_rect           = (self.item_image_w//4*3,self.item_image_h//2)

    def checkCanRoll(self):
        """
        更興是否可以抽取的狀態
        extraItem恆不能抽
        specialItem 只能有一個
        normalItem 無上限
        可以直接回傳是否能抽
        """
        self.canRoll = True
        if self.item_type == "extraItem" : self.canRoll = False ; return False
        if self.item_type == "normalItem": return True
        if self.item_type == "specialItem":
            if self.name in self.screen.inventory.inventoryData[self.item_type]:
                self.canRoll = False
                return False#有就不能
            else: return True 
        
    def draw_rolled(self):
        self.screen.screen.blit(self.rolled_image,self.rolled_rect)

    def draw_itemList(self,count:int ,get:bool ,move:int ):
        """
        count: 數量
        get: 是否有取得
        move: 位移距離
        """
        self.item_image.fill((255,55,55))
        self.item_image.set_colorkey((255,55,55))#清空
        if self.item_type == "normalItem" and self.screen.inventory.UI.scene == 1:
            if get == False:
                self.item_image.blit(self.not_get_image,self.not_get_rect)
            else:
                #其他兩個一經設定好的
                self.item_image.blit(self.item_name_image,self.item_name_rect)
                self.item_image.blit(self.rarity_image,self.rarity_rect)

                #唯獨數量會變所以不能先設定
                count_image = self.font.render(str(count),True,(0,0,0))
                count_rect = count_image.get_rect()
                count_rect.center = (self.item_name_image_w + self.rarity_image_w + self.count_w//2 ,self.item_image_h//2)
                self.item_image.blit(count_image , count_rect)

            self.item_rect.y           = self.rarity_count * self.item_image_h + move
        
        if self.item_type == "specialItem" and self.screen.inventory.UI.scene == 2:
            if get == False:
                self.item_image.blit(self.not_get_image,self.not_get_rect)
            if get == True:
                self.item_image.blit(self.item_name_image,self.item_name_rect)
                self.item_image.blit(self.rarity_image,self.rarity_rect)

            self.item_rect.y = (self.rarity_count - self.rarity_count%2)//2 * self.item_image_h + move
            
        
        self.screen.screen.blit(self.item_image,self.item_rect)
        

    def play_animation(self):
        if self.name == "1K":
            self.animation_wait(30)
            self.animation_showText("It first special item : )",180,Gradient = True , GradientTime= 30)
            self.animation_wait(30)
            self.animation_showText("When can roll (v0.2), I join it",180,Gradient = True , GradientTime= 30)
            self.animation_wait(30)
            self.animation_showText("This was best item then",180,Gradient = True , GradientTime= 30)
            self.animation_wait(30)
            self.animation_showText("But I remove it at v0.3.5.5 because I want it be a special item",180,Gradient = True , GradientTime= 30)
            self.animation_wait(30)
            self.animation_showText("I rejoin it at v0.4.2",180,Gradient = True , GradientTime= 30)
            self.animation_wait(30)
            self.animation_showText("It also first special item",180,Gradient = True , GradientTime= 30)
            self.animation_wait(30)
            self.animation_showText("It not easy to got then",180,Gradient = True , GradientTime= 30)
            self.animation_wait(30)
            self.animation_showText("Because this game don't have any luckboost then",180,Gradient = True , GradientTime= 30)
            self.animation_wait(30)

        if self.name == "2025HappyNewYear":
            self.animation_wait(30)
            self.animation_showText("HappyNewYear !!",180,Gradient = True , GradientTime= 30)
            self.animation_wait(30)
            self.animation_showText("Now also around Chinese New Year :) ",180,Gradient = True , GradientTime= 30)
            self.animation_wait(30)
            self.animation_showText("2025 is special",180,Gradient = True , GradientTime= 30)
            self.animation_wait(30)
            self.animation_showText("2025 = 45^2 = (1+2+3+4+5+6+7+8+9)^2",180,Gradient = True , GradientTime= 30)
            self.animation_wait(30)
            self.animation_showText("Good Luck",180,Gradient = True , GradientTime= 30)

    def animation_showText(self,text:str,time:int ,
                           text_color = (255,255,255),
                           Gradient:bool = False ,
                           GradientTime:int = 0):
        """
        將會在正中間顯示文字
        text: 顯示的文字
        text_color : 文字顏色，預設為白色
        time: 持續時間
        Gradient: 漸變特效
        GradientTime : 漸變特效持續時間
        """
        textfont = pygame.font.match_font("arial")
        textFont = pygame.font.Font(textfont,100)
        textimage = textFont.render(text,True,text_color)
        textRect = textimage.get_rect()
        textRect.center = (SCREENSIZEX//2,SCREENSIZEY//2)
        for t in range(time):
                if Gradient:
                    transparency = 255
                    #漸出
                    if t <= GradientTime:
                        transparency = t/GradientTime * 255
                    #中間
                    if t >= GradientTime and t < time - GradientTime:
                        transparency = 255
                    # 尾
                    if t >= time - GradientTime:
                        _t = t - (time-GradientTime)
                        transparency = 255 - (_t/GradientTime)*255
                    #重新加載圖片後再做透明變化
                    textimage = textFont.render(text,True,text_color)
                    textimage.set_alpha(transparency)

                self.screen.screen.fill((0,0,0))
                self.screen.screen.blit(textimage,textRect)
                self.UpdateScreenWhenPlayingAnimation()
    
    def animation_wait(self,time:int):
        """
        在撥動畫時等遺下
        """
        self.screen.screen.fill((0,0,0))
        for _ in range(time): self.UpdateScreenWhenPlayingAnimation()

    def UpdateScreenWhenPlayingAnimation(self):
        for event in self.screen.event:
            if event.type == pygame.QUIT:
                self.screen.save()
                pygame.quit()
                import sys ; sys.exit()
        
        self.screen.clock.tick(60)
        pygame.display.update()