import pygame
from config import *

from lib.GUI.imageButton import *
from lib.functions.functions import draw_text

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
        self.boost = 1
        self.Achievement_boost = 1

        pygame.font.init()
        CourierNew = pygame.font.match_font("Tahoma")
        self.font = pygame.font.Font(CourierNew,40)

        # 創建提示內容
        if   self.name == "100roll" : self.caption = "You roll 100 times !!!!!!!!!"
        elif self.name == "10000roll" : self.caption = "You roll 10000 times !!!!!!!!!"
        elif self.name == "10Htimeplayed" : self.caption = "You played 10H in this game!!"

        # 創建圖片
        self.rolled_image = pygame.image.load(image_path).convert_alpha()
        self.rolled_image.set_colorkey((0,0,0))# 去背
        self.rolled_rect        = self.rolled_image.get_rect()
        self.rolled_rect.center = (SCREENSIZEX//2,SCREENSIZEY//2) #一律放在螢幕中間


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
            self.item_rect.y           = rarity_count * self.item_image_h
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
            else :return False
        return False

    def get_boost(self):
        return self.Achievement_boost * self.screen.setting.ChangeLuckBoost.ItemGetBoost

    def draw_rolled(self,movex = 0,movey = 0):
        show_rect = self.rolled_image.get_rect()
        show_rect.x = self.rolled_rect.x + movex
        show_rect.y = self.rolled_rect.y + movey
        self.screen.screen.blit(self.rolled_image,show_rect)

    def draw_itemList(self,count:int ,get:bool ,move:int ):
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
                count_image = self.font.render(f"{count:.0f}",True,(0,0,0))
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