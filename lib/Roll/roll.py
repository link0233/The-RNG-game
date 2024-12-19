import pygame
import random

from lib.Roll.rollbutton import *

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
        self.text_surface = FONT.render(f"click roll to roll", True, (0,0,0))

        self.items = {
            "common" : 2,
            "uncommon": 3,
            "rare"    : 4,
            "veryRare": 10,
            "epic"    : 100,
            "1K"      : 1000
        }
        

        self.roll :roll  = roll()
        self.rollbutton : rollbutton = rollbutton(self.screen)

    def draw(self):
        self.rollbutton.draw(self.screen.screen)
        self.rect = self.text_surface.get_rect()
        self.screen.screen.blit(self.text_surface, (
            (-self.rect.width + SCREENSIZEX)//2,
            SCREENSIZEY//2
        ))

    def update(self):
        ifRoll = self.rollbutton.handle_event(self.screen.event)
        if ifRoll:        #確定抽到的物品
            get = self.roll.roll()
            rollitemlist = []
            bestitem = "common"
            for item in self.items:
                itemluck = self.items[item]
                if get>itemluck:
                    bestitem = item
                if itemluck> get//2 and itemluck<=get:
                    rollitemlist.append(item)

                print((rollitemlist,get))

            if rollitemlist == []:
                itemget = bestitem
            else:
                itemget = rollitemlist[random.randint(0,len(rollitemlist)-1)]

            self.text_surface = FONT.render(f"You get:{itemget} ", True, (0,0,0))