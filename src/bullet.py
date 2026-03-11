"""
子弹类模块
定义子弹的类型和行为
"""

import pygame
from config import (
    BULLET_SPEED, BULLET_SIZE,
    DIRECTION_UP, DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_RIGHT
)
from src.entity import Entity


class Bullet(Entity):
    """子弹类"""

    def __init__(self, x, y, direction, owner_type="player", level=1):
        super().__init__(x, y, BULLET_SIZE, BULLET_SIZE)
        self.direction = direction
        self.owner_type = owner_type
        self.level = level
        self.speed = BULLET_SPEED + level * 0.5
        self.damage = 1 + level // 2
        self.bullet_type = "normal"  # normal, fast, pierce

        # 设置子弹颜色
        if owner_type == "player":
            self.color = (255, 255, 0)  # 黄色
        else:
            self.color = (255, 0, 0)  # 红色

    def update(self, delta_time=0):
        """更新子弹位置"""
        if self.direction == DIRECTION_UP:
            self.y -= self.speed
        elif self.direction == DIRECTION_DOWN:
            self.y += self.speed
        elif self.direction == DIRECTION_LEFT:
            self.x -= self.speed
        elif self.direction == DIRECTION_RIGHT:
            self.x += self.speed

        # 检查是否超出边界
        if self.is_out_of_bounds():
            self.active = False

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw(self, screen):
        """绘制子弹"""
        # 绘制圆形子弹
        center_x = int(self.x + self.width // 2)
        center_y = int(self.y + self.height // 2)
        pygame.draw.circle(screen, self.color, (center_x, center_y), 4)
        pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), 2)


class FastBullet(Bullet):
    """高速子弹"""

    def __init__(self, x, y, direction, owner_type="player", level=1):
        super().__init__(x, y, direction, owner_type, level)
        self.speed = BULLET_SPEED * 1.5
        self.bullet_type = "fast"


class PierceBullet(Bullet):
    """穿甲子弹"""

    def __init__(self, x, y, direction, owner_type="player", level=1):
        super().__init__(x, y, direction, owner_type, level)
        self.speed = BULLET_SPEED
        self.bullet_type = "pierce"
        self.pierce_count = 0
        self.max_pierce = level

    def hit(self):
        """击中目标"""
        self.pierce_count += 1
        if self.pierce_count >= self.max_pierce:
            self.active = False
