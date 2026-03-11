"""
UI 系统模块
处理游戏界面渲染
"""

import pygame
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    FONT_SIZE_LARGE, FONT_SIZE_MEDIUM, FONT_SIZE_SMALL,
    BLACK, WHITE, RED, GREEN, BLUE, GRAY,
    STATE_MENU, STATE_PLAYING, STATE_PAUSED, STATE_GAME_OVER, STATE_LEVEL_COMPLETE, STATE_VICTORY
)


class UI:
    """用户界面类"""

    def __init__(self):
        # 初始化字体
        pygame.font.init()
        try:
            # 尝试使用中文字体
            self.font_large = pygame.font.Font("simhei.ttf", FONT_SIZE_LARGE)
            self.font_medium = pygame.font.Font("simhei.ttf", FONT_SIZE_MEDIUM)
            self.font_small = pygame.font.Font("simhei.ttf", FONT_SIZE_SMALL)
        except:
            #  fallback 到默认字体
            self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE + 8)
            self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM + 8)
            self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL + 8)

        self.menu_options = ["开始游戏", "双人模式", "帮助", "退出"]
        self.selected_option = 0

    def draw_menu(self, screen):
        """绘制主菜单"""
        # 背景
        screen.fill(BLACK)

        # 标题
        title = self.font_large.render("坦克大战", True, GREEN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title, title_rect)

        # 副标题
        subtitle = self.font_small.render("BATTLE CITY", True, GRAY)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(subtitle, subtitle_rect)

        # 菜单选项
        for i, option in enumerate(self.menu_options):
            color = GREEN if i == self.selected_option else WHITE
            text = self.font_medium.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 250 + i * 60))
            screen.blit(text, text_rect)

            # 选中指示器
            if i == self.selected_option:
                indicator = self.font_medium.render("▶ ", True, GREEN)
                screen.blit(indicator, (text_rect.left - 40, text_rect.top))

        # 底部信息
        info = self.font_small.render("使用方向键选择，按 Enter 确认", True, GRAY)
        info_rect = info.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(info, info_rect)

    def draw_hud(self, screen, player_tank, level, score, enemies_remaining):
        """绘制游戏 HUD"""
        # 顶部信息栏背景
        info_bg = pygame.Rect(0, 0, SCREEN_WIDTH, 40)
        pygame.draw.rect(screen, (30, 30, 30), info_bg)

        # 关卡信息
        level_text = self.font_small.render(f"关卡：{level}", True, WHITE)
        screen.blit(level_text, (20, 5))

        # 得分
        score_text = self.font_small.render(f"得分：{score}", True, WHITE)
        screen.blit(score_text, (200, 5))

        # 生命
        lives_text = self.font_small.render(f"生命：{player_tank.lives}", True, WHITE)
        screen.blit(lives_text, (400, 5))

        # 敌人剩余
        enemy_text = self.font_small.render(f"敌人：{enemies_remaining}", True, RED)
        screen.blit(enemy_text, (600, 5))

        # 生命值条
        if player_tank.max_health > 1:
            health_bar_width = 100
            health_bar_height = 10
            health_ratio = player_tank.health / player_tank.max_health

            health_bg = pygame.Rect(SCREEN_WIDTH - 120, 10, health_bar_width, health_bar_height)
            pygame.draw.rect(screen, GRAY, health_bg)

            health_fg = pygame.Rect(SCREEN_WIDTH - 120, 10,
                                    int(health_bar_width * health_ratio), health_bar_height)
            pygame.draw.rect(screen, GREEN, health_fg)
            pygame.draw.rect(screen, WHITE, health_bg, 1)

    def draw_pause_menu(self, screen):
        """绘制暂停菜单"""
        # 半透明遮罩
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        # 暂停文字
        pause_text = self.font_large.render("游戏暂停", True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(pause_text, pause_rect)

        # 提示
        resume_text = self.font_medium.render("按 P 继续游戏", True, GRAY)
        resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        screen.blit(resume_text, resume_rect)

        quit_text = self.font_small.render("按 ESC 退出到菜单", True, GRAY)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
        screen.blit(quit_text, quit_rect)

    def draw_game_over(self, screen, score):
        """绘制游戏结束界面"""
        # 背景
        screen.fill(BLACK)

        # 游戏结束
        game_over_text = self.font_large.render("游戏结束", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(game_over_text, game_over_rect)

        # 最终得分
        score_text = self.font_medium.render(f"最终得分：{score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(score_text, score_rect)

        # 提示
        restart_text = self.font_small.render("按 Enter 重新开始", True, GRAY)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        screen.blit(restart_text, restart_rect)

        menu_text = self.font_small.render("按 ESC 返回菜单", True, GRAY)
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
        screen.blit(menu_text, menu_rect)

    def draw_level_complete(self, screen, level):
        """绘制关卡完成界面"""
        # 半透明遮罩
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        # 关卡完成
        complete_text = self.font_large.render(f"第 {level} 关 完成!", True, GREEN)
        complete_rect = complete_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(complete_text, complete_rect)

        # 提示
        next_text = self.font_medium.render("按 Enter 进入下一关", True, WHITE)
        next_rect = next_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        screen.blit(next_text, next_rect)

    def draw_victory(self, screen, score):
        """绘制胜利界面"""
        # 背景
        screen.fill(BLACK)

        # 胜利文字
        victory_text = self.font_large.render("恭喜通关!", True, GREEN)
        victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(victory_text, victory_rect)

        # 最终得分
        score_text = self.font_medium.render(f"最终得分：{score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(score_text, score_rect)

        # 提示
        restart_text = self.font_small.render("按 Enter 重新开始", True, GRAY)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        screen.blit(restart_text, restart_rect)

    def draw_help(self, screen):
        """绘制帮助界面"""
        screen.fill(BLACK)

        # 标题
        help_title = self.font_large.render("游戏帮助", True, WHITE)
        help_title_rect = help_title.get_rect(center=(SCREEN_WIDTH // 2, 80))
        screen.blit(help_title, help_title_rect)

        # 操作说明
        controls = [
            "操作说明:",
            "W / ↑ - 向上移动",
            "S / ↓ - 向下移动",
            "A / ← - 向左移动",
            "D / → - 向右移动",
            "J / 空格 - 射击",
            "P / ESC - 暂停游戏",
            "",
            "游戏目标:",
            "消灭所有敌人，保护基地!",
            "",
            "按 ESC 返回菜单"
        ]

        for i, line in enumerate(controls):
            color = GREEN if "操作" in line or "游戏" in line else WHITE
            text = self.font_small.render(line, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 180 + i * 35))
            screen.blit(text, text_rect)

    def draw_message(self, screen, message, duration=60):
        """绘制临时消息"""
        text = self.font_medium.render(message, True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        screen.blit(text, text_rect)


class Explosion:
    """爆炸特效类"""

    def __init__(self, x, y, size="medium"):
        self.x = x
        self.y = y
        self.frame = 0
        self.max_frames = 20

        if size == "small":
            self.max_radius = 20
        elif size == "large":
            self.max_radius = 50
        else:
            self.max_radius = 35

        self.active = True

    def update(self):
        """更新爆炸帧"""
        self.frame += 1
        if self.frame >= self.max_frames:
            self.active = False

    def draw(self, screen):
        """绘制爆炸效果"""
        progress = self.frame / self.max_frames

        # 爆炸半径先扩大后缩小
        if progress < 0.5:
            radius = int(self.max_radius * (progress * 2))
        else:
            radius = int(self.max_radius * (1 - (progress - 0.5) * 2))

        # 外层红色
        pygame.draw.circle(screen, (255, 100, 0), (int(self.x), int(self.y)), radius)
        # 内层黄色
        inner_radius = int(radius * 0.6)
        pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), inner_radius)
        # 中心白色
        center_radius = int(radius * 0.3)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), center_radius)
