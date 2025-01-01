import pygame
from config import *

class item:
    def __init__(self,name:str , rarity: int ,image_path: str, item_type: str,screen):
        """
        name: 物品名稱
        rarity : 該物品的稀有度
        image_path : 該物品的圖案路徑
        item_type : 物品型態，分為"normal item" 以及 "special item"
        screen : 繪製的視窗
        """
        self.name = name
        self.rarity = rarity
        self.image_path = image_path
        self.item_type = item_type
        self.screen = screen

        # 創建圖片
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image.set_colorkey((0,0,0))# 去背
        self.rect = self.image.get_rect()
        self.rect.center = (SCREENSIZEX//2,SCREENSIZEY//2) #一律放在螢幕中間

    def draw(self):
        self.screen.screen.blit(self.image,self.rect)

class common(item):
    def __init__(self,screen):
        super().__init__("common",2,"./images/items/common.png","",screen)

class uncommon(item):
    def __init__(self,screen):
        super().__init__("uncommon",4,"./images/items/uncommon.png","",screen)

class rock(item):
    def __init__(self,screen):
        super().__init__("rock",12,"./images/items/rock.png","",screen)