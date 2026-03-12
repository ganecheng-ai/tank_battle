# 坦克大战 - Battle City

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.5+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
[![Build](https://github.com/ganecheng-ai/tank_battle/actions/workflows/build.yml/badge.svg)](https://github.com/ganecheng-ai/tank_battle/actions)

**一款使用 Python 和 Pygame 开发的经典坦克大战游戏**

[开始游戏](#安装) • [游戏截图](#游戏截图) • [操作说明](#操作说明) • [开发计划](#开发计划)

</div>

---

## 🎮 游戏简介

《坦克大战》（Battle City）是一款经典的街机坦克游戏。本项目使用 Python 和 Pygame 框架进行开发，重现了这一经典游戏的核心玩法，并加入了现代化的视觉效果。

### 游戏特色

- 🎨 **精美画面** - 高清分辨率 (1280x720)，精心绘制的坦克和地形
- 🎯 **10 个关卡** - 从简单到复杂，包含 Boss 关卡
- 👥 **双人合作** - 支持本地双人游戏
- 💥 **丰富敌人** - 普通坦克、快速坦克、重装坦克、Boss
- 🔊 **音效支持** - 背景音乐和音效
- 🇨🇳 **简体中文** - 完整的中文化界面

### 游戏类型

| 类型 | 说明 |
|------|------|
| 普通坦克 | 绿色，标准属性 |
| 快速坦克 | 橙色，移动速度快 |
| 重装坦克 | 灰色，防御高 |
| Boss 坦克 | 红色，血量厚，体型大 |

---

## 📦 安装

### 环境要求

- Python 3.11 或更高版本
- pygame 2.5 或更高版本

### 安装步骤

```bash
# 1. 克隆仓库
git clone git@github.com:ganecheng-ai/tank_battle.git
cd tank_battle

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行游戏
python main.py
```

### 打包成可执行文件

```bash
# 安装 PyInstaller
pip install pyinstaller

# 打包
pyinstaller --onefile --name "TankBattle" --console main.py
```

打包后的可执行文件位于 `dist/` 目录。

---

## 🎯 操作说明

### 玩家 1 控制

| 动作 | 按键 |
|------|------|
| 向上移动 | W / ↑ |
| 向下移动 | S / ↓ |
| 向左移动 | A / ← |
| 向右移动 | D / → |
| 射击 | J / 空格 |

### 玩家 2 控制（双人模式）

| 动作 | 按键 |
|------|------|
| 向上移动 | 数字键盘 8 |
| 向下移动 | 数字键盘 2 |
| 向左移动 | 数字键盘 4 |
| 向右移动 | 数字键盘 6 |
| 射击 | 数字键盘 0 / 右 Ctrl |

### 通用按键

| 动作 | 按键 |
|------|------|
| 暂停游戏 | P / ESC |
| 确认选择 | Enter |
| 返回菜单 | ESC |

---

## 🗺️ 关卡设计

游戏包含 10 个精心设计的关卡：

| 关卡 | 主题 | 特点 |
|------|------|------|
| 第 1 关 | 入门 | 简单地形，教学关卡 |
| 第 2 关 | 水域 | 河流障碍 |
| 第 3 关 | 钢板 | 金属障碍 |
| 第 4 关 | 草地 | 隐蔽地形 |
| 第 5 关 | 混合 | 综合地形 |
| 第 6-9 关 | 进阶 | 难度递增 |
| 第 10 关 | Boss | 最终决战 |

---

## 🏗️ 项目结构

```
tank_battle/
├── main.py              # 游戏入口
├── config.py            # 游戏配置
├── requirements.txt     # 依赖包
├── README.md            # 项目说明
├── plan.md              # 开发计划
├── prompt.md            # 开发指令
├── .github/
│   └── workflows/
│       └── build.yml    # GitHub Actions 配置
├── assets/              # 资源文件
│   ├── images/          # 图片资源
│   ├── sounds/          # 音效资源
│   └── fonts/           # 字体资源
├── src/                 # 源代码
│   ├── __init__.py
│   ├── game.py          # 游戏主循环
│   ├── entity.py        # 实体基类
│   ├── tank.py          # 坦克类
│   ├── bullet.py        # 子弹类
│   ├── terrain.py       # 地形类
│   ├── collision.py     # 碰撞检测
│   ├── level.py         # 关卡管理
│   └── ui.py            # UI 渲染
└── tests/               # 单元测试
    └── test_game.py
```

---

## 🧪 测试

运行单元测试：

```bash
pytest tests/ -v
```

当前测试状态：**36 个测试全部通过 ✅**

---

## 🚀 发布历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.2.0 | 2026-03 | 优化游戏画面和特效 |
| v1.1.0 | 2026-03 | 添加 macOS 构建支持 |
| v1.0.0 | 2026-03 | 初始发布版本 |

---

## 📋 开发计划

### 阶段 1：基础框架 ✅
- [x] 搭建项目结构
- [x] 实现游戏主循环
- [x] 实现基础输入处理
- [x] 创建配置系统

### 阶段 2：核心玩法 ✅
- [x] 实现坦克类（移动/旋转）
- [x] 实现子弹系统
- [x] 实现碰撞检测
- [x] 实现基础地形

### 阶段 3：游戏内容 ✅
- [x] 实现敌人 AI
- [x] 实现 10 个关卡设计
- [x] 实现 UI 界面（简体中文）
- [x] 添加音效
- [x] 中文字体集成

### 阶段 4：优化完善 ✅
- [x] 添加特效
- [x] 性能优化
- [x] Bug 修复
- [x] 打包发布（GitHub Actions 自动构建）

---

## 📸 游戏截图

游戏画面精美，包含：
- 精美的坦克设计（带履带纹理和炮塔）
- 多样化的地形（砖块/钢板/水域/草地/基地）
- 华丽的爆炸特效（多层粒子效果）
- 简洁明了的 UI 界面

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

---

<div align="center">

**🎮 享受游戏！Happy Gaming! 🎮**

</div>
