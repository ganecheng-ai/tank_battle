"""
地形类模块
定义游戏中的各种地形
"""

import pygame
from config import (
    TILE_SIZE,
    BLACK, BROWN, STEEL_COLOR, WATER_COLOR, GRASS_COLOR, BLUE
)
from src.entity import Entity


# 地形类型
TERRAIN_EMPTY = 0
TERRAIN_BRICK = 1    # 可破坏砖块
TERRAIN_STEEL = 2    # 不可破坏钢板
TERRAIN_WATER = 3    # 水域
TERRAIN_GRASS = 4    # 草地
TERRAIN_BASE = 5     # 基地（老鹰）


class Terrain(Entity):
    """地形基类"""

    def __init__(self, x, y, terrain_type=TERRAIN_EMPTY):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE)
        self.terrain_type = terrain_type
        self.health = 1 if terrain_type == TERRAIN_BRICK else 999
        self.active = terrain_type != TERRAIN_EMPTY

    def is_solid(self):
        """是否是固体（阻挡坦克）"""
        return self.terrain_type in [TERRAIN_BRICK, TERRAIN_STEEL, TERRAIN_BASE]

    def blocks_bullet(self):
        """是否阻挡子弹"""
        return self.terrain_type in [TERRAIN_BRICK, TERRAIN_STEEL, TERRAIN_BASE]

    def is_visible(self):
        """是否可见"""
        return self.terrain_type != TERRAIN_GRASS

    def take_damage(self, damage=1):
        """受到伤害"""
        if self.terrain_type == TERRAIN_BRICK:
            self.health -= damage
            if self.health <= 0:
                self.active = False
                return True
        elif self.terrain_type == TERRAIN_BASE:
            self.health -= damage
            if self.health <= 0:
                self.active = False
                return True
        return False

    def draw(self, screen):
        """绘制地形"""
        if not self.active:
            return

        if self.terrain_type == TERRAIN_BRICK:
            self._draw_brick(screen)
        elif self.terrain_type == TERRAIN_STEEL:
            self._draw_steel(screen)
        elif self.terrain_type == TERRAIN_WATER:
            self._draw_water(screen)
        elif self.terrain_type == TERRAIN_GRASS:
            self._draw_grass(screen)
        elif self.terrain_type == TERRAIN_BASE:
            self._draw_base(screen)

    def _draw_brick(self, screen):
        """绘制砖块"""
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, BROWN, rect)

        # 绘制砖块纹理
        brick_color = (160, 82, 45)
        for i in range(2):
            for j in range(4):
                bx = self.x + j * 12
                by = self.y + i * 24
                brick_rect = pygame.Rect(bx + 1, by + 1, 10, 22)
                pygame.draw.rect(screen, brick_color, brick_rect)

        # 边框
        pygame.draw.rect(screen, (100, 50, 30), rect, 2)

    def _draw_steel(self, screen):
        """绘制钢板"""
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, STEEL_COLOR, rect)

        # 绘制钢板纹理
        inner_rect = pygame.Rect(self.x + 4, self.y + 4, self.width - 8, self.height - 8)
        pygame.draw.rect(screen, (220, 220, 220), inner_rect)

        # 边框
        pygame.draw.rect(screen, (150, 150, 150), rect, 3)

    def _draw_water(self, screen):
        """绘制水域"""
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, WATER_COLOR, rect)

        # 绘制水波效果
        wave_offset = pygame.time.get_ticks() // 200 % 10
        for i in range(3):
            wave_y = self.y + 10 + i * 15 + wave_offset % 5
            pygame.draw.line(screen, (100, 200, 255),
                           (self.x + 5, wave_y),
                           (self.x + self.width - 5, wave_y), 2)

    def _draw_grass(self, screen):
        """绘制草地"""
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, GRASS_COLOR, rect)

        # 绘制草丛效果
        for i in range(5):
            grass_x = self.x + i * 10 + 2
            pygame.draw.line(screen, (0, 100, 0),
                           (grass_x, self.y + self.height),
                           (grass_x - 3, self.y + self.height - 10), 2)

    def _draw_base(self, screen):
        """绘制基地"""
        # 绘制城堡形状
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2

        # 城堡主体
        castle_rect = pygame.Rect(self.x + 8, self.y + 8, 32, 32)
        pygame.draw.rect(screen, (150, 100, 50), castle_rect)

        # 屋顶
        roof_points = [
            (self.x + 4, self.y + 8),
            (center_x, self.y - 4),
            (self.x + self.width - 4, self.y + 8)
        ]
        pygame.draw.polygon(screen, (139, 69, 19), roof_points)

        # 旗帜
        pygame.draw.line(screen, (255, 0, 0),
                        (center_x, self.y - 4),
                        (center_x, self.y - 20), 2)
        flag_points = [
            (center_x, self.y - 20),
            (center_x + 12, self.y - 15),
            (center_x, self.y - 10)
        ]
        pygame.draw.polygon(screen, (255, 0, 0), flag_points)

        # 边框
        pygame.draw.rect(screen, (100, 50, 20), castle_rect, 2)

    def get_rect(self):
        """获取碰撞矩形"""
        return pygame.Rect(self.x, self.y, self.width, self.height)


class TerrainManager:
    """地形管理器"""

    def __init__(self):
        self.terrains = []
        self.base_terrain = None

    def load_from_grid(self, grid_data):
        """从网格数据加载地形"""
        self.terrains = []

        for row_idx, row in enumerate(grid_data):
            for col_idx, cell in enumerate(row):
                x = col_idx * TILE_SIZE
                y = row_idx * TILE_SIZE

                if cell == TERRAIN_BRICK:
                    self.terrains.append(Terrain(x, y, TERRAIN_BRICK))
                elif cell == TERRAIN_STEEL:
                    self.terrains.append(Terrain(x, y, TERRAIN_STEEL))
                elif cell == TERRAIN_WATER:
                    self.terrains.append(Terrain(x, y, TERRAIN_WATER))
                elif cell == TERRAIN_GRASS:
                    self.terrains.append(Terrain(x, y, TERRAIN_GRASS))
                elif cell == TERRAIN_BASE:
                    base = Terrain(x, y, TERRAIN_BASE)
                    self.terrains.append(base)
                    self.base_terrain = base

    def update(self):
        """更新所有地形"""
        for terrain in self.terrains:
            terrain.update()

    def draw(self, screen, layer="ground"):
        """绘制地形"""
        for terrain in self.terrains:
            if layer == "ground" and terrain.terrain_type != TERRAIN_GRASS:
                terrain.draw(screen)
            elif layer == "grass" and terrain.terrain_type == TERRAIN_GRASS:
                terrain.draw(screen)

    def get_terrains_at(self, x, y):
        """获取指定位置的地形"""
        result = []
        for terrain in self.terrains:
            if terrain.active and terrain.get_rect().collidepoint(x, y):
                result.append(terrain)
        return result

    def check_base_destroyed(self):
        """检查基地是否被摧毁"""
        if self.base_terrain:
            return not self.base_terrain.active
        return False

    def get_colliding_terrains(self, rect):
        """获取与矩形碰撞的地形"""
        result = []
        for terrain in self.terrains:
            if terrain.active and terrain.get_rect().colliderect(rect):
                result.append(terrain)
        return result
