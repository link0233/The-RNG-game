import pygame
import random
import time
import math

from lib.functions.functions import draw_hollow_circle

class buypart_animation:
    def __init__(self ,type):
        """
        type: 類型
        創建後直接撥放，放完則設置為 None
        """
        self.type = type
        self.end = False

        if self.type == "cash" or self.type =="luck" or self.type =="xp" or self.type =="point":
            self.circle_r_plus = 300
            self.line_grow_speed = 0.02
            self.circle_grow_speed = 0.2
            self.line_movespeed = 380
            self.line_length = 80
            self.transparency = 255

            self.circle_created = 0
            self.line_created = 0
            self.circle_create_max = 3
            self.line_created_max = 100

            self.start_time = time.time()
            self.t = self.start_time

            self.circles = []
            self.lines = []
            # circle : [r,border_w,t]
            # line :   [angle,r,t]

            if self.type == "cash":
                self.color = (55, 210, 79)
            if self.type == "luck":
                self.color = (28, 161, 48)
            if self.type == "xp":
                self.color = (28, 119, 161)
            if self.type == "point":
                self.color = (255,255,255)

    def update(self):
        dt = time.time() - self.start_time - self.t
        self.t = time.time() - self.start_time
        # update
        for i in range(len(self.lines)):
            self.lines[i][1] += dt *self.line_movespeed
            self.lines[i][2] -= dt *180
            if self.lines[i][2]<= 0:
                self.lines[i][2]  = 0

        for i in range(len(self.circles)):
            self.circles[i][0] += dt *self.circle_r_plus
            self.circles[i][1] -= 0.01
            self.circles[i][2] -= dt *180
            if self.circles[i][1] < 1 or self.circles[i][2]<=0 :
                self.circles[i][2] = 0
                self.circles[i][1] = 1

        # 超過4秒直接算結束
        if self.t >= 4:
            self.end = True

        # create
        lines = int(self.t/self.line_grow_speed)
        circles = int(self.t/self.circle_grow_speed)

        if lines>self.line_created and self.line_created < self.line_created_max:
            for _ in range(-self.line_created + lines):
                self.lines .append([random.randint(0,359),0,255])
                self.line_created += 1 
        if circles>self.circle_created and self.circle_created<self.circle_create_max:
            for _ in range(-self.circle_created + circles):
                self.circles .append([0,10,255])
                self.circle_created +=1

        # 確定結束
        # 最後一個變為透明
        if self.circles != [] and self.lines !=[]:
            if self.circles[-1][2] <= 0 and self.lines[-1][2] <= 0:
                self.end = True

        #print(int(self.t/self.line_grow_speed))
        
    def draw(self , screen , center):
        line_surface = pygame.Surface(screen.get_size(),pygame.SRCALPHA)
        line_s_size = line_surface.get_size()
        line_center = (line_s_size[0]//2,line_s_size[1]//2)
        for line in self.lines:
            pygame.draw.line(line_surface,(self.color[0],self.color[1],self.color[2],line[2]),(line[1] * math.cos(line[0]) + line_center[0] , line[1] * math.sin(line[0]) + line_center[1]) ,((line[1] + self.line_length)  * math.cos(line[0])  + line_center[0], (line[1] + self.line_length)  * math.sin(line[0]) + line_center[1]))
        rect = line_surface.get_rect()
        rect.center = center
        screen.blit(line_surface,rect)
        for circle in self.circles:
            draw_hollow_circle(screen,center,circle[0],int(circle[1]),self.color,circle[2])

