import pygame

pygame.font.init()
arial = pygame.font.match_font('arial')
FONT = pygame.font.Font( arial,36)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

class Button:
    def __init__(self, x, y, w, h, text, color=GRAY, text_color=BLACK, hover_color=BLUE,textsize = -1,font:str = arial , border_radius = -1):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.hover_color = hover_color
        self.current_color = color
        self.text_size = textsize
        self.h = h
        if textsize == -1:
            self.font = pygame.font.Font(font,h-15)
        else:
            self.font = pygame.font.Font(font,textsize)
        self.text_surface = self.font.render(text, True, text_color)
        self.border_radius = border_radius

    def create_text(self , text :str = "__None__"):
        """
        當重興修改文字時可是用這個函示修改
        """
        if text != "__None__":
            self.text = text
        self.text_surface = self.font.render(text, True, self.text_color)

    def draw(self, screen):
        pygame.draw.rect(screen, self.current_color, self.rect , border_radius= self.border_radius)
        screen.blit(self.text_surface, (
            self.rect.x + (self.rect.width - self.text_surface.get_width()) // 2,
            self.rect.y + (self.rect.height - self.text_surface.get_height()) // 2,
        ))

    def handle_event(self,events,move = (0,0)):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                # 檢查滑鼠是否在按鈕範圍內
                if self.rect.collidepoint(event.pos[0] - move[0],event.pos[1] - move[1]):
                    self.current_color = self.hover_color
                else:
                    self.current_color = self.color
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.rect.collidepoint(event.pos[0] - move[0],event.pos[1] - move[1]):
                        return True  # 如果按鈕被點擊，返回 True
        return False