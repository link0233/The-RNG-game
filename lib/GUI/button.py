import pygame

pygame.font.init()
arial = pygame.font.match_font('arial')
FONT = pygame.font.Font( arial,36)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

class Button:
    def __init__(self, x, y, w, h, text, color=GRAY, text_color=BLACK, hover_color=BLUE):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.hover_color = hover_color
        self.current_color = color
        self.text_surface = FONT.render(text, True, text_color)

    def draw(self, screen):
        pygame.draw.rect(screen, self.current_color, self.rect)
        screen.blit(self.text_surface, (
            self.rect.x + (self.rect.width - self.text_surface.get_width()) // 2,
            self.rect.y + (self.rect.height - self.text_surface.get_height()) // 2,
        ))

    def handle_event(self,events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                # 檢查滑鼠是否在按鈕範圍內
                if self.rect.collidepoint(event.pos):
                    self.current_color = self.hover_color
                else:
                    self.current_color = self.color
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.rect.collidepoint(event.pos):
                        return True  # 如果按鈕被點擊，返回 True
        return False