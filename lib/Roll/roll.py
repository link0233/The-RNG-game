import pygame
import random

from lib.Roll.rollbutton import *
from lib.Roll.autoRollButton import  *
from lib.functions.RateLimitedFunction import *
from lib.functions.functions import format_to_two_decimal_places

class roll:
    def __init__(self):
        self.rollList = []
        self.rollCounts = [0,0,0,0,0]
        self.luckboost = 1
        for i in range(len(self.rollCounts)):#隨機起始值
            self.rollCounts[i] = random.randint(0,1023)

        self.create_rollList()

    def create_rollList(self):
        for i in range(512):
            self.rollList.append(2)
        for i in range(256):
            self.rollList.append(4)
        for i in range(128):
            self.rollList.append(8)
        for i in range(64):
            self.rollList.append(16)
        for i in range(32):
            self.rollList.append(32)
        for i in range(16):
            self.rollList.append(64)
        for i in range(8):
            self.rollList.append(128)
        for i in range(4):
            self.rollList.append(256)
        for i in range(2):
            self.rollList.append(512)
        self.rollList.append(1024)
        self.rollList.append(2048)
        #打亂
        for i in range(2000):
            a = random.randint(0,1023)
            b = random.randint(0,1023)
            c = self.rollList[a]
            d = self.rollList[b]
            self.rollList[a] = d
            self.rollList[b] = c

    def roll(self):
        rolled : int = 1
        # 演算法: 先抽，洛維2048則在抽一次，可以倍增機率，最高可達2^50(約1000^5)
        for i in range(5):
            if self.rollCounts[i] >= 1023:
                self.rollCounts[i] = 0
            else: 
                self.rollCounts[i] += 1

            get = self.rollList[self.rollCounts[i]]#抽

            #if i !=0:print([get,i,rolled])
            rolled *= (1024^i)*get//1024
            rolled = rolled //2
            if get != 2048:
                break
        rolled *= 2 * self.luckboost
        return rolled

class rollUI:
    def __init__(self,screen):
        self.screen = screen

        arial = pygame.font.match_font('arial')
        FONT = pygame.font.Font( arial,36)
        self.no_show_image = FONT.render(f"click roll to roll", True, (0,0,0))
        self.show_image = None
        self.timeToRun_surface = FONT.render("0s", True, (0,0,0))

        self.rollDelay = 3 #等待3秒抽一次

        # self.items = {
        #     "common"      : 2,         v
        #     # "uncommon"    : 4,       v
        #     # "one6"        : 6,
        #     # "rare"        : 8,
        #     # "rock"        : 12,      v
        #     # "miku"        : 39,
        #     # "veryRare"    : 50,
        #     # "epic"        : 100,
        #       "gold"        : 200,
        #     # "pi-1"        : 314,
        #     # "1K"          : 1000,
        #     # "mikumiku"    : 3939,
        #     # "pi-2"        : 31415,
        #     # "mikumikumiku": 393939,
        #     # "666666"      : 666666,
        #     # "lengerdary"  : 100000,
        #     # "drogun"      : 375000,
        #     # "pi-3"        : 3141592,
        #     # "The Void"    : 99999999
        # }
        
        self.roll :roll  = roll()
        self.rollbutton : rollbutton = rollbutton(self.screen)
        self.autoRollButton : autoRollButton = autoRollButton(self.screen)
        self.RollTimeRate : RateLimitedFunction = RateLimitedFunction(self.rollDelay,self.rollbutton.ifRoll)

    def draw(self):
        #繪製按鈕
        self.rollbutton.draw(self.screen.screen)
        self.autoRollButton.draw(self.screen.screen)

        #繪製抽到的東西
        if self.show_image == None :
            self.rect = self.no_show_image.get_rect()
            self.screen.screen.blit(self.no_show_image, (
                (-self.rect.width + SCREENSIZEX)//2,
                SCREENSIZEY//2
            ))
        else:
            self.screen.inventory.item_list[self.show_image].draw()

        self.screen.screen.blit(self.timeToRun_surface,self.timeToRun_Rect)

    def update(self):
        #更興按鈕狀態
        self.rollbutton.update()
        self.autoRollButton.update()

        #更興剩餘時間狀態
        self.timeToRun_surface = FONT.render(format_to_two_decimal_places(self.RollTimeRate.get_timeToRun()) + "s", True, (0,0,0))
        self.timeToRun_Rect = self.timeToRun_surface.get_rect()
        self.timeToRun_Rect.center = (self.rollbutton.rect.centerx,self.rollbutton.rect.centery - SCREENSIZEY//20) #至於抽取按鈕下方
 
        self.RollTimeRate.execute(self.Roll)       #抽
        
    def Roll(self):
        #確定抽到的物品
        get = self.roll.roll()
        rollitemlist = []
        bestitem = "common"
        for item in self.screen.inventory.item_list:
            itemluck = self.screen.inventory.item_list[item].rarity
            if get>itemluck:
                bestitem = item
            if itemluck> get//2 and itemluck<=get:
                rollitemlist.append(item)

        print((rollitemlist,get))

        if rollitemlist == []:
            itemget = self.screen.inventory.item_list[bestitem].name
            print(True)
        else:
            itemget = self.screen.inventory.item_list[   rollitemlist[random.randint(0,len(rollitemlist)-1)]   ].name

        # 加入得到的物品至清單中
        if itemget in self.screen.inventory.itemData["item"]:
            self.screen.inventory.itemData["item"][itemget] += 1
        else:
            self.screen.inventory.itemData["item"][itemget] = 1

        self.show_image = itemget
        print(itemget)
        #self.text_surface = FONT.render(f"You get:{itemget.name} ", True, (0,0,0))