from config import *
import math

from lib.functions.RateLimitedFunction import RateLimitedFunction
from lib.functions.functions import returnTrue

class point:
    def __init__(self,screen):
        self.point:float = 0
        self.point_index:int = 0
        self.point_boost:float = 1
        self.point_boost_index:int = 0
        self.screen = screen

        self.point_gen_timer = RateLimitedFunction(1,returnTrue)

    def update(self):
        self.point_gen_timer.execute(self.add_point)

        #debug
        self.point_index = int(self.point_index)

        self.point_boost = 1
        self.point_boost_index  = 0

        self.point_boost *= self.screen.upgrade.point_boost
        self.point_boost_index += self.screen.upgrade.point_index_boost

        print( (self.point * (10 ** self.point_index) , self.point_index))

    def add_point(self,base = 1 , index = 0):
        a = self.point_index - self.point_boost_index - index
        
        # 比較小
        if a > 0:
            self.point += base * (10 ** -a) * self.point_boost
        
        if a == 0:
            self.point += base * self.point_boost

        if a < 0 :
            # 先將原本的指數往上拉至相同的
            self.point *= 10 ** a
            self.point_index = self.point_boost_index + index

            self.point += base * self.point_boost

        #print((self.point,self.point_index))
        b = int(math.log10(self.point))
        self.point /= 10 ** b
        self.point_index += b

    def add_point_noboost(self,base = 1 , index = 0):
        a = self.point_index - index
        #print((a,base / (10 ** a)))
        
        # 比較小
        if a > 0:
            self.point += base / (10 ** a) 
        
        if a == 0:
            self.point += base 

        if a < 0 :
            # 先將原本的指數往上拉至相同的
            self.point *= 10 ** a
            self.point_index = index

            self.point += base

        #print((self.point,self.point_index))
        b = int(math.log10(self.point))
        self.point /= 10 ** b
        self.point_index += b

    def size(self,number:float,index:int= 0) -> int:
        """
        比較大小
        回傳:
        1: 大
        2: 依樣
        3: 小
        """
        try:
            a = int(math.log10(number))
        except:
            a = 0
        index += a
        number /= 10 ** a

        try:
            b = int(math.log10(self.point))
        except:
            b = 0
        self.point /= 10 ** b
        self.point_index += b

        #print((self.point,self.point_boost_index))

        if index > self.point_index :
            return 1
        if index < self.point_index:
            return 3

        if index == self.point_index:
            if self.point == number:
                return 2
            if number> self.point:
                return 1
            if number < self.point :
                return 3
