#!/usr/bin/env python3
"""
坦克大战游戏单元测试
"""

import pytest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TILE_SIZE,
    DIRECTION_UP, DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_RIGHT,
    INITIAL_LIVES, TANK_SIZE, BULLET_SIZE
)


class TestConfig:
    """测试配置模块"""

    def test_screen_resolution(self):
        """测试屏幕分辨率配置"""
        assert SCREEN_WIDTH == 1280
        assert SCREEN_HEIGHT == 720

    def test_fps(self):
        """测试帧率配置"""
        assert FPS == 60

    def test_tile_size(self):
        """测试格子大小配置"""
        assert TILE_SIZE == 48

    def test_direction_constants(self):
        """测试方向常量"""
        assert DIRECTION_UP == 0
        assert DIRECTION_RIGHT == 1
        assert DIRECTION_DOWN == 2
        assert DIRECTION_LEFT == 3


class TestEntity:
    """测试实体类"""

    def setup_method(self):
        """设置测试环境"""
        pygame.init()

    def teardown_method(self):
        """清理测试环境"""
        pygame.quit()

    def test_entity_creation(self):
        """测试实体创建"""
        from src.entity import Entity
        entity = Entity(100, 100, 50, 50)

        assert entity.x == 100
        assert entity.y == 100
        assert entity.width == 50
        assert entity.height == 50
        assert entity.active == True

    def test_entity_move(self):
        """测试实体移动"""
        from src.entity import Entity
        entity = Entity(100, 100, 50, 50)

        entity.move(10, 5)

        assert entity.x == 110
        assert entity.y == 105

    def test_entity_get_rect(self):
        """测试实体获取矩形"""
        from src.entity import Entity
        entity = Entity(100, 100, 50, 50)

        rect = entity.get_rect()

        assert rect.x == 100
        assert rect.y == 100
        assert rect.width == 50
        assert rect.height == 50

    def test_entity_out_of_bounds(self):
        """测试实体边界检测"""
        from src.entity import Entity
        entity = Entity(0, 0, 50, 50)

        # 在边界内
        assert entity.is_out_of_bounds() == False

        # 超出左边界
        entity.x = -10
        assert entity.is_out_of_bounds() == True

        # 重置
        entity.x = 0
        entity.y = -10
        assert entity.is_out_of_bounds() == True


class TestTank:
    """测试坦克类"""

    def setup_method(self):
        """设置测试环境"""
        pygame.init()

    def teardown_method(self):
        """清理测试环境"""
        pygame.quit()

    def test_player_tank_creation(self):
        """测试玩家坦克创建"""
        from src.tank import PlayerTank
        tank = PlayerTank(100, 100, 1)

        assert tank.x == 100
        assert tank.y == 100
        assert tank.tank_type == "player"
        assert tank.lives == 3
        assert tank.active == True

    def test_enemy_tank_creation(self):
        """测试敌人坦克创建"""
        from src.tank import EnemyTank
        tank = EnemyTank(200, 200, "enemy_normal")

        assert tank.tank_type == "enemy_normal"
        assert tank.active == True

    def test_tank_shoot(self):
        """测试坦克射击"""
        from src.tank import PlayerTank
        tank = PlayerTank(100, 100, 1)
        tank.direction = DIRECTION_UP

        bullet = tank.shoot()

        assert bullet is not None
        assert bullet.direction == DIRECTION_UP

    def test_tank_take_damage(self):
        """测试坦克受到伤害"""
        from src.tank import PlayerTank
        tank = PlayerTank(100, 100, 1)

        # 第一次伤害
        result = tank.take_damage(1)
        assert result == True  # 坦克死亡

    def test_tank_upgrade(self):
        """测试坦克升级"""
        from src.tank import PlayerTank
        tank = PlayerTank(100, 100, 1)

        initial_level = tank.level
        tank.upgrade()

        assert tank.level == initial_level + 1
        assert tank.max_health > 1


class TestBullet:
    """测试子弹类"""

    def setup_method(self):
        """设置测试环境"""
        pygame.init()

    def teardown_method(self):
        """清理测试环境"""
        pygame.quit()

    def test_bullet_creation(self):
        """测试子弹创建"""
        from src.bullet import Bullet
        bullet = Bullet(100, 100, DIRECTION_UP, "player", 1)

        assert bullet.x == 100
        assert bullet.y == 100
        assert bullet.direction == DIRECTION_UP
        assert bullet.owner_type == "player"
        assert bullet.active == True

    def test_bullet_update(self):
        """测试子弹更新"""
        from src.bullet import Bullet
        bullet = Bullet(100, 100, DIRECTION_UP, "player", 1)

        initial_y = bullet.y
        bullet.update()

        # 向上移动，y 应该减小
        assert bullet.y < initial_y

    def test_bullet_out_of_bounds(self):
        """测试子弹边界检测"""
        from src.bullet import Bullet
        bullet = Bullet(100, -20, DIRECTION_UP, "player", 1)

        bullet.update()

        assert bullet.active == False


class TestTerrain:
    """测试地形类"""

    def setup_method(self):
        """设置测试环境"""
        pygame.init()

    def teardown_method(self):
        """清理测试环境"""
        pygame.quit()

    def test_terrain_creation(self):
        """测试地形创建"""
        from src.terrain import Terrain, TERRAIN_BRICK
        terrain = Terrain(100, 100, TERRAIN_BRICK)

        assert terrain.x == 100
        assert terrain.y == 100
        assert terrain.terrain_type == TERRAIN_BRICK
        assert terrain.active == True

    def test_terrain_is_solid(self):
        """测试地形固体属性"""
        from src.terrain import Terrain, TERRAIN_BRICK, TERRAIN_WATER, TERRAIN_GRASS
        brick = Terrain(0, 0, TERRAIN_BRICK)
        water = Terrain(0, 0, TERRAIN_WATER)
        grass = Terrain(0, 0, TERRAIN_GRASS)

        assert brick.is_solid() == True
        assert water.is_solid() == False
        assert grass.is_solid() == False

    def test_brick_take_damage(self):
        """测试砖块受到伤害"""
        from src.terrain import Terrain, TERRAIN_BRICK
        terrain = Terrain(100, 100, TERRAIN_BRICK)

        result = terrain.take_damage(1)
        assert result == True  # 砖块被摧毁
        assert terrain.active == False

    def test_steel_take_damage(self):
        """测试钢板受到伤害"""
        from src.terrain import Terrain, TERRAIN_STEEL
        terrain = Terrain(100, 100, TERRAIN_STEEL)

        result = terrain.take_damage(1)
        assert result == False  # 钢板不会被摧毁
        assert terrain.active == True


class TestTerrainManager:
    """测试地形管理器"""

    def setup_method(self):
        """设置测试环境"""
        pygame.init()

    def teardown_method(self):
        """清理测试环境"""
        pygame.quit()

    def test_terrain_manager_creation(self):
        """测试地形管理器创建"""
        from src.terrain import TerrainManager
        manager = TerrainManager()

        assert len(manager.terrains) == 0
        assert manager.base_terrain is None

    def test_load_from_grid(self):
        """测试从网格加载地形"""
        from src.terrain import TerrainManager, TERRAIN_BRICK, TERRAIN_BASE

        # 简单的 2x2 网格
        grid = [
            [0, 1],
            [5, 0]
        ]

        manager = TerrainManager()
        manager.load_from_grid(grid)

        assert len(manager.terrains) == 2
        assert manager.base_terrain is not None


class TestCollision:
    """测试碰撞检测"""

    def setup_method(self):
        """设置测试环境"""
        pygame.init()

    def teardown_method(self):
        """清理测试环境"""
        pygame.quit()

    def test_collision_detector_creation(self):
        """测试碰撞检测器创建"""
        from src.collision import CollisionDetector
        detector = CollisionDetector()

        assert detector is not None

    def test_rect_collision(self):
        """测试矩形碰撞"""
        from src.collision import rect_collides_with_rect
        import pygame

        rect1 = pygame.Rect(0, 0, 50, 50)
        rect2 = pygame.Rect(40, 40, 50, 50)
        rect3 = pygame.Rect(100, 100, 50, 50)

        assert rect_collides_with_rect(rect1, rect2) == True
        assert rect_collides_with_rect(rect1, rect3) == False

    def test_point_in_rect(self):
        """测试点在矩形内"""
        from src.collision import point_in_rect
        import pygame

        rect = pygame.Rect(0, 0, 50, 50)

        assert point_in_rect(25, 25, rect) == True
        assert point_in_rect(100, 100, rect) == False


class TestLevel:
    """测试关卡管理"""

    def setup_method(self):
        """设置测试环境"""
        pygame.init()

    def teardown_method(self):
        """清理测试环境"""
        pygame.quit()

    def test_level_manager_creation(self):
        """测试关卡管理器创建"""
        from src.level import LevelManager
        manager = LevelManager()

        assert manager.current_level == 1
        assert manager.terrain_manager is not None

    def test_load_level(self):
        """测试加载关卡"""
        from src.level import LevelManager
        manager = LevelManager()

        result = manager.load_level(1)
        assert result == True
        assert manager.current_level == 1

    def test_load_invalid_level(self):
        """测试加载无效关卡"""
        from src.level import LevelManager
        manager = LevelManager()

        result = manager.load_level(999)
        assert result == False

    def test_get_player_start_position(self):
        """测试获取玩家起始位置"""
        from src.level import LevelManager
        manager = LevelManager()
        manager.load_level(1)

        pos = manager.get_player_start_position(1)

        assert pos is not None
        assert len(pos) == 2

    def test_get_next_level(self):
        """测试获取下一关"""
        from src.level import LevelManager
        manager = LevelManager()
        manager.load_level(1)

        next_level = manager.get_next_level()
        assert next_level == 2


class TestUI:
    """测试 UI 系统"""

    def setup_method(self):
        """设置测试环境"""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    def teardown_method(self):
        """清理测试环境"""
        pygame.quit()

    def test_ui_creation(self):
        """测试 UI 创建"""
        from src.ui import UI
        ui = UI()

        assert ui is not None
        assert len(ui.menu_options) > 0

    def test_draw_menu(self):
        """测试绘制菜单"""
        from src.ui import UI
        ui = UI()

        # 不应该抛出异常
        ui.draw_menu(self.screen)

    def test_explosion_creation(self):
        """测试爆炸特效创建"""
        from src.ui import Explosion
        explosion = Explosion(100, 100, "medium")

        assert explosion.x == 100
        assert explosion.y == 100
        assert explosion.active == True

    def test_explosion_update(self):
        """测试爆炸特效更新"""
        from src.ui import Explosion
        explosion = Explosion(100, 100, "medium")

        initial_frame = explosion.frame
        explosion.update()

        assert explosion.frame > initial_frame


class TestGameIntegration:
    """集成测试"""

    def setup_method(self):
        """设置测试环境"""
        pygame.init()

    def teardown_method(self):
        """清理测试环境"""
        pygame.quit()

    def test_game_module_import(self):
        """测试游戏模块导入"""
        from src import game
        assert hasattr(game, 'Game')

    def test_all_modules_import(self):
        """测试所有模块导入"""
        from src import entity
        from src import tank
        from src import bullet
        from src import terrain
        from src import collision
        from src import level
        from src import ui

        assert entity is not None
        assert tank is not None
        assert bullet is not None
        assert terrain is not None
        assert collision is not None
        assert level is not None
        assert ui is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
