#!/usr/bin/env python3
"""
坦克大战游戏入口
Tank Battle Game - Main Entry Point
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.game import Game


def main():
    """主函数"""
    print("=" * 50)
    print("     坦克大战 - Battle City")
    print("=" * 50)
    print()
    print("正在启动游戏...")
    print()

    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"游戏启动失败：{e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
