import pygame
import random
import time
import math

from lib.functions.functions import draw_hollow_circle
#from functions import draw_hollow_circle

class buypart_animation:
    def __init__(self ,type):
        """
        type: 類型
        創建後直接撥放，放完則設置為 None
        """
        self.type = type
        self.end = False
        self.start_time = time.time()
        self.t = self.start_time

        if self.type == "cash" or self.type =="luck" or self.type =="xp" or self.type =="point":
            self.circle_r_plus = 600
            self.line_grow_speed = 0.01
            self.circle_grow_speed = 0.15
            self.line_movespeed = 1600
            self.line_length = 100
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

        if self.type == "F":
            self.move_speed = 1000
            self.rotate_speed = 100
            self.grow_speed = 0.05
            self.create_max = 10
            self.create_per_time = 20
            self.square_width = 15
            self.square_color = (119, 255, 144)
            self.square_created = 0

                        # [distance , angle , rotate , t]
            self.squares = []
            self.square_image = pygame.Surface((self.square_width , self.square_width) , pygame.SRCALPHA)
            self.square_image.fill((119, 255, 144))

            # i = pygame.Surface((self.square_width,self.square_width) , pygame.SRCALPHA)
            # i.fill((self.square_color[0],self.square_color[1],self.square_color[2],data[3]))

    def update(self):
        dt = time.time() - self.start_time - self.t
        self.t = time.time() - self.start_time
        # update
        if self.type == "cash" or self.type =="luck" or self.type =="xp" or self.type =="point":
            for i in range(len(self.lines)):
                self.lines[i][1] += dt *self.line_movespeed
                self.lines[i][2] -= dt *360
                if self.lines[i][2]<= 0:
                    self.lines[i][2]  = 0

            for i in range(len(self.circles)):
                self.circles[i][0] += dt *self.circle_r_plus
                self.circles[i][1] -= 0.01
                self.circles[i][2] -= dt *360
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

        if self.type == "F":
            # update
            for n in range(len(self.squares)):
                self.squares[n][0] += self.move_speed*dt
                self.squares[n][2] += self.rotate_speed * dt
                self.squares[n][2] += -10 * dt

            # create
            can_create = int(self.t/self.grow_speed)
            if can_create > self.create_max : can_create = self.create_max

            if can_create > self.square_created and self.square_created < self.create_max:
                for _ in range(can_create - self.square_created):
                    for __ in range(self.create_per_time):
                        self.squares.append([0 , random.randint(0,360) , random.randint(0,90) , 255])

                    self.square_created += 1

            if self.t >= 4:
                self.end = True

    def draw(self , screen:pygame.Surface , center):
        if self.type == "cash" or self.type =="luck" or self.type =="xp" or self.type =="point":
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

        if self.type == "F":
            
            for data in self.squares:
                self.square_image.fill((self.square_color[0],self.square_color[1],self.square_color[2],data[3]))
                image = pygame.transform.rotate(self.square_image , data[2])
                rect = image.get_rect()
                rect.center = (data[0] * math.cos(data[1]) + center[0], data[0] * math.sin(data[1]) + center[1])
                
                screen.blit(image , rect)

# pygame.init()
# _screen = pygame.display.set_mode((640,480))
# t = buypart_animation("F")

# while True:
#     t.update()

#     _screen.fill((255,255,255))
    
#     t.draw(_screen,(320,240))

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             import sys;sys.exit()

#     pygame.display.update()


