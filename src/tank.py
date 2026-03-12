"""
坦克类模块
定义玩家坦克和敌人坦克
"""

import pygame
from config import (
    TANK_SPEED, TANK_SIZE, TANK_ROTATION_SPEED,
    DIRECTION_UP, DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_RIGHT,
    SCREEN_WIDTH, SCREEN_HEIGHT
)
from src.entity import Entity


class Tank(Entity):
    """坦克基类"""

    def __init__(self, x, y, tank_type="player"):
        super().__init__(x, y, TANK_SIZE, TANK_SIZE)
        self.tank_type = tank_type
        self.speed = TANK_SPEED
        self.direction = DIRECTION_UP
        self.lives = 1
        self.level = 1
        self.health = 1
        self.max_health = 1
        self.shoot_cooldown = 0
        self.shoot_delay = 30  # 射击冷却帧数
        self.score = 0
        self.invincible = False
        self.invincible_timer = 0
        self.color = self._get_default_color()

    def _get_default_color(self):
        """获取默认颜色"""
        if self.tank_type == "player":
            return (0, 200, 0)  # 绿色
        elif self.tank_type == "enemy_normal":
            return (200, 200, 0)  # 黄色
        elif self.tank_type == "enemy_fast":
            return (200, 100, 0)  # 橙色
        elif self.tank_type == "enemy_heavy":
            return (150, 150, 150)  # 灰色
        elif self.tank_type == "enemy_boss":
            return (200, 0, 0)  # 红色
        return (255, 255, 255)

    def create_surface(self):
        """创建坦克表面 - 精美绘制"""
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))

        # 坦克主体颜色根据类型有所不同
        base_color = self.color
        highlight_color = tuple(min(255, c + 40) for c in base_color)
        shadow_color = tuple(max(0, c - 40) for c in base_color)

        # 绘制履带（底层）
        track_color = (50, 50, 50)
        track_width = 10
        if self.direction in [DIRECTION_UP, DIRECTION_DOWN]:
            # 左右履带
            left_track = pygame.Rect(0, 2, track_width, self.height - 4)
            right_track = pygame.Rect(self.width - track_width, 2, track_width, self.height - 4)
        else:
            # 上下履带
            left_track = pygame.Rect(2, 0, self.width - 4, track_width)
            right_track = pygame.Rect(2, self.height - track_width, self.width - 4, track_width)

        pygame.draw.rect(surface, track_color, left_track, border_radius=3)
        pygame.draw.rect(surface, track_color, right_track, border_radius=3)

        # 履带纹理
        pygame.draw.rect(surface, (30, 30, 30), left_track, 2, border_radius=3)
        pygame.draw.rect(surface, (30, 30, 30), right_track, 2, border_radius=3)

        # 绘制坦克主体（中层）
        body_rect = pygame.Rect(10, 10, self.width - 20, self.height - 20)
        pygame.draw.rect(surface, base_color, body_rect, border_radius=5)
        pygame.draw.rect(surface, shadow_color, body_rect, 3, border_radius=5)

        # 主体高光
        inner_rect = pygame.Rect(14, 14, self.width - 28, self.height - 28)
        highlight_surface = pygame.Surface((inner_rect.width, inner_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(highlight_surface, (*highlight_color, 80), highlight_surface.get_rect(), border_radius=3)
        surface.blit(highlight_surface, (inner_rect.x, inner_rect.y))

        # 绘制炮塔（中心圆）
        center_x, center_y = self.width // 2, self.height // 2
        turret_radius = 12
        pygame.draw.circle(surface, shadow_color, (center_x, center_y), turret_radius + 2)
        pygame.draw.circle(surface, base_color, (center_x, center_y), turret_radius)
        pygame.draw.circle(surface, highlight_color, (center_x - 2, center_y - 2), turret_radius - 4)

        # 绘制炮管（根据方向）
        barrel_width = 10
        barrel_length = 22
        if self.direction == DIRECTION_UP:
            barrel_rect = pygame.Rect(center_x - barrel_width // 2, 0, barrel_width, barrel_length)
        elif self.direction == DIRECTION_DOWN:
            barrel_rect = pygame.Rect(center_x - barrel_width // 2, self.height - barrel_length, barrel_width, barrel_length)
        elif self.direction == DIRECTION_LEFT:
            barrel_rect = pygame.Rect(0, center_y - barrel_width // 2, barrel_length, barrel_width)
        else:  # DIRECTION_RIGHT
            barrel_rect = pygame.Rect(self.width - barrel_length, center_y - barrel_width // 2, barrel_length, barrel_width)

        pygame.draw.rect(surface, shadow_color, barrel_rect, border_radius=3)
        pygame.draw.rect(surface, base_color, pygame.Rect(barrel_rect.x + 1, barrel_rect.y + 1, barrel_rect.width - 2, barrel_rect.height - 2), border_radius=2)

        # 履带细节 - 添加履带上的凸起
        if self.direction in [DIRECTION_UP, DIRECTION_DOWN]:
            for i in range(6):
                y_pos = 4 + i * 6
                pygame.draw.line(surface, (40, 40, 40), (2, y_pos), (8, y_pos), 2)
                pygame.draw.line(surface, (40, 40, 40), (self.width - 8, y_pos), (self.width - 2, y_pos), 2)
        else:
            for i in range(6):
                x_pos = 4 + i * 6
                pygame.draw.line(surface, (40, 40, 40), (x_pos, 2), (x_pos, 8), 2)
                pygame.draw.line(surface, (40, 40, 40), (x_pos, self.height - 8), (x_pos, self.height - 2), 2)

        # 无敌状态效果
        if self.invincible:
            surface.set_alpha(200 + int(55 * pygame.time.get_ticks() / 100 % 2))

        return surface

    def update(self, delta_time=0):
        """更新坦克状态"""
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if self.invincible and self.invincible_timer > 0:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

        self.rect.x = self.x
        self.rect.y = self.y

    def move(self, direction, terrains=None, tanks=None):
        """移动坦克"""
        self.direction = direction

        dx = 0
        dy = 0

        if direction == DIRECTION_UP:
            dy = -self.speed
        elif direction == DIRECTION_DOWN:
            dy = self.speed
        elif direction == DIRECTION_LEFT:
            dx = -self.speed
        elif direction == DIRECTION_RIGHT:
            dx = self.speed

        new_x = self.x + dx
        new_y = self.y + dy

        # 边界检测
        if new_x < 0:
            new_x = 0
        if new_y < 0:
            new_y = 0
        if new_x + self.width > SCREEN_WIDTH:
            new_x = SCREEN_WIDTH - self.width
        if new_y + self.height > SCREEN_HEIGHT:
            new_y = SCREEN_HEIGHT - self.height

        # 碰撞检测
        new_rect = pygame.Rect(new_x, new_y, self.width, self.height)

        if terrains:
            for terrain in terrains:
                if terrain.active and new_rect.colliderect(terrain.get_rect()):
                    if terrain.is_solid():
                        if dx != 0:
                            new_x = self.x
                        if dy != 0:
                            new_y = self.y
                        break

        if tanks:
            for tank in tanks:
                if tank is not self and tank.active and new_rect.colliderect(tank.get_rect()):
                    if dx != 0:
                        new_x = self.x
                    if dy != 0:
                        new_y = self.y
                    break

        self.x = new_x
        self.y = new_y
        self.rect.x = self.x
        self.rect.y = self.y

    def shoot(self):
        """射击"""
        if self.shoot_cooldown > 0:
            return None

        self.shoot_cooldown = self.shoot_delay

        # 计算子弹起始位置
        if self.direction == DIRECTION_UP:
            bullet_x = self.x + self.width // 2 - 4
            bullet_y = self.y - 8
        elif self.direction == DIRECTION_DOWN:
            bullet_x = self.x + self.width // 2 - 4
            bullet_y = self.y + self.height
        elif self.direction == DIRECTION_LEFT:
            bullet_x = self.x - 8
            bullet_y = self.y + self.height // 2 - 4
        else:  # DIRECTION_RIGHT
            bullet_x = self.x + self.width
            bullet_y = self.y + self.height // 2 - 4

        from src.bullet import Bullet
        return Bullet(bullet_x, bullet_y, self.direction, self.tank_type, self.level)

    def take_damage(self, damage=1):
        """受到伤害"""
        if self.invincible:
            return False

        self.health -= damage
        if self.health <= 0:
            self.active = False
            return True
        return False

    def upgrade(self):
        """升级坦克"""
        self.level += 1
        self.max_health += 1
        self.health = self.max_health
        self.shoot_delay = max(15, self.shoot_delay - 3)

    def draw(self, screen):
        """绘制坦克"""
        surface = self.create_surface()

        # 无敌状态闪烁效果
        if self.invincible and (self.invincible_timer // 5) % 2 == 0:
            surface.set_alpha(128)
        else:
            surface.set_alpha(255)

        screen.blit(surface, (self.x, self.y))


class PlayerTank(Tank):
    """玩家坦克"""

    def __init__(self, x, y, player_id=1):
        super().__init__(x, y, "player")
        self.player_id = player_id
        self.lives = 3
        self.health = 1
        self.max_health = 1

    def handle_input(self, keys):
        """处理玩家输入"""
        moving = False

        if self.player_id == 1:
            # 玩家 1 使用 WASD
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.move(DIRECTION_UP)
                moving = True
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.move(DIRECTION_DOWN)
                moving = True
            elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.move(DIRECTION_LEFT)
                moving = True
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.move(DIRECTION_RIGHT)
                moving = True
        else:
            # 玩家 2 使用方向键
            if keys[pygame.K_KP8] or keys[pygame.K_UP]:
                self.move(DIRECTION_UP)
                moving = True
            elif keys[pygame.K_KP2] or keys[pygame.K_DOWN]:
                self.move(DIRECTION_DOWN)
                moving = True
            elif keys[pygame.K_KP4] or keys[pygame.K_LEFT]:
                self.move(DIRECTION_LEFT)
                moving = True
            elif keys[pygame.K_KP6] or keys[pygame.K_RIGHT]:
                self.move(DIRECTION_RIGHT)
                moving = True

        return moving

    def want_to_shoot(self, keys):
        """检查是否想要射击"""
        if self.player_id == 1:
            return keys[pygame.K_j] or keys[pygame.K_SPACE]
        else:
            return keys[pygame.K_KP0] or keys[pygame.K_RCTRL]


class EnemyTank(Tank):
    """敌人坦克"""

    def __init__(self, x, y, tank_type="enemy_normal"):
        super().__init__(x, y, tank_type)

        # 根据类型设置属性
        if tank_type == "enemy_fast":
            self.speed = TANK_SPEED * 1.5
            self.health = 1
        elif tank_type == "enemy_heavy":
            self.speed = TANK_SPEED * 0.7
            self.health = 3
        elif tank_type == "enemy_boss":
            self.speed = TANK_SPEED * 0.5
            self.health = 10
            self.width = TANK_SIZE * 1.5
            self.height = TANK_SIZE * 1.5
        else:  # enemy_normal
            self.speed = TANK_SPEED
            self.health = 1

        self.max_health = self.health
        self.move_timer = 0
        self.move_duration = 60
        self.shoot_timer = 30

    def update_ai(self, player_tank, terrains):
        """更新 AI 行为"""
        self.update()

        # 移动计时器
        self.move_timer += 1
        if self.move_timer >= self.move_duration:
            self.move_timer = 0
            self.move_duration = 30 + pygame.time.get_ticks() % 60

            # 随机改变方向，但有概率朝向玩家
            if pygame.time.get_ticks() % 100 < 40 and player_tank and player_tank.active:
                dx = player_tank.x - self.x
                dy = player_tank.y - self.y

                if abs(dx) > abs(dy):
                    self.direction = DIRECTION_RIGHT if dx > 0 else DIRECTION_LEFT
                else:
                    self.direction = DIRECTION_DOWN if dy > 0 else DIRECTION_UP
            else:
                self.direction = pygame.time.get_ticks() % 4

        # 移动
        old_x, old_y = self.x, self.y
        self.move(self.direction, terrains)

        # 如果移动受阻，改变方向
        if abs(self.x - old_x) < 0.1 and abs(self.y - old_y) < 0.1:
            self.move_timer = self.move_duration

        # 射击计时器
        self.shoot_timer += 1
        if self.shoot_timer >= 60 and pygame.time.get_ticks() % 100 < 30:
            self.shoot_timer = 0
            return True

        return False
