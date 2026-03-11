# 坦克大战 - Battle City

经典的坦克大战游戏，使用 Python 和 Pygame 开发。

## 游戏特性

- 🎮 经典坦克大战玩法
- 🎨 高清画面 (1280x720)
- 🎯 10 个精心设计的关卡
- 👥 支持双人合作模式
- 💥 丰富的敌人类型（普通/快速/重装/Boss）
- 🔊 音效和背景音乐支持

## 操作说明

| 动作 | 按键 |
|------|------|
| 上移 | W / ↑ |
| 下移 | S / ↓ |
| 左移 | A / ← |
| 右移 | D / → |
| 射击 | J / 空格 |
| 暂停 | P / ESC |

## 安装

### 环境要求

- Python 3.11+
- pygame 2.5+

### 安装步骤

```bash
# 安装依赖
pip install -r requirements.txt

# 运行游戏
python main.py
```

## 打包成可执行文件

```bash
# 安装 PyInstaller
pip install pyinstaller

# 打包
pyinstaller --onefile --name "坦克大战" --icon=assets/images/icon.ico main.py
```

## 开发

### 运行测试

```bash
pytest tests/ -v
```

### 项目结构

```
tank_battle/
├── main.py              # 游戏入口
├── config.py            # 游戏配置
├── requirements.txt     # 依赖包
├── src/
│   ├── game.py          # 游戏主循环
│   ├── entity.py        # 实体基类
│   ├── tank.py          # 坦克类
│   ├── bullet.py        # 子弹类
│   ├── terrain.py       # 地形类
│   ├── collision.py     # 碰撞检测
│   ├── level.py         # 关卡管理
│   └── ui.py            # UI 渲染
├── tests/
│   └── test_game.py     # 单元测试
└── assets/
    ├── images/          # 图片资源
    └── sounds/          # 音效资源
```

## 许可证

MIT License
