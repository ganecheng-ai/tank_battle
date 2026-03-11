"""
碰撞检测模块
处理游戏中的各种碰撞检测
"""

import pygame
from src.terrain import TERRAIN_BRICK, TERRAIN_STEEL, TERRAIN_BASE


class CollisionDetector:
    """碰撞检测器"""

    def __init__(self):
        pass

    def check_bullet_terrain_collision(self, bullet, terrains):
        """检测子弹与地形的碰撞"""
        if not bullet.active:
            return None

        bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)

        for terrain in terrains:
            if terrain.active and terrain.blocks_bullet():
                if bullet_rect.colliderect(terrain.get_rect()):
                    # 处理碰撞
                    if terrain.terrain_type == TERRAIN_BRICK:
                        terrain.take_damage(bullet.damage)
                        bullet.active = True  # 普通子弹击中砖块后消失
                    elif terrain.terrain_type == TERRAIN_STEEL:
                        # 钢板不被子弹破坏
                        pass
                    elif terrain.terrain_type == TERRAIN_BASE:
                        terrain.take_damage(bullet.damage)

                    if terrain.terrain_type in [TERRAIN_BRICK, TERRAIN_STEEL]:
                        bullet.active = False

                    return terrain

        return None

    def check_bullet_tank_collision(self, bullet, tanks):
        """检测子弹与坦克的碰撞"""
        if not bullet.active:
            return None

        bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)

        for tank in tanks:
            if tank.active and tank is not bullet.owner:
                # 检查是否是友军
                if bullet.owner_type == "player" and isinstance(tank, type(bullet.owner)):
                    if tank.tank_type == "player":
                        continue  # 玩家子弹不会伤害其他玩家
                elif bullet.owner_type != "player" and tank.tank_type != "player":
                    continue  # 敌人子弹不会伤害其他敌人

                if bullet_rect.colliderect(tank.get_rect()):
                    tank.take_damage(bullet.damage)
                    bullet.active = False
                    return tank

        return None

    def check_tank_terrain_collision(self, tank, terrains):
        """检测坦克与地形的碰撞"""
        tank_rect = tank.get_rect()

        for terrain in terrains:
            if terrain.active and terrain.is_solid():
                if tank_rect.colliderect(terrain.get_rect()):
                    return terrain

        return None

    def check_tank_tank_collision(self, tank, tanks):
        """检测坦克与其他坦克的碰撞"""
        tank_rect = tank.get_rect()

        for other_tank in tanks:
            if other_tank is not tank and other_tank.active:
                if tank_rect.colliderect(other_tank.get_rect()):
                    return other_tank

        return None

    def resolve_tank_terrain_collision(self, tank, terrains):
        """解决坦克与地形的碰撞"""
        tank_rect = tank.get_rect()

        for terrain in terrains:
            if terrain.active and terrain.is_solid():
                terrain_rect = terrain.get_rect()

                if tank_rect.colliderect(terrain_rect):
                    # 计算重叠区域
                    overlap_left = tank_rect.right - terrain_rect.left
                    overlap_right = terrain_rect.right - tank_rect.left
                    overlap_top = tank_rect.bottom - terrain_rect.top
                    overlap_bottom = terrain_rect.bottom - tank_rect.top

                    # 找到最小的重叠方向
                    min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

                    if min_overlap == overlap_left:
                        tank.x = terrain_rect.left - tank.width
                    elif min_overlap == overlap_right:
                        tank.x = terrain_rect.right
                    elif min_overlap == overlap_top:
                        tank.y = terrain_rect.top - tank.height
                    elif min_overlap == overlap_bottom:
                        tank.y = terrain_rect.bottom

                    tank.rect.x = int(tank.x)
                    tank.rect.y = int(tank.y)

    def check_explosion_damage(self, explosion_x, explosion_y, explosion_radius, targets):
        """检测爆炸范围伤害"""
        explosion_rect = pygame.Rect(
            explosion_x - explosion_radius,
            explosion_y - explosion_radius,
            explosion_radius * 2,
            explosion_radius * 2
        )

        damaged = []
        for target in targets:
            if target.active and explosion_rect.colliderect(target.get_rect()):
                damaged.append(target)

        return damaged


def rect_collides_with_rect(rect1, rect2):
    """检测两个矩形是否碰撞"""
    return rect1.colliderect(rect2)


def point_in_rect(x, y, rect):
    """检测点是否在矩形内"""
    return rect.collidepoint(x, y)


def circle_rect_collision(circle_x, circle_y, circle_radius, rect):
    """检测圆形与矩形的碰撞"""
    # 找到矩形上离圆心最近的点
    closest_x = max(rect.left, min(circle_x, rect.right))
    closest_y = max(rect.top, min(circle_y, rect.bottom))

    # 计算距离
    distance_x = circle_x - closest_x
    distance_y = circle_y - closest_y

    return (distance_x ** 2 + distance_y ** 2) <= (circle_radius ** 2)
