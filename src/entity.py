"""
实体基类模块
定义所有游戏实体的共同属性和方法
"""

import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT


class Entity:
    """游戏实体基类"""

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.direction = 0  # 0:上，1:右，2:下，3:左
        self.speed = 0
        self.active = True
        self.image = None
        self.rect = pygame.Rect(x, y, width, height)

    def update(self, delta_time=0):
        """更新实体状态"""
        pass

    def draw(self, screen):
        """绘制实体"""
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            # 默认绘制矩形
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

    def get_rect(self):
        """获取碰撞矩形"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def is_out_of_bounds(self):
        """检查是否超出边界"""
        return (self.x < 0 or self.x + self.width > SCREEN_WIDTH or
                self.y < 0 or self.y + self.height > SCREEN_HEIGHT)

    def move(self, dx, dy):
        """移动实体"""
        self.x += dx
        self.y += dy
        self.rect.x = self.x
        self.rect.y = self.y
