import pygame
import sys

class ImageButton:
    def __init__(self, screen, image_path, hover_image_path, position, transparency):
        """
        初始化按鈕屬性
        :param screen: Pygame 畫布
        :param image_path: 按鈕圖片路徑
        :param hover_image_path: 滑鼠懸停時按鈕圖片路徑
        :param position: 按鈕的位置 (x, y)
        :param transparency: 按鈕的透明度 (0-255)
        """
        self.screen = screen

        self.image = pygame.image.load(image_path).convert_alpha()
        self.image.set_colorkey((0, 0, 0))  # 設置黑色 (0, 0, 0) 為透明色
        self.image.set_alpha(transparency)  # 設置透明度

        self.hover_image = pygame.image.load(hover_image_path).convert_alpha()
        self.hover_image.set_colorkey((0, 0, 0))  # 設置黑色 (0, 0, 0) 為透明色
        self.hover_image.set_alpha(transparency)

        self.rect = self.image.get_rect(center=position)
        self.is_hovered = False
        self.is_clicked = False

    def draw(self):
        """繪製按鈕"""
        if self.is_hovered:
            self.screen.blit(self.hover_image, self.rect)
        else:
            self.screen.blit(self.image, self.rect)

    def update_hover_state(self, events,rect_move = (0,0)):
        """
        更新按鈕的懸停狀態
        :param event : pygame evnet
        """
        # 檢查滑鼠是否在按鈕範圍內
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                # print((event.pos[0] - rect_move[0],event.pos[1] - rect_move[1]))
                # print(self.rect.center)
                # print(rect_move)
                self.is_hovered = self.rect.collidepoint((event.pos[0] - rect_move[0],event.pos[1] - rect_move[1]))

    def check_clicked(self, events,rect_move = (0,0)):
        """
        檢測按鈕是否被點擊
        :param events: Pygame 事件
        :return: 如果被點擊返回 True，否則返回 False
        """
        self.is_clicked = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.rect.collidepoint(event.pos[0] - rect_move[0],event.pos[1] - rect_move[1]):
                        self.is_clicked = True  # 如果按鈕被點擊，返回 True
                