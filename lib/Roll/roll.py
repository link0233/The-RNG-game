import pygame
import random
import math

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
        self.testLuckboost = 1

        self.rollDelay :float = 3 #等待3秒抽一次
        self.baseLuckBoost = 1

        # self.items = {
        #     "common"      : 2,         v
        #     # "uncommon"    : 4,       v
        #     # "one6"        : 6,
        #     # "rare"        : 8,       v
        #     # "rock"        : 12,      v
        #     # "miku"        : 39,
        #     # "veryRare"    : 50,      v
        #     # "epic"        : 100,     v
        #       "gold"        : 200,
        #     # "pi-1"        : 314,
        #     # "1K"          : 1000,
            #   "line"        : 1500,    v
        #     # "mikumiku"    : 3939,
        #     # "pi-2"        : 31415,
        #     # "mikumikumiku": 393939,
        #     # "666666"      : 666666,  v
        #     # "lengerdary"  : 100000,  v
        #     # "drogun"      : 375000,
        #     # "pi-3"        : 3141592,
        #     # "The Void"    : 99999999
        # }
        
        self.roll :roll  = roll()
        self.rollbutton : rollbutton = rollbutton(self.screen)
        self.autoRollButton : autoRollButton = autoRollButton(self.screen)
        self.RollTimeRate : RateLimitedFunction = RateLimitedFunction(self.rollDelay,self.rollbutton.ifRoll)
        self.rollAnimation: rollAnimation = rollAnimation(self.screen)

    def draw(self):
        #繪製按鈕
        if self.screen.scene == 0:
            self.rollbutton.draw(self.screen.screen)
            self.autoRollButton.draw(self.screen.screen)
            self.rollAnimation.draw()

            #沒播放動畫時繪製抽到的東西
            if self.rollAnimation.playing == False:
                if self.show_image == None :
                    self.rect = self.no_show_image.get_rect()
                    self.screen.screen.blit(self.no_show_image, (
                        (-self.rect.width + SCREENSIZEX)//2,
                        SCREENSIZEY//2
                    ))
                else:
                    self.screen.inventory.item_list[self.show_image].draw_rolled()

            self.screen.screen.blit(self.timeToRun_surface,self.timeToRun_Rect)

    def update(self):
        # 處理所有的加成
        self.baseLuckBoost = 1
        self.baseLuckBoost *= self.screen.Achievement.totalLuckBoost
        self.baseLuckBoost *= self.screen.upgrade.luckboost
        self.roll.luckboost = self.baseLuckBoost * self.screen.setting.ChangeLuckBoost.downLuck * self.testLuckboost

        self.RollTimeRate.interval = self.rollDelay
        self.RollTimeRate.interval -= self.screen.Achievement.totalTimeReduce
        self.rollAnimation.update()
        #在主畫面時更興按鈕狀態
        if self.screen.scene == 0:
            self.rollbutton.update()
            self.autoRollButton.update()

        #更興剩餘時間狀態
        self.timeToRun_surface = FONT.render(format_to_two_decimal_places(self.RollTimeRate.get_timeToRun()) + "s", True, (0,0,0))
        self.timeToRun_Rect = self.timeToRun_surface.get_rect()
        self.timeToRun_Rect.center = (self.rollbutton.rect.centerx,self.rollbutton.rect.centery - SCREENSIZEY//20) #至於抽取按鈕下方
 
        self.RollTimeRate.execute(self.Roll)       #抽
        
    def Roll(self):
        # 先確認是否有extra item可獲的，如可獲得，則直接獲得
        getExtra = self.screen.inventory.checkExtraGet()
        print(getExtra)
        if getExtra != None:
            self.show_image = getExtra
            self.rollAnimation.playAnimation(getExtra,self.RollTimeRate.interval)
            self.screen.inventory.inventoryData["extraItem"][getExtra] = 1
            # self.screen.inventory.item_list[  getExtra ] . play_animation()
            # self.RollTimeRate.reset()
            return
        #確定抽到的物品
        self.screen.states.states["rolls"] += 1
        get = self.roll.roll()
        self.screen.inventory.addCash(get)
        rollitemlist = []
        bestitem = "common"
        for item in self.screen.inventory.item_list:
            itemluck = self.screen.inventory.item_list[item].rarity
            canRoll = self.screen.inventory.item_list[item].checkCanRoll()
            if get>itemluck and canRoll:
                bestitem = item
            if itemluck> get//2 and itemluck<=get and canRoll:
                rollitemlist.append(item)

        print((rollitemlist,get))

        if rollitemlist == []:
            itemget = self.screen.inventory.item_list[bestitem].name
            #print(True)
        else:
            itemget = self.screen.inventory.item_list[   rollitemlist[random.randint(0,len(rollitemlist)-1)]   ].name
        getItemType = self.screen.inventory.item_list[  itemget ].item_type

        # 加入得到的物品至清單中
        if itemget in self.screen.inventory.inventoryData[getItemType]:
            self.screen.inventory.inventoryData[getItemType][itemget] += self.screen.inventory.item_list[  itemget ].get_boost()
        else:
            self.screen.inventory.inventoryData[getItemType][itemget] = self.screen.inventory.item_list[  itemget ].get_boost()

        self.show_image = itemget
        # 資源取得
        self.screen.states.experience.xp += get
        #確定之後撥放動畫
        print(itemget)
        self.rollAnimation.playAnimation(itemget,self.RollTimeRate.interval)
        # self.screen.inventory.item_list[  itemget ] . play_animation()
        # self.RollTimeRate.reset()
        #self.text_surface = FONT.render(f"You get:{itemget.name} ", True, (0,0,0))

class rollAnimation:
    def __init__(self,screen):
        self.screen = screen
        self.roll :roll = roll()
        #self.item_list = self.screen.inventory.item_list

        self.playing = False
        self.start_play_time = 0
        self.rolled : str = None
        #切換圖片
        self.start_time_to_next_image  = 0.1
        self.last_change = 0
        self.time_to_next_image = 0.05
        self.time_to_next_image_plus = 0.025
        #圖片進場特效(由上往下)
        self.down_Duration = self.time_to_next_image/2
        self.down_distance = 30
        self.down_movey = 0
        self.AnimationPlayTime = 2
        self.show_currect_time = 0

        self.showing_image = None

    def playAnimation(self,rolled,rollSpeed):
        self.playing = True
        self.start_play_time = time.time()
        self.start_time_to_next_image = rollSpeed/50
        self.time_to_next_image_plus = rollSpeed/100
        self.time_to_next_image = self.start_time_to_next_image
        self.down_Duration = self.time_to_next_image/2
        self.rolled = rolled
        self.item_list = self.screen.inventory.item_list
        self.last_change = 0
        self.show_currect_time = rollSpeed/3
        self.change_image()

    def change_image(self):
        if self.last_change + self.time_to_next_image + self.show_currect_time>= self.AnimationPlayTime:
            self.showing_image = self.rolled
        else:
            self.roll.luckboost = self.screen.roll.roll.luckboost ** 0.8
            get = self.showing_image #先設定成相同才會改成正確的
            while get == self.showing_image:
                luck = self.roll.roll()
                cangets = []
                best = ["common",2]
                for item in self.item_list:
                    rarity = self.item_list[item].rarity
                    if rarity<luck and rarity>luck//2:
                        cangets.append(item)
                    elif rarity > best[1] and rarity <=luck:
                        best = [item,rarity]
                if cangets == []:
                    get= best[0]
                else:
                    get = cangets[random.randint(0,len(cangets) - 1)]
            self.showing_image = get
        self.down_movey = self.down_distance

    def update(self):
        if self.playing:
            now = time.time()
            t = now - self.start_play_time
            
            if t - self.last_change >= self.time_to_next_image:
                self.time_to_next_image += self.time_to_next_image_plus
                self.last_change = t
                self.change_image()
            
            if t >= self.AnimationPlayTime:
                self.playing = False
                self.showing_image = None
                self.screen.roll.RollTimeRate.stop()
                self.item_list[self.screen.roll.show_image].play_animation()
                self.screen.roll.RollTimeRate.restart()

            self.down_movey = -(1.5 ** (-((t - self.last_change)/self.down_Duration)))*self.down_distance

    def draw(self):
        if self.playing:
            self.item_list[self.showing_image].draw_rolled(movey = self.down_movey)
