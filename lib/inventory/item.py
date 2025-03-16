import pygame
from config import *

from lib.GUI.imageButton import *
from lib.functions.functions import draw_text
from lib.functions.bigNumber import BigNumber

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
        self.hover_state = False
        self.beside_show_state = False
        self.boost = BigNumber(1)
        self.Achievement_boost = BigNumber(1)

        pygame.font.init()
        CourierNew = pygame.font.match_font("Tahoma")
        self.font = pygame.font.Font(CourierNew,40)

        # 創建提示內容
        if   self.name == "100roll" : self.caption = "You roll 100 times !!!!!!!!!"
        elif self.name == "10000roll" : self.caption = "You roll 10000 times !!!!!!!!!"
        elif self.name == "10Htimeplayed" : self.caption = "You played 10H in this game!!"
        elif self.name == "2025HappyNewYear" : self.caption = "Hatch it around 2025 new year!!"
        elif self.name == "A lot of pi" : self.caption = "1e8 pi"
        elif self.name == "The Real pi" : self.caption = "get all pi and a lot of pi"

        # 創建圖片
        self.rolled_image = pygame.image.load(image_path).convert_alpha()
        self.rolled_image.set_colorkey((0,0,0))# 去背
        self.rolled_rect        = self.rolled_image.get_rect()
        self.rolled_rect.center = (SCREENSIZEX//2,SCREENSIZEY//2) #一律放在螢幕中間

    def loadImage(self):
        #顯示在物品欄中的
        if self.item_type == "normalItem":
            #主要的
            self.item_image_w      = SCREENSIZEX//5*3
            self.item_image_h      = SCREENSIZEY//7
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
            self.item_rect.y           = self.rarity_count * self.item_image_h
            self.item_name_rect.center = (self.item_name_image_w//2,self.item_image_h//2)
            self.not_get_rect.center   = (self.item_image_w//2,self.item_image_h//2)
            self.rarity_rect.center    = (self.item_name_image_w + self.rarity_image_w//2 ,self.item_image_h//2)
            #旁邊的
            #大小
            self.beside_w = SCREENSIZEX - self.item_image_w
            self.beside_h = SCREENSIZEY
            original_size = self.rolled_image.get_size()
            self.beside_showImage_w = self.beside_w
            scale_factor = self.beside_showImage_w / original_size[0]
            self.beside_showImage_h = original_size[1] * scale_factor

            self.beside_image = pygame.Surface((self.beside_w,self.beside_h))
            self.beside_image.set_colorkey((0,0,0))
            self.beside_showImage = pygame.transform.smoothscale(self.rolled_image,(self.beside_showImage_w,self.beside_showImage_h))
            self.beside_showImage.set_colorkey((0,0,0))

            self.beside_rect = self.beside_image.get_rect()
            self.beside_rect.x = self.item_image_w
            self.beside_rect.y = 0
            self.beside_showImage_rect = self.beside_showImage.get_rect()
            self.beside_showImage_rect.x = 0
            self.beside_showImage_rect.centery = SCREENSIZEY//4
            
            self.beside_image.blit(self.beside_showImage,self.beside_showImage_rect)

        if self.item_type == "specialItem":
            # 主要的
            # 大小
            self.item_image_w      = SCREENSIZEX//3
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
            self.item_name_rect.center = (self.item_image_w//10*3,self.item_image_h//2)
            self.not_get_rect.center   = (self.item_image_w//2,self.item_image_h//2)
            self.rarity_rect.center    = (self.item_image_w//10*8,self.item_image_h//2)
            #旁邊的
            #大小
            self.beside_w = SCREENSIZEX - self.item_image_w*2
            self.beside_h = SCREENSIZEY
            original_size = self.rolled_image.get_size()
            self.beside_showImage_w = self.beside_w
            scale_factor = self.beside_showImage_w / original_size[0]
            self.beside_showImage_h = original_size[1] * scale_factor

            self.beside_image = pygame.Surface((self.beside_w,self.beside_h))
            self.beside_image.set_colorkey((0,0,0))
            self.beside_showImage = pygame.transform.smoothscale(self.rolled_image,(self.beside_showImage_w,self.beside_showImage_h))
            self.beside_showImage.set_colorkey((0,0,0))

            self.beside_rect = self.beside_image.get_rect()
            self.beside_rect.x = self.item_image_w*2
            self.beside_rect.y = 0
            self.beside_showImage_rect = self.beside_showImage.get_rect()
            self.beside_showImage_rect.x = 0
            self.beside_showImage_rect.centery = SCREENSIZEY//4
            #波放動畫按鈕
            self.playAnimationButton = playAnimationButton(self.beside_image , self.beside_image,self.beside_w,self.beside_h)
            
            self.beside_image.blit(self.beside_showImage,self.beside_showImage_rect)

        if self.item_type == "extraItem":
            # 主要的
            # 大小
            self.item_image_w      = SCREENSIZEX//3
            self.item_image_h      = SCREENSIZEY//6
            self.item_name_image_h = self.item_image_h//4-5
            #圖
            self.item_image      = pygame.Surface((self.item_image_w,self.item_image_h))
            self.not_get_image   = self.font.render("???",True,(0,0,0))
            self.item_name_image = self.font.render(self.name,True,(0,0,0))
            #set rect
            self.item_rect        = self.item_image.get_rect()
            self.item_name_rect   = self.item_name_image.get_rect()
            self.not_get_rect     = self.not_get_image.get_rect()
            #定位
            self.item_rect.x           = (self.rarity_count %2) * self.item_image_w
            self.item_rect.y           = 0
            self.item_name_rect.center = (self.item_image_w//2,self.item_image_h//2)
            self.not_get_rect.center   = (self.item_image_w//2,self.item_image_h//2)
            #旁邊的
            #大小
            self.beside_w = SCREENSIZEX - self.item_image_w*2
            self.beside_h = SCREENSIZEY
            original_size = self.rolled_image.get_size()
            self.beside_showImage_w = self.beside_w
            scale_factor = self.beside_showImage_w / original_size[0]
            self.beside_showImage_h = original_size[1] * scale_factor

            self.beside_image = pygame.Surface((self.beside_w,self.beside_h))
            self.beside_image.set_colorkey((0,0,0))
            self.beside_showImage = pygame.transform.smoothscale(self.rolled_image,(self.beside_showImage_w,self.beside_showImage_h))
            self.beside_showImage.set_colorkey((0,0,0))
            self.beside_captionImage = pygame.Surface((self.beside_w,self.beside_h//3))
            self.beside_captionImage.set_colorkey((0,0,0))
            draw_text(self.beside_captionImage,self.caption,self.font,(255,255,255),(0,0,self.beside_w,self.beside_h//3),50)

            self.beside_rect = self.beside_image.get_rect()
            self.beside_rect.x = self.item_image_w*2
            self.beside_rect.y = 0
            self.beside_showImage_rect = self.beside_showImage.get_rect()
            self.beside_showImage_rect.x = 0
            self.beside_showImage_rect.centery = SCREENSIZEY//4
            self.beside_caption_rect = self.beside_captionImage.get_rect()
            self.beside_caption_rect.center = (self.beside_w//2,self.beside_h//2)
            #波放動畫按鈕
            self.playAnimationButton = playAnimationButton(self.beside_image , self.beside_image,self.beside_w,self.beside_h)
            
            self.beside_image.blit(self.beside_showImage,self.beside_showImage_rect)
            self.beside_image.blit(self.beside_captionImage,self.beside_caption_rect)
        self.hover_image = pygame.Surface((self.item_image_w,self.item_image_h))
        self.hover_image.fill((121, 51, 35))
        self.hover_image.set_alpha(250)
        self.hover_rect = self.hover_image.get_rect()
        self.hover_rect.x = 0
        self.hover_rect.y = 0

    def unloadImage(self):
        if self.item_type == "normalItem":
            #主要的
            self.item_image_w      = SCREENSIZEX//5*3
            self.item_image_h      = SCREENSIZEY//7
            self.item_name_image_w = self.item_image_w//5*2
            self.rarity_image_w    = self.item_image_w //5 * 2
            self.count_w           = self.item_image_w //5

            self.item_image      = None
            self.not_get_image   = None
            self.rarity_image    = None
            self.item_name_image = None

            self.item_rect        = None
            self.item_name_rect   = None
            self.not_get_rect     = None
            self.rarity_rect      = None
            #旁邊的
            #大小
            self.beside_w = SCREENSIZEX - self.item_image_w
            self.beside_h = SCREENSIZEY
            original_size = self.rolled_image.get_size()
            self.beside_showImage_w = self.beside_w
            scale_factor = self.beside_showImage_w / original_size[0]
            self.beside_showImage_h = original_size[1] * scale_factor

            self.beside_image = None
            self.beside_showImage = None

            self.beside_rect = None
            self.beside_showImage_rect = None

        if self.item_type == "specialItem":
            # 主要的
            # 大小
            self.item_image_w      = SCREENSIZEX//3
            self.item_image_h      = SCREENSIZEY//6
            self.item_name_image_h = self.item_image_h//4-5
            self.rarity_image_h    = self.item_image_h//4-5
            #圖
            self.item_image      = None
            self.not_get_image   = None
            self.rarity_image    = None
            self.item_name_image = None
            
            #set rect
            self.item_rect        = None
            self.item_name_rect   = None
            self.not_get_rect     = None
            self.rarity_rect      = None
            #大小
            self.beside_w = SCREENSIZEX - self.item_image_w*2
            self.beside_h = SCREENSIZEY
            original_size = self.rolled_image.get_size()
            self.beside_showImage_w = self.beside_w
            scale_factor = self.beside_showImage_w / original_size[0]
            self.beside_showImage_h = original_size[1] * scale_factor

            self.beside_image = None
            self.beside_showImage = None

            self.beside_rect = None
            self.beside_rect.x = self.item_image_w*2
            self.beside_showImage_rect = None
            #波放動畫按鈕
            self.playAnimationButton = None

        if self.item_type == "extraItem":
            # 主要的
            #圖
            self.item_image      = None
            self.not_get_image   = None
            self.item_name_image = None
            #set rect
            self.item_rect        = None
            self.item_name_rect   = None
            self.not_get_rect     = None
            #旁邊的
            #大小


            self.beside_image = None
            self.beside_showImage = None
            self.beside_captionImage = None

            self.beside_rect = None
            self.beside_showImage_rect = None
            self.beside_caption_rect = None
            #波放動畫按鈕
            self.playAnimationButton = None
        self.hover_image = None
        self.hover_rect = None

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

    def checkExtraGet(self):
        """
        回傳此extra item是否獲得，如果獲得，則視為當前抽取物，回傳為bool
        """
        if self.item_type != "extraItem": return False
        get = False
        if self.name in self.screen.inventory.inventoryData["extraItem"]:
            if self.screen.inventory.inventoryData["extraItem"][self.name] >= 1:
                return False
            else : get = True
        else: get = True
        if get:
            if self.name == "100roll":
                if self.screen.states.states["rolls"] >= 100:
                    print("a")
                    return True
            if self.name == "10000roll":
                if self.screen.states.states["rolls"] >= 10000:
                    return True
            if self.name == "10Htimeplayed":
                if self.screen.states.states["playtime"] >= 36000:
                    return True
            if self.name == "A lot of pi":
                if "pi" in self.screen.inventory.inventoryData["normalItem"]:
                    if self.screen.inventory.inventoryData["normalItem"]["pi"] > BigNumber("1e8"):
                        return True
            if self.name == "The Real pi":
                c = 0
                if "pi" in self.screen.inventory.inventoryData["normalItem"]:
                    if self.screen.inventory.inventoryData["normalItem"]["pi"] > BigNumber("1e13"):
                        c +=1
                if "3141" in self.screen.inventory.inventoryData["specialItem"]:
                    if self.screen.inventory.inventoryData["specialItem"]["3141"] >= 1:
                        c +=1
                if "314159" in self.screen.inventory.inventoryData["specialItem"]:
                    if self.screen.inventory.inventoryData["specialItem"]["314159"] >= 1:
                        c +=1
                if "31415926" in self.screen.inventory.inventoryData["specialItem"]:
                    if self.screen.inventory.inventoryData["specialItem"]["31415926"] >= 1:
                        c +=1
                if c >= 4 : return True
            else :return False
        return False

    def get_boost(self):
        return (self.Achievement_boost * self.screen.setting.ChangeLuckBoost.ItemGetBoost)#.__repr__()

    def draw_rolled(self,movex = 0,movey = 0):
        show_rect = self.rolled_image.get_rect()
        show_rect.x = self.rolled_rect.x + movex
        show_rect.y = self.rolled_rect.y + movey
        self.screen.screen.blit(self.rolled_image,show_rect)

    def draw_itemList(self, count ,get:bool ,move:int ):
        """
        count: 數量
        get: 是否有取得
        move: 位移距離
        """
        #確認是否有被點擊
        clicked = False
        canShow = False
        if self.item_type == "normalItem" and self.screen.inventory.ItemUI.scene == 1: canShow = True
        elif self.item_type == "specialItem" and self.screen.inventory.ItemUI.scene == 2: canShow = True
        elif self.item_type == "extraItem" and self.screen.inventory.ItemUI.scene == 3: canShow = True
        
        for event in self.screen.event:
            if event.type == pygame.MOUSEMOTION:
                # 檢查滑鼠是否在按鈕範圍內
                if self.item_rect.collidepoint(event.pos):
                    self.hover_state = True
                else:
                    self.hover_state = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.item_rect.collidepoint(event.pos) and canShow:
                        clicked = True
                        self.screen.inventory.ItemUI.hide_allBeside()
                        self.beside_show_state = True
        #繪製
        self.item_image.fill((255,55,55))
        self.item_image.set_colorkey((255,55,55))#清空

        if self.item_type == "normalItem" and self.screen.inventory.ItemUI.scene == 1:
            if self.hover_state: self.item_image.blit(self.hover_image,self.hover_rect)
            if get == False:
                self.item_image.blit(self.not_get_image,self.not_get_rect)
            else:
                #其他兩個一經設定好的
                self.item_image.blit(self.item_name_image,self.item_name_rect)
                self.item_image.blit(self.rarity_image,self.rarity_rect)

                #唯獨數量會變所以不能先設定
                if isinstance(count , BigNumber):
                    count_image = self.font.render(f"{count.__repr__(True)}",True,(0,0,0))
                else:
                    count_image = self.font.render(f"{count}",True,(0,0,0))
                count_rect = count_image.get_rect()
                count_rect.center = (self.item_name_image_w + self.rarity_image_w + self.count_w//2 ,self.item_image_h//2)
                self.item_image.blit(count_image , count_rect)
                #旁邊的
                if self.beside_show_state : 
                    self.screen.screen.blit(self.beside_image,self.beside_rect)
                    

            self.item_rect.y           = self.rarity_count * self.item_image_h + move
             
        if self.item_type == "specialItem" and self.screen.inventory.ItemUI.scene == 2:
            if self.hover_state: self.item_image.blit(self.hover_image,self.hover_rect)
            if get == False:
                self.item_image.blit(self.not_get_image,self.not_get_rect)
            if get == True:
                self.item_image.blit(self.item_name_image,self.item_name_rect)
                self.item_image.blit(self.rarity_image,self.rarity_rect)
                #旁邊的
                if self.beside_show_state : 
                    
                    self.playAnimationButton.check_clicked(self.screen.event,(self.item_image_w*2,0))
                    self.playAnimationButton.update_hover_state(self.screen.event,(self.item_image_w*2,0))
                    self.playAnimationButton.draw()
                    if self.playAnimationButton.is_clicked : self.play_animation()

                    self.screen.screen.blit(self.beside_image,self.beside_rect)

            self.item_rect.y = (self.rarity_count - self.rarity_count%2)//2 * self.item_image_h + move    

        if self.item_type == "extraItem" and self.screen.inventory.ItemUI.scene == 3:
            if self.hover_state: self.item_image.blit(self.hover_image,self.hover_rect)
            if get == False:
                self.item_image.blit(self.not_get_image,self.not_get_rect)
            if get == True:
                self.item_image.blit(self.item_name_image,self.item_name_rect)
                #旁邊的
                if self.beside_show_state : 

                    self.playAnimationButton.check_clicked(self.screen.event,(self.item_image_w*2,0))
                    self.playAnimationButton.update_hover_state(self.screen.event,(self.item_image_w*2,0))
                    self.playAnimationButton.draw()
                    if self.playAnimationButton.is_clicked : self.play_animation()

                    self.screen.screen.blit(self.beside_image,self.beside_rect)

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

        elif self.name == "100roll":
            self.animation_wait(300)
            self.animation_showText("WOW You roll 100 times",210,Gradient=True,GradientTime= 60)
            self.animation_showText("It's must be easy and fast to get",210,Gradient=True,GradientTime= 60)
            self.animation_showText("It's the first extra item",210,Gradient=True,GradientTime= 60)
            self.animation_showText("Is it also your first extra item?",210,Gradient=True,GradientTime= 60)
            self.animation_wait(300)

        elif self.name == "CURV":
            self.animation_showText("CURV",234,Gradient = True , GradientTime= 30)
            self.animation_wait(30)
            self.animation_wait(30)
            self.animation_showText("It's just abbreviation",234,Gradient = True , GradientTime= 30)
            self.animation_wait(30)
            self.animation_showText("It's full name is commonuncommonrareveryrare",234,Gradient = True , GradientTime= 30)
            self.animation_wait(30)
            self.animation_showText("yes It's very long",234,Gradient = True , GradientTime= 30)
            self.animation_wait(30)
            self.animation_showText("and It's rarity also is 2x4x8x50",234,Gradient = True , GradientTime= 30)
            self.animation_wait(30)

        elif self.name == "watermelon":
            self.animation_showText("OH this is delicious",234,Gradient = True , GradientTime= 30)
            self.animation_wait(30)
            self.animation_showText("Simple have red and yellow",234,Gradient = True , GradientTime= 30)
            self.animation_wait(30)
            self.animation_showText("It's can make the juise",234,Gradient = True , GradientTime= 30)
            self.animation_wait(30)
            self.animation_showText("It's verygood on Summer",234,Gradient = True , GradientTime= 30)
            self.animation_wait(30)
            self.animation_showText("yes, It's watermelon",234,Gradient = True , GradientTime= 30)
            self.animation_wait(30)

        elif self.name == "error-1":
            self.animation_showText("jlhgkicjuojvyhdr9p iefjof",234,Gradient = True , GradientTime= 30)
            self.animation_wait(30)
            self.animation_showText(" xhjol griuldh ihih S&*P(YP&*SE yp9yrgai)",234,Gradient = True , GradientTime= 30)
            self.animation_wait(30)
            self.animation_showText("I don't know what happend",234,Gradient = True , GradientTime= 30)
            self.animation_wait(30)
            self.animation_showText("as 62g76er5249g24ext5y  ",234,Gradient = True , GradientTime= 30)
            self.animation_wait(30)
            self.animation_showText("a dfi hare oa hafd gpre gh\e",234,Gradient = True , GradientTime= 30)
            self.animation_wait(30)
            self.animation_showText("maybe system have some wrong",234,Gradient = True , GradientTime= 30)
            self.animation_wait(30)
            self.animation_showText("43 tgipraouwjda ;kg j",234,Gradient = True , GradientTime= 30)
            self.animation_wait(30)
            self.animation_showText("Error",234,Gradient = True , GradientTime= 30)
            self.animation_wait(30)
            self.animation_showText("a eto h ue5624dzf 56fg",234,Gradient = True , GradientTime= 30)
            self.animation_wait(30)
            self.animation_showText("errorerrorerrorerrorerrorerror1024AAAsasn",234,Gradient = True , GradientTime= 30)
            self.animation_wait(30)
        elif self.name == "666666":
            self.animation_showText("666666",234,Gradient = True , GradientTime= 30)
            self.animation_wait(30)
            self.animation_showText("I like that",234,Gradient = True , GradientTime= 30)
            self.animation_wait(30)
            self.animation_showText("but I hate old 6",234,Gradient = True , GradientTime= 30)
            self.animation_wait(30)
            self.animation_showText("like my friend Allen(Grass King)",234,Gradient = True , GradientTime= 30)
            self.animation_wait(30)
            self.animation_showText("He had a lot of time get 0 damge in RIVALS",234,Gradient = True , GradientTime= 30)
            self.animation_wait(30)
            self.animation_showText("..............",234,Gradient = True , GradientTime= 30)
            self.animation_wait(30)
            self.animation_showText("I don't know say what",234,Gradient = True , GradientTime= 30)
            self.animation_wait(30)

        elif self.name == "10Htimeplayed":
            self.animation_showText(":)",210,Gradient = True , GradientTime= 30)
            self.animation_wait(50)
            self.animation_showText("You played It's 10 hour now",210,Gradient = True , GradientTime= 30)
            self.animation_wait(50)
            self.animation_showText("How do you feel?",210,Gradient = True , GradientTime= 30)
            self.animation_wait(50)
            self.animation_showText("Did you get all item?",210,Gradient = True , GradientTime= 30)
            self.animation_wait(50)

        elif self.name == "10000roll":
            self.animation_showText("WOW",210,Gradient = True , GradientTime= 30)
            self.animation_wait(50)
            self.animation_showText("You rolled 10000times",210,Gradient = True , GradientTime= 30)
            self.animation_wait(50)

        elif self.name == "3141":
            self.animation_showText("3.141",210,Gradient = True , GradientTime= 30)
            self.animation_wait(50)
            self.animation_showText("It's like pi but not pi",210,Gradient = True , GradientTime= 30)
            self.animation_wait(50)
        
        elif self.name == "314159":
            self.animation_showText("3.14159",210,Gradient = True , GradientTime= 30)
            self.animation_wait(50)
            self.animation_showText("It's closer to pi than 3.141",210,Gradient = True , GradientTime= 30)
            self.animation_wait(50)
            self.animation_showText("But still far away",210,Gradient = True , GradientTime= 30)
            self.animation_wait(50)

        elif self.name == "31415926":
            self.animation_showText("3.1515926",210,Gradient = True , GradientTime= 30)
            self.animation_wait(50)
            self.animation_showText("It's the closest to pi in special items",210,Gradient = True , GradientTime= 30)
            self.animation_wait(50)
            self.animation_showText("But still far away, too",210,Gradient = True , GradientTime= 30)
            self.animation_wait(50)
            self.animation_showText("Because pi have infinite Decimal Places",210,Gradient = True , GradientTime= 30)
            self.animation_wait(50)
            self.animation_showText("Yeah , It's Disrespectful Number",210,Gradient = True , GradientTime= 30)
            self.animation_wait(50)
            self.animation_showText("If you play more I fill you'll find real pi :)",210,Gradient = True , GradientTime= 30)
            self.animation_wait(50)
            self.animation_showText(":P",210,Gradient = True , GradientTime= 30)
            self.animation_wait(50)
            self.animation_showText("good luck",210,Gradient = True , GradientTime= 30)
            self.animation_wait(50)

        elif self.name == "A lot of pi":
            self.animation_showText("oh",10,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("oh wow",50,text_font="./font/Ubuntu/Ubuntu-Light.ttf")

            self.animation_showText("o",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("oh",20,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("oh y",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("oh yo",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("oh you",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("oh you ge",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("oh you get ",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("oh you get a ",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("oh you get a lo",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("oh you get a lot ",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("oh you get a lot of",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("oh you get a lot of p",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("oh you get a lot of pi",50,text_font="./font/Ubuntu/Ubuntu-Light.ttf")

            self.animation_showText("y",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("ye",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("yea",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("yeah",50,text_font="./font/Ubuntu/Ubuntu-Light.ttf")

            self.animation_showText("T",10,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("Th",10,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("Thi",10,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("This",10,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("This n",10,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("This no",10,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("This not",10,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("This not r",10,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("This not rea",10,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("This not real",10,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("This not real p",10,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("This not real pi",80,text_font="./font/Ubuntu/Ubuntu-Light.ttf")

            self.animation_showText("b",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("bu",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("but",20,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("but a",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("but a l",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("but a lo",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("but a lot",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("but a lot :)",120,text_font="./font/Ubuntu/Ubuntu-Light.ttf" , Gradientout= True , GradientTime= 60)

            self.animation_showText("As",10,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("As of",10,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("As of August",10,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("As of August 2021",30,text_font="./font/Ubuntu/Ubuntu-Light.ttf")

            self.animation_showText("a",10,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("a team",10,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("a team of",10,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("a team of Swiss",10,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("a team of Swiss scientists",10,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("a team of Swiss scientists used",10,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("a team of Swiss scientists used a supercomputer",50,text_font="./font/Ubuntu/Ubuntu-Light.ttf")

            self.animation_showText("to calculate",10,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("to calculate the value ",10,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("to calculate the value of pi (π)",10,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("to calculate the value of pi (π) to",50,text_font="./font/Ubuntu/Ubuntu-Light.ttf")

            self.animation_showText("6",50,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("62",20,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("62.8",100,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("62.8 t",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("62.8 tr",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("62.8 tri",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("62.8 tril",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("62.8 trill",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("62.8 trilli",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("62.8 trillio",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("62.8 trillion",50,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("62.8 trillion d",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("62.8 trillion de",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("62.8 trillion dec",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("62.8 trillion deci",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("62.8 trillion decim",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("62.8 trillion decima",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("62.8 trillion decimal",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("62.8 trillion decimal p",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("62.8 trillion decimal pl",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("62.8 trillion decimal pla",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("62.8 trillion decimal plac",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("62.8 trillion decimal place",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("62.8 trillion decimal places",200,text_font="./font/Ubuntu/Ubuntu-Light.ttf")

            self.animation_showText("setting",15,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("setting a",15,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("setting a new ",15,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("setting a new world ",15,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("setting a new world record",15,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("setting a new world record at the time.",200,text_font="./font/Ubuntu/Ubuntu-Light.ttf"  , Gradientout= True , GradientTime= 60)

        elif self.name == "The Real pi":
            self.animation_showText("o",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("oh",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("oh m",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("oh my ",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("oh my g",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("oh my go",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("oh my god",50,text_font="./font/Ubuntu/Ubuntu-Light.ttf")

            self.animation_showText("y",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("yo",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("you",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("you r",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("you re",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("you rea",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("you real",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("you real g",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("you real ge",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("you real get",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("you real get r",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("you real get re",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("you real get rea",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("you real get real",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("you real get real p",50,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("you real get real pi!",50,text_font="./font/Ubuntu/Ubuntu-Light.ttf")

            self.animation_showText("n",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("no",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("now",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("now I",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("now I'l",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("now I'll",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("now I'll s",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("now I'll sh",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("now I'll sho",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("now I'll show",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("now I'll show w",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("now I'll show wh",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("now I'll show wha",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("now I'll show what!",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("now I'll show what i",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("now I'll show what is!",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("now I'll show what is r",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("now I'll show what is re",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("now I'll show what is rea",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("now I'll show what is real",5,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("now I'll show what is real p",50,text_font="./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_showText("now I'll show what is real pi!",50,text_font="./font/Ubuntu/Ubuntu-Light.ttf")

            self.animation_image("./images/animations/The Real pi/1.png" , 300 ,imagefullscreen= True, Gradient= True , GradientTime= 100)
            self.animation_image("./images/animations/The Real pi/2.png" , 300 ,imagefullscreen= True, Gradient= True , GradientTime= 100)
            self.animation_image("./images/animations/The Real pi/3.png" , 300 ,imagefullscreen= True, Gradient= True , GradientTime= 100)
            self.animation_image("./images/animations/The Real pi/4.png" , 300 ,imagefullscreen= True, Gradient= True , GradientTime= 100)
            self.animation_image("./images/animations/The Real pi/5.png" , 300 ,imagefullscreen= True, Gradient= True , GradientTime= 100)
            self.animation_image("./images/animations/The Real pi/6.png" , 300 ,imagefullscreen= True, Gradient= True , GradientTime= 100)
            self.animation_image("./images/animations/The Real pi/7.png" , 300 ,imagefullscreen= True, Gradient= True , GradientTime= 100)
            self.animation_image("./images/animations/The Real pi/8.png" , 300 ,imagefullscreen= True, Gradient= True , GradientTime= 100)
            self.animation_image("./images/animations/The Real pi/9.png" , 300 ,imagefullscreen= True, Gradient= True , GradientTime= 100)
            self.animation_image("./images/animations/The Real pi/10.jpg" , 300 ,imagefullscreen= True, Gradient= True , GradientTime= 100)
            self.animation_image("./images/animations/The Real pi/11.jpg" , 300 ,imagefullscreen= True, Gradient= True , GradientTime= 100)

            self.animation_showText(":)",200,text_font="./font/Ubuntu/Ubuntu-Light.ttf",Gradient= True , GradientTime= 30)
 
            self.animation_type_text("Pi (π) is a mathematical constant" , 50  , "./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_type_text("that represents the ratio of a circle's circumference" , 50  , "./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_type_text("to its diameter." , 50  , "./font/Ubuntu/Ubuntu-Light.ttf")
            self.animation_type_text("It is an irrational number" , 200  , "./font/Ubuntu/Ubuntu-Light.ttf" , 100 , True)

    def animation_type_text(self , text ,endtime, font = "arial", GradientTime:int = 0 ,
                           Gradientout : bool = False):
        t = "" 
        for at in text:
            t += at
            if t != text:
                self.animation_showText(t , 5 , (255,255,255) , font , False , GradientTime , Gradientout )
            else:
                self.animation_showText(t , endtime , (255,255,255) , font , False , GradientTime , Gradientout )

    def animation_showText(self,text:str,time:int ,
                           text_color = (255,255,255),
                           text_font = "arial",
                           Gradient:bool = False ,
                           GradientTime:int = 0 ,
                           Gradientout : bool = False):
        """
        將會在正中間顯示文字
        text: 顯示的文字
        text_color : 文字顏色，預設為白色
        time: 持續時間(tick)
        Gradient: 漸變特效
        GradientTime : 漸變特效持續時間
        """
        if text_font == "arial":
            text_font = pygame.font.match_font("arial")
        textFont = pygame.font.Font(text_font,100)
        textimage = textFont.render(text,True,text_color)
        textRect = textimage.get_rect()
        textRect.center = (SCREENSIZEX//2,SCREENSIZEY//2)
        for t in range(time):
                transparency = 255
                if Gradient:
                    transparency = 255
                    #漸出
                    if t <= GradientTime:
                        transparency = t/GradientTime * 255
                    #中間
                if Gradient:
                    if t >= GradientTime and t < time - GradientTime:
                        transparency = 255
                if Gradient or Gradientout:
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
    
    def animation_image(self,image_path:str , time:int,
                        imagefullscreen:bool = False,
                        Gradient:bool = False ,
                        GradientTime:int = 0 ,
                        Gradientout : bool = False):
        image = pygame.image.load(image_path)
        if imagefullscreen:
            size = image.get_size()
            if size[1] > size[0]:
                a = self.screen.size[1] / size[1]
                image = pygame.transform.smoothscale(image , (size[0] * a ,size[1] * a))
            if size[0] > size[1]:
                a = self.screen.size[0] / size[0]
                image = pygame.transform.smoothscale(image , (size[0] * a ,size[1] * a))

        rect = image.get_rect()
        rect.center = (self.screen.size[0]//2 , self.screen.size[1]//2)
        for t in range(time):
            transparency = 255
            if Gradient:
                #漸出
                if t <= GradientTime:
                    transparency = t/GradientTime * 255
                #中間
            if Gradient:
                if t >= GradientTime and t < time - GradientTime:
                    transparency = 255
            if Gradient or Gradientout:
                # 尾
                if t >= time - GradientTime:
                    _t = t - (time-GradientTime)
                    transparency = 255 - (_t/GradientTime)*255
                #重新加載圖片後再做透明變化
            di = image.copy()
            di.set_alpha(transparency)
            self.screen.screen.fill((0,0,0))
            self.screen.screen.blit(di , rect)
            self.UpdateScreenWhenPlayingAnimation()
    
    def animation_wait(self,time:int):
        """
        在撥動畫時等遺下
        """
        self.screen.screen.fill((0,0,0))
        for _ in range(time): self.UpdateScreenWhenPlayingAnimation()

    def UpdateScreenWhenPlayingAnimation(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.screen.save()
                pygame.quit()
                import sys ; sys.exit()
        
        self.screen.clock.tick(60)
        pygame.display.update()

class playAnimationButton(ImageButton):
    def __init__(self,screen,besideImage,besidex,besidey):
        self.sizex = besidex//2
        self._screen = screen
        super().__init__(besideImage,
                         "./images/button/playAnimation.png",
                         "./images/button/hover_playAnimation.png",
                         (besidex//2,besidey//4*3),
                         60)
        image_originalScale       = self.image.get_size()
        hover_image_originalScale = self.hover_image.get_size()
        image_factor = self.sizex / image_originalScale[0]
        hover_image_factor = self.sizex / hover_image_originalScale[0]
        self.image = pygame.transform.smoothscale(self.image,(self.sizex,image_originalScale[1] * image_factor))
        self.hover_image = pygame.transform.smoothscale(self.hover_image,(self.sizex,hover_image_originalScale[1] * hover_image_factor))

        self.rect = self.image.get_rect()
        self.rect.centerx = besidex//2
        self.rect.centery = besidey//4*3