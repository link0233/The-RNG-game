from config import *
import math

from lib.functions.RateLimitedFunction import RateLimitedFunction
from lib.functions.functions import returnTrue
from lib.functions.bigNumber import BigNumber

class point:
    def __init__(self,screen):
        # self.point:float = 0
        # self.point_exp:int = 0
        # self.point_boost:float = 1
        # self.point_boost_exp:int = 0
        self.point = BigNumber(0)
        self.point_boost = BigNumber(1)
        self.screen = screen

        self.point_gen_timer = RateLimitedFunction(1,returnTrue)

    def update(self):
        self.point_gen_timer.execute(self.add_a_point)

        #debug
        #self.point_exp = int(self.point_exp)

        self.point_boost = BigNumber(1)
        # self.point_boost_exp  = 0

        self.point_boost *= self.screen.upgrade.point_boost
        # self.point_boost_exp += self.screen.upgrade.point_exp_boost
        
    def add_a_point(self):
        #print(self.point)
        #print(self.point_boost)
        self.point = self.point + self.point_boost
        #print( (self.point * (10 ** self.point_exp) , self.point_exp))

    # def add_point(self,base = 1 , exp = 0):
    #     a = self.point_exp - self.point_boost_exp - exp
        
    #     # 比較小
    #     if a > 0:
    #         self.point += base * (10 ** -a) * self.point_boost
        
    #     if a == 0:
    #         self.point += base * self.point_boost

    #     if a < 0 :
    #         # 先將原本的指數往上拉至相同的
    #         self.point *= 10 ** a
    #         self.point_exp = self.point_boost_exp + exp

    #         self.point += base * self.point_boost

    #     #print((self.point,self.point_exp))
    #     b = int(math.log10(self.point))
    #     self.point /= 10 ** b
    #     self.point_exp += b

    # def add_point_noboost(self,base = 1 , exp = 0):
    #     a = self.point_exp - exp
    #     #print((a,base / (10 ** a)))
        
    #     # 比較小
    #     if a > 0:
    #         self.point += base / (10 ** a) 
        
    #     if a == 0:
    #         self.point += base 

    #     if a < 0 :
    #         # 先將原本的指數往上拉至相同的
    #         self.point *= 10 ** a
    #         self.point_exp = exp

    #         self.point += base

    #     #print((self.point,self.point_exp))
    #     b = int(math.log10(self.point))
    #     self.point /= 10 ** b
    #     self.point_exp += b

    # def size(self,number:float,exp:int= 0) -> int:
    #     """
    #     比較大小
    #     回傳:
    #     1: 大
    #     2: 依樣
    #     3: 小
    #     """
    #     try:
    #         a = int(math.log10(number))
    #     except:
    #         a = 0
    #     exp += a
    #     number /= 10 ** a

    #     try:
    #         b = int(math.log10(self.point))
    #     except:
    #         b = 0
    #     self.point /= 10 ** b
    #     self.point_exp += b

    #     #print((self.point,self.point_boost_exp))

    #     if exp > self.point_exp :
    #         return 1
    #     if exp < self.point_exp:
    #         return 3

    #     if exp == self.point_exp:
    #         if self.point == number:
    #             return 2
    #         if number> self.point:
    #             return 1
    #         if number < self.point :
    #             return 3
