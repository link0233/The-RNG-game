import pygame
from config import *

class item:
    def __init__(self,name:str , rarity: int ,rarity_count: int,image_path: str, item_type: str,screen):
        """
        name: 物品名稱
        rarity : 該物品的稀有度
        rarity_count : 該物品稀有度排名
        image_path : 該物品的圖案路徑
        item_type : 物品型態，分為"normal item" 以及 "special item"
        screen : 繪製的視窗
        """
        self.name = name
        self.rarity = rarity
        self.rarity_count = rarity_count
        self.rolled_image_path = image_path
        self.item_type = item_type
        self.screen = screen

        pygame.font.init()
        self.font = pygame.font.Font(None,50)

        # 創建圖片
        self.rolled_image = pygame.image.load(image_path).convert_alpha()
        self.rolled_image.set_colorkey((0,0,0))# 去背
        self.rolled_rect        = self.rolled_image.get_rect()
        self.rolled_rect.center = (SCREENSIZEX//2,SCREENSIZEY//2) #一律放在螢幕中間


        #顯示在物品欄中的
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
        self.rarity_rect           = (self.item_name_image_w + self.rarity_image_w//2 ,self.item_image_h//2)

        
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
        self.screen.screen.blit(self.item_image,self.item_rect)
        

