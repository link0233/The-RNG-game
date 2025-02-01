import pygame
from config import *

class part:
    def __init__(self,name : str, pos : int ,screen ):
        self.screen = screen
        self.name = name
        self.posx = pos % 4
        self.posy = pos

        pygame.font.init()
        self.arial = pygame.font.match_font("arial")

        # 建立基本圖像
        self.size = (SCREENSIZEX//4 - 50,300)
        self.name_image_size = (self.size[0] - 50 , (self.size[1] - 50) // 2)
        self.ProgressBar_image_size = (self.size[0] - 50 , (self.size[1] - 50) // 4)
        self.boost_image_size = (self.size[0] - 50 , (self.size[1] - 50) // 4)

        #image
        self.image = pygame.Surface(self.size)
        self.image.set_colorkey((0,0,0))

        self.bg_image = pygame.Surface(self.size)
        pygame.draw.rect(self.bg_image,(255,255,255),(0,0,self.size[0],self.size[1]),border_radius= 20)
        pygame.draw.rect(self.bg_image,(108, 227, 4),(5,5,self.size[0]-10,self.size[1]-10),border_radius= 20)

        self.namefont = pygame.font.Font(self.arial,self.name_image_size[1] - 15)
        self.name_image = self.namefont.render(self.name,True,(255,255,255))
        
        self.ProgressBar_font = pygame.font.Font(self.arial,self.ProgressBar_image_size[1] - 30)
        self.boost_font = pygame.font.Font(self.arial,self.boost_image_size[1] - 20)

        self.ProgressBar_image = pygame.Surface(self.ProgressBar_image_size)
        self.ProgressBar_image.set_colorkey((0,0,0))
        self.boost_image : pygame.Surface = pygame.Surface(self.boost_image_size)

        #rect and positions
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREENSIZEX //8 * (self.posx*2 +1)
        self.rect.centery = 0
        # pos = (x,y)
        self.name_pos = (25,25)
        self.ProgressBar_pos = (25,self.name_image_size[1] + 25)
        self.boost_pos = (25 , self.ProgressBar_pos[1] + self.ProgressBar_image_size[1])

    def update_image(self):
        data = self.screen.Achievement.achievementData[self.name]
        state = data["now_state"]
        value = data["now_value"]
        boost = data["boost"]
        p_text = ""
        
        if data["nextlevelreq_value"] == 0:
            a = 1
        elif data["nextlevelreq"] == "max":
            a = 1
            p_text = data["nextlevelreq"]
        else: 
            a = value / data["nextlevelreq_value"]
            p_text = f"{state} / {data["nextlevelreq"]}"
        pygame.draw.rect(self.ProgressBar_image,(51, 101, 7),(30,10,self.ProgressBar_image_size[0] - 60 , self.ProgressBar_image_size[1] -20),border_radius= self.ProgressBar_image_size[1]//2 - 10)
        pygame.draw.rect(self.ProgressBar_image,(74, 207, 255),(30,10,(self.ProgressBar_image_size[0] - 60) * a , self.ProgressBar_image_size[1] -20),border_radius= self.ProgressBar_image_size[1]//2 - 10)
        pt_image = self.ProgressBar_font.render(p_text,True,(0,0,1))
        rect = pt_image.get_rect()
        rect.center = (self.ProgressBar_image_size[0]//2,self.ProgressBar_image_size[1]//2)
        self.ProgressBar_image.blit(pt_image,rect)

        self.boost_image = self.boost_font.render(boost,True,(3, 0, 207))

    def draw(self , move : int):
        self.update_image()
        #reset
        self.image = pygame.Surface(self.size)
        self.image.set_colorkey((0,0,0))    
        # bg
        self.image.blit(self.bg_image,(0,0))
        # name
        self.image.blit(self.name_image,(self.name_pos[0] , self.name_pos[1],self.name_image_size[0],self.name_image_size[1]))
        #progressbar
        self.image.blit(self.ProgressBar_image,(self.ProgressBar_pos[0],self.ProgressBar_pos[1] , self.ProgressBar_image_size[0], self.ProgressBar_image_size[1]))
        #boost
        self.image.blit(self.boost_image,(self.boost_pos[0],self.boost_pos[1] , self.boost_image_size[0], self.boost_image_size[1]) )

        # draw on screen
        self.rect.y = (self.size[1] + 80) * (self.posy - self.posy %4) // 4 + move
        self.screen.screen.blit(self.image,self.rect)
