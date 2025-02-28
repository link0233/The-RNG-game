import pygame

class label:
    def __init__(self , text : str,
                        rect ,
                        text_color = (255,255,255),
                        text_size : int = -1,
                        text_font : str = "arial",
                        antialiab : bool = True,
                        background  : bool = False,
                        background_color = (0,0,0),
                        background_border_radius :int = -1
                        ):
        """
        此為一個標籤，上面有文字
        :param text: 要繪製的文字
        :param rect: 位置(x,y,w,h)
        :param text_color: 字的顏色，預設為白色
        :param text_size: 字的大小，預設會根據大小調整
        :param text_font: 字體，預設為arial
        :param antialiab: 是否啟用抗拒尺
        :param background: 是否啟用背景，預設為否
        :param background_color: 背景顏色，預設為黑
        :param background_border_radius: 是否啟用背景邊角元化，預設為-1 (不啟用)
        """
        # 基本資料
        self.text = text
        self.rect = rect
        self.text_color = text_color
        self.text_size = text_size
        self.font = text_font
        self.antialiab = antialiab
        self.background = background
        self.bg_color = background_color
        self.bg_b_r = background_border_radius

        # 先處裡字體
        pygame.font.init()
        if self.font == "arial":
            self.font = pygame.font.match_font(self.font)

        if self.text_size == -1 :
            self.text_font = pygame.font.Font(self.font,self.rect[3] - 10)
        else:
            self.text_font = pygame.font.Font(self.font,self.text_size)

        # 處理圖案
        self.image = pygame.Surface((self.rect[2],self.rect[3]) , pygame.SRCALPHA)
        self.image.fill((0,0,0,0)) #全透明
        self.text_image = self.text_font.render(self.text,self.antialiab,self.text_color)
        if background:
            self.background_image = pygame.Surface((self.rect[2],self.rect[3]))
            pygame.draw.rect(self.background_image , self.bg_color , (0,0,self.rect[2],self.rect[3]) ,  border_radius = self.bg_b_r)
        
        if background :
            self.image.blit(self.background_image , (0,0,self.rect[2],self.rect[3]))
        self.text_rect = self.text_image.get_rect()
        self.text_rect.center = (self.rect[2]//2 , self.rect[3]//2)
        self.image.blit(self.text_image ,self.text_rect)

        # rect
        self.image_rect = self.image.get_rect()
        self.image_rect.x = self.rect[0]
        self.image_rect.y = self.rect[1]

    def draw(self , screen:pygame.Surface):
        """
        繪製，需給予繪製視窗
        """
        screen.blit(self.image,self.image_rect)

    def change_text(self , text = "__update__"):
        """
        使用此函示變更文字，若設定為 __update__ 則不會更興
        """
        if text != "__update__":
            self.text = text
            
        self.image.fill((0,0,0,0)) #全透明

        self.text_image = self.text_font.render(self.text,self.antialiab,self.text_color)
        if self.background : self.image.blit(self.background_image , (0,0,self.rect[2],self.rect[3]))
        self.text_rect = self.text_image.get_rect()
        self.text_rect.center = (self.rect[2]//2 , self.rect[3]//2)
        self.image.blit(self.text_image ,self.text_rect)

# pygame.init()
# screen = pygame.display.set_mode((640,480))
# n = 1
# l = label(str(n) , (100,100,200,100),(90,255,43),30,"arial",True,True,(3,56,2),30)

# while True:
#     l.draw(screen)
#     pygame.display.update()

#     n += 1
#     l.change_text(str(n))

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             break