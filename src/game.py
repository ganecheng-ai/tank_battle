"""
游戏主逻辑模块
管理游戏状态、更新和渲染
"""

import pygame
import sys
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE,
    STATE_MENU, STATE_PLAYING, STATE_PAUSED, STATE_GAME_OVER, STATE_LEVEL_COMPLETE, STATE_VICTORY,
    DIRECTION_UP, DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_RIGHT, INITIAL_LIVES
)
from src.tank import PlayerTank, EnemyTank
from src.bullet import Bullet
from src.terrain import TERRAIN_BASE
from src.collision import CollisionDetector
from src.level import LevelManager
from src.ui import UI, Explosion


class Game:
    """游戏主类"""

    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.state = STATE_MENU
        self.ui = UI()
        self.level_manager = LevelManager()
        self.collision_detector = CollisionDetector()

        # 游戏对象
        self.player_tank = None
        self.player2_tank = None
        self.enemies = []
        self.bullets = []
        self.explosions = []

        # 游戏数据
        self.score = 0
        self.current_level = 1
        self.two_player_mode = False

        # 输入状态
        self.keys = pygame.key.get_pressed()

    def reset_game(self):
        """重置游戏状态"""
        self.score = 0
        self.current_level = 1
        self.enemies = []
        self.bullets = []
        self.explosions = []
        self.level_manager = LevelManager()

    def start_game(self, two_player=False):
        """开始新游戏"""
        self.reset_game()
        self.two_player_mode = two_player
        self.load_level(1)
        self.state = STATE_PLAYING

    def load_level(self, level_num):
        """加载关卡"""
        self.level_manager.load_level(level_num)
        self.current_level = level_num

        # 创建玩家坦克
        pos1 = self.level_manager.get_player_start_position(1)
        self.player_tank = PlayerTank(pos1[0], pos1[1], 1)

        if self.two_player_mode:
            pos2 = self.level_manager.get_player_start_position(2)
            self.player2_tank = PlayerTank(pos2[0], pos2[1], 2)
        else:
            self.player2_tank = None

        self.enemies = []
        self.bullets = []
        self.explosions = []

    def spawn_enemy(self, enemy_data):
        """生成敌人"""
        if enemy_data:
            enemy_type, x, y = enemy_data
            enemy = EnemyTank(x, y, enemy_type)
            enemy.direction = DIRECTION_DOWN  # 初始方向向下
            self.enemies.append(enemy)

    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if self.state == STATE_MENU:
                    self.handle_menu_input(event.key)
                elif self.state == STATE_PLAYING:
                    self.handle_playing_input(event.key)
                elif self.state == STATE_PAUSED:
                    self.handle_paused_input(event.key)
                elif self.state == STATE_GAME_OVER:
                    self.handle_game_over_input(event.key)
                elif self.state == STATE_LEVEL_COMPLETE:
                    self.handle_level_complete_input(event.key)
                elif self.state == STATE_VICTORY:
                    self.handle_victory_input(event.key)

        self.keys = pygame.key.get_pressed()
        return True

    def handle_menu_input(self, key):
        """处理菜单输入"""
        if key == pygame.K_UP:
            self.ui.selected_option = (self.ui.selected_option - 1) % len(self.ui.menu_options)
        elif key == pygame.K_DOWN:
            self.ui.selected_option = (self.ui.selected_option + 1) % len(self.ui.menu_options)
        elif key == pygame.K_RETURN:
            if self.ui.selected_option == 0:  # 开始游戏
                self.start_game(False)
            elif self.ui.selected_option == 1:  # 双人模式
                self.start_game(True)
            elif self.ui.selected_option == 2:  # 帮助
                self.show_help()
            elif self.ui.selected_option == 3:  # 退出
                return False
        elif key == pygame.K_ESCAPE:
            return False

    def show_help(self):
        """显示帮助界面"""
        helping = True
        while helping:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    helping = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        helping = False

            self.ui.draw_help(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)

    def handle_playing_input(self, key):
        """处理游戏中输入"""
        if key == pygame.K_p or key == pygame.K_ESCAPE:
            self.state = STATE_PAUSED

    def handle_paused_input(self, key):
        """处理暂停输入"""
        if key == pygame.K_p:
            self.state = STATE_PLAYING
        elif key == pygame.K_ESCAPE:
            self.state = STATE_MENU

    def handle_game_over_input(self, key):
        """处理游戏结束输入"""
        if key == pygame.K_RETURN:
            self.start_game(self.two_player_mode)
        elif key == pygame.K_ESCAPE:
            self.state = STATE_MENU

    def handle_level_complete_input(self, key):
        """处理关卡完成输入"""
        if key == pygame.K_RETURN:
            next_level = self.level_manager.get_next_level()
            if next_level:
                self.load_level(next_level)
                self.state = STATE_PLAYING
            else:
                self.state = STATE_VICTORY

    def handle_victory_input(self, key):
        """处理胜利输入"""
        if key == pygame.K_RETURN:
            self.start_game(self.two_player_mode)
        elif key == pygame.K_ESCAPE:
            self.state = STATE_MENU

    def player_move(self, tank, terrains=None, tanks=None):
        """玩家移动坦克"""
        dx = 0
        dy = 0
        new_direction = tank.direction

        if tank.player_id == 1:
            if self.keys[pygame.K_w] or self.keys[pygame.K_UP]:
                dy = -tank.speed
                new_direction = DIRECTION_UP
            elif self.keys[pygame.K_s] or self.keys[pygame.K_DOWN]:
                dy = tank.speed
                new_direction = DIRECTION_DOWN
            elif self.keys[pygame.K_a] or self.keys[pygame.K_LEFT]:
                dx = -tank.speed
                new_direction = DIRECTION_LEFT
            elif self.keys[pygame.K_d] or self.keys[pygame.K_RIGHT]:
                dx = tank.speed
                new_direction = DIRECTION_RIGHT
        else:
            if self.keys[pygame.K_KP8]:
                dy = -tank.speed
                new_direction = DIRECTION_UP
            elif self.keys[pygame.K_KP2]:
                dy = tank.speed
                new_direction = DIRECTION_DOWN
            elif self.keys[pygame.K_KP4]:
                dx = -tank.speed
                new_direction = DIRECTION_LEFT
            elif self.keys[pygame.K_KP6]:
                dx = tank.speed
                new_direction = DIRECTION_RIGHT

        if dx != 0 or dy != 0:
            tank.direction = new_direction
            new_x = tank.x + dx
            new_y = tank.y + dy

            # 边界检测
            new_x = max(0, min(new_x, SCREEN_WIDTH - tank.width))
            new_y = max(0, min(new_y, SCREEN_HEIGHT - tank.height))

            # 碰撞检测
            new_rect = pygame.Rect(new_x, new_y, tank.width, tank.height)
            can_move = True

            if terrains:
                for terrain in terrains:
                    if terrain.active and terrain.is_solid():
                        if new_rect.colliderect(terrain.get_rect()):
                            can_move = False
                            break

            if tanks and can_move:
                for other_tank in tanks:
                    if other_tank is not tank and other_tank.active:
                        if new_rect.colliderect(other_tank.get_rect()):
                            can_move = False
                            break

            if can_move:
                tank.x = new_x
                tank.y = new_y
                tank.rect.x = int(tank.x)
                tank.rect.y = int(tank.y)

    def player_shoot(self, tank):
        """玩家射击"""
        if tank.player_id == 1:
            if self.keys[pygame.K_j] or self.keys[pygame.K_SPACE]:
                return True
        else:
            if self.keys[pygame.K_KP0] or self.keys[pygame.K_RCTRL]:
                return True
        return False

    def update(self):
        """更新游戏状态"""
        if self.state != STATE_PLAYING:
            return

        terrains = self.level_manager.terrain_manager.terrains

        # 更新玩家坦克
        if self.player_tank and self.player_tank.active:
            all_tanks = [self.player_tank] + self.enemies
            if self.player2_tank and self.player2_tank.active:
                all_tanks.append(self.player2_tank)

            self.player_move(self.player_tank, terrains, all_tanks)
            self.player_tank.update()

            # 玩家 1 射击
            if self.player_shoot(self.player_tank):
                bullet = self.player_tank.shoot()
                if bullet:
                    bullet.owner = self.player_tank
                    if bullet not in self.bullets:
                        self.bullets.append(bullet)

        # 更新玩家 2 坦克
        if self.player2_tank and self.player2_tank.active:
            all_tanks = [self.player2_tank] + self.enemies
            if self.player_tank and self.player_tank.active:
                all_tanks.append(self.player_tank)

            self.player_move(self.player2_tank, terrains, all_tanks)
            self.player2_tank.update()

            # 玩家 2 射击
            if self.player_shoot(self.player2_tank):
                bullet = self.player2_tank.shoot()
                if bullet:
                    bullet.owner = self.player2_tank
                    if bullet not in self.bullets:
                        self.bullets.append(bullet)

        # 生成敌人
        enemy_data = self.level_manager.update()
        self.spawn_enemy(enemy_data)

        # 更新敌人
        for enemy in self.enemies:
            if enemy.active:
                should_shoot = enemy.update_ai(self.player_tank, terrains)

                if should_shoot:
                    bullet = enemy.shoot()
                    if bullet:
                        bullet.owner = enemy
                        self.bullets.append(bullet)

        # 更新子弹
        for bullet in self.bullets:
            bullet.update()

        # 更新爆炸
        for explosion in self.explosions:
            explosion.update()

        # 碰撞检测
        self.check_collisions()

        # 清理非活动对象
        self.bullets = [b for b in self.bullets if b.active]
        self.enemies = [e for e in self.enemies if e.active]
        self.explosions = [e for e in self.explosions if e.active]

        # 检查游戏状态
        self.check_game_state()

    def check_collisions(self):
        """处理碰撞检测"""
        terrains = self.level_manager.terrain_manager.terrains
        all_tanks = []
        if self.player_tank and self.player_tank.active:
            all_tanks.append(self.player_tank)
        if self.player2_tank and self.player2_tank.active:
            all_tanks.append(self.player2_tank)
        all_tanks.extend(self.enemies)

        # 子弹碰撞
        for bullet in self.bullets:
            if not bullet.active:
                continue

            # 子弹与地形
            hit_terrain = self.collision_detector.check_bullet_terrain_collision(bullet, terrains)
            if hit_terrain:
                if hit_terrain.terrain_type == TERRAIN_BASE:
                    self.state = STATE_GAME_OVER
                continue

            # 子弹与坦克
            hit_tank = self.collision_detector.check_bullet_tank_collision(bullet, all_tanks)
            if hit_tank:
                if hit_tank.tank_type.startswith("enemy"):
                    self.score += 100
                    self.level_manager.enemy_defeated()
                    self.explosions.append(Explosion(hit_tank.x + hit_tank.width // 2,
                                                      hit_tank.y + hit_tank.height // 2))
                elif hit_tank.tank_type == "player":
                    self.explosions.append(Explosion(hit_tank.x + hit_tank.width // 2,
                                                      hit_tank.y + hit_tank.height // 2))

    def check_game_state(self):
        """检查游戏状态"""
        # 检查玩家是否死亡
        player_dead = not self.player_tank or not self.player_tank.active
        player2_dead = not self.player2_tank or not self.player2_tank.active

        if self.two_player_mode:
            if player_dead and player2_dead:
                self.state = STATE_GAME_OVER
        else:
            if player_dead:
                self.state = STATE_GAME_OVER

        # 检查基地是否被摧毁
        if self.level_manager.terrain_manager.check_base_destroyed():
            self.state = STATE_GAME_OVER

        # 检查关卡是否完成
        if self.level_manager.enemies_remaining <= 0 and len(self.enemies) == 0:
            if self.current_level >= len(LEVEL_MAPS):
                self.state = STATE_VICTORY
            else:
                self.state = STATE_LEVEL_COMPLETE

    def draw(self):
        """绘制游戏画面"""
        self.screen.fill((0, 0, 0))

        if self.state == STATE_MENU:
            self.ui.draw_menu(self.screen)

        elif self.state == STATE_PLAYING:
            self.level_manager.terrain_manager.draw(self.screen, "ground")

            if self.player_tank and self.player_tank.active:
                self.player_tank.draw(self.screen)
            if self.player2_tank and self.player2_tank.active:
                self.player2_tank.draw(self.screen)

            for enemy in self.enemies:
                enemy.draw(self.screen)

            for bullet in self.bullets:
                bullet.draw(self.screen)

            for explosion in self.explosions:
                explosion.draw(self.screen)

            self.level_manager.terrain_manager.draw(self.screen, "grass")

            enemies_remaining = self.level_manager.enemies_remaining + len(self.enemies)
            if self.player_tank:
                self.ui.draw_hud(self.screen, self.player_tank, self.current_level,
                                self.score, enemies_remaining)

        elif self.state == STATE_PAUSED:
            self.level_manager.terrain_manager.draw(self.screen, "ground")
            if self.player_tank:
                self.player_tank.draw(self.screen)
            for enemy in self.enemies:
                enemy.draw(self.screen)
            self.ui.draw_pause_menu(self.screen)

        elif self.state == STATE_GAME_OVER:
            self.ui.draw_game_over(self.screen, self.score)

        elif self.state == STATE_LEVEL_COMPLETE:
            self.level_manager.terrain_manager.draw(self.screen, "ground")
            if self.player_tank:
                self.player_tank.draw(self.screen)
            self.ui.draw_level_complete(self.screen, self.current_level)

        elif self.state == STATE_VICTORY:
            self.ui.draw_victory(self.screen, self.score)

        pygame.display.flip()

    def run(self):
        """运行游戏主循环"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


# 导入关卡地图用于检查通关
from src.level import LEVEL_MAPS
