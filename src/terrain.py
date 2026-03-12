"""
地形类模块
定义游戏中的各种地形
"""

import pygame
import math
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
        """绘制砖块 - 精美纹理"""
        rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # 砖块背景
        pygame.draw.rect(screen, (140, 80, 50), rect)

        # 绘制砖块纹理（交错排列）
        brick_rows = 4
        brick_cols = 2
        brick_height = self.height // brick_rows
        brick_width = self.width // brick_cols

        for row in range(brick_rows):
            offset = (row % 2) * (brick_width // 2)
            for col in range(brick_cols + 1):
                bx = self.x + col * brick_width - offset
                by = self.y + row * brick_height

                # 砖块主体
                brick_rect = pygame.Rect(bx + 2, by + 2, brick_width - 4, brick_height - 4)
                pygame.draw.rect(screen, (160, 82, 45), brick_rect)

                # 砖块高光
                highlight_rect = pygame.Rect(bx + 4, by + 4, brick_width - 8, brick_height // 3)
                pygame.draw.rect(screen, (180, 100, 60), highlight_rect)

                # 砖块阴影
                shadow_rect = pygame.Rect(bx + 4, by + brick_height - 8, brick_width - 8, 4)
                pygame.draw.rect(screen, (100, 50, 25), shadow_rect)

        # 外边框
        pygame.draw.rect(screen, (80, 40, 20), rect, 3)

    def _draw_steel(self, screen):
        """绘制钢板 - 金属质感"""
        rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # 钢板底色
        pygame.draw.rect(screen, (160, 160, 160), rect)

        # 金属渐变效果
        for i in range(0, self.width, 4):
            brightness = 180 + int(40 * abs(i / self.width - 0.5) * 2)
            pygame.draw.rect(screen, (brightness, brightness, brightness),
                           (self.x + i, self.y, 2, self.height))

        # 铆钉效果（四个角）
        rivet_positions = [
            (self.x + 6, self.y + 6),
            (self.x + self.width - 6, self.y + 6),
            (self.x + 6, self.y + self.height - 6),
            (self.x + self.width - 6, self.y + self.height - 6)
        ]
        for rx, ry in rivet_positions:
            # 铆钉外圈
            pygame.draw.circle(screen, (120, 120, 120), (int(rx), int(ry)), 6)
            # 铆钉内圈（高光）
            pygame.draw.circle(screen, (200, 200, 200), (int(rx - 1), int(ry - 1)), 3)

        # 中心装饰
        center_x, center_y = self.x + self.width // 2, self.y + self.height // 2
        pygame.draw.circle(screen, (140, 140, 140), (int(center_x), int(center_y)), 8)

        # 外边框
        pygame.draw.rect(screen, (100, 100, 100), rect, 3)

    def _draw_water(self, screen):
        """绘制水域 - 动态波浪"""
        rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # 水底色
        pygame.draw.rect(screen, (30, 100, 150), rect)

        # 动态波浪效果
        time_offset = pygame.time.get_ticks() / 500
        wave_count = 4

        for i in range(wave_count):
            wave_y = self.y + (i + 1) * (self.height / (wave_count + 1))

            # 波浪点
            points = []
            for px in range(0, self.width + 10, 10):
                offset = math.sin((px / 20) + time_offset + i) * 3
                points.append((self.x + px, wave_y + offset))

            if len(points) > 1:
                pygame.draw.lines(screen, (80, 180, 255), False, points, 2)

        # 水面高光
        for i in range(3):
            highlight_x = self.x + 10 + i * 15
            highlight_y = self.y + 10 + i * 5
            pygame.draw.line(screen, (150, 220, 255),
                           (highlight_x, highlight_y),
                           (highlight_x + 10, highlight_y + 2), 2)

    def _draw_grass(self, screen):
        """绘制草地 - 自然草丛效果"""
        rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # 草地底色
        pygame.draw.rect(screen, (60, 140, 60), rect)

        # 随机草丛（使用确定性伪随机，基于位置）
        grass_positions = [
            (self.x + 5, self.y + 5),
            (self.x + 15, self.y + 8),
            (self.x + 25, self.y + 3),
            (self.x + 35, self.y + 10),
            (self.x + 8, self.y + 20),
            (self.x + 18, self.y + 25),
            (self.x + 30, self.y + 18),
            (self.x + 40, self.y + 22),
            (self.x + 10, self.y + 35),
            (self.x + 22, self.y + 38),
            (self.x + 35, self.y + 32),
        ]

        for gx, gy in grass_positions:
            # 草叶
            grass_height = 8 + (hash(str(gx) + str(gy)) % 5)
            pygame.draw.line(screen, (40, 120, 40),
                           (gx, gy + grass_height),
                           (gx - 2, gy), 2)
            pygame.draw.line(screen, (50, 130, 50),
                           (gx + 3, gy + grass_height),
                           (gx + 3, gy), 2)
            pygame.draw.line(screen, (45, 125, 45),
                           (gx + 6, gy + grass_height),
                           (gx + 8, gy), 2)

        # 草地纹理
        for i in range(5):
            for j in range(5):
                dot_x = self.x + i * 10 + 5
                dot_y = self.y + j * 10 + 5
                pygame.draw.circle(screen, (50, 130, 50), (dot_x, dot_y), 2)

    def _draw_base(self, screen):
        """绘制基地 - 精致城堡"""
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2

        # 城堡主体（石材质感）
        castle_rect = pygame.Rect(self.x + 8, self.y + 12, 32, 28)
        pygame.draw.rect(screen, (139, 90, 60), castle_rect)

        # 石砖纹理
        for row in range(3):
            for col in range(4):
                brick_x = self.x + 10 + col * 8
                brick_y = self.y + 14 + row * 8
                brick_rect = pygame.Rect(brick_x, brick_y, 7, 6)
                pygame.draw.rect(screen, (120, 75, 50), brick_rect)

        # 屋顶（红色瓦片）
        roof_points = [
            (self.x + 6, self.y + 12),
            (center_x, self.y - 6),
            (self.x + self.width - 6, self.y + 12)
        ]
        pygame.draw.polygon(screen, (150, 50, 40), roof_points)

        # 屋顶高光
        roof_highlight_points = [
            (center_x, self.y - 6),
            (center_x + 5, self.y + 2),
            (center_x, self.y + 2),
        ]
        pygame.draw.polygon(screen, (180, 70, 60), roof_highlight_points)

        # 入口
        entrance_rect = pygame.Rect(center_x - 6, self.y + 28, 12, 12)
        pygame.draw.rect(screen, (60, 40, 30), entrance_rect)
        pygame.draw.arc(screen, (60, 40, 30),
                       (center_x - 6, self.y + 22, 12, 12),
                       3.14, 0, 3)

        # 旗帜杆
        pygame.draw.line(screen, (100, 80, 60),
                        (center_x, self.y - 6),
                        (center_x, self.y - 18), 2)

        # 旗帜（飘动效果）
        time_offset = pygame.time.get_ticks() / 300
        wave = math.sin(time_offset) * 3
        flag_points = [
            (center_x, self.y - 18),
            (center_x + 14 + wave, self.y - 14),
            (center_x, self.y - 10)
        ]
        pygame.draw.polygon(screen, (220, 40, 40), flag_points)
        pygame.draw.polygon(screen, (255, 80, 80),
                          [(center_x, self.y - 18), (center_x + 6 + wave, self.y - 15), (center_x, self.y - 12)])

        # 边框
        pygame.draw.rect(screen, (80, 50, 30), castle_rect, 2)

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
