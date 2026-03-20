# Pixel Wall 像素墙

基于树莓派 + NeoPixel LED 矩阵的互动显示项目，支持**时钟显示**和**贪吃蛇游戏**，可通过 **Web 遥控** 或 **PS4 手柄** 控制。

---

## 功能特性

- **时钟模式**：24×7 LED 矩阵显示 HH:MM:SS
- **贪吃蛇模式**：在像素墙上玩贪吃蛇
- **Web 遥控**：手机/电脑浏览器控制，含**像素预览**（与实体 LED 同步）
- **PS4 手柄**：方向键、X 切换模式、Options 重置（需 Linux）
- **模拟模式**：无树莓派时可在 PC 上通过浏览器玩贪吃蛇测试
- **每格多灯支持**：支持 1 个逻辑像素格对应多颗物理 LED（见 `drivers.py` 的 `LEDS_PER_GRID`）

---

## 快速开始

### 有树莓派 + NeoPixel

```bash
pip install -r requirements.txt
python main.py
```

浏览器访问 `http://树莓派IP:5000`

### 无树莓派（PC 测试）

```bash
pip install -r requirements-mock.txt
python main.py
```

程序会自动打开浏览器，或手动访问 `http://localhost:5000`

### Windows 一键运行

双击 `run.bat`

---

## 项目结构

```
pixel_wall/
├── main.py              主程序
├── drivers.py           LED 驱动（含模拟模式）
├── clock_app.py         时钟显示
├── snake_app.py         贪吃蛇游戏
├── requirements.txt     树莓派依赖
├── requirements-mock.txt 无硬件测试依赖
├── run.bat              Windows 一键启动
├── README.md            本文件
├── DEPLOYMENT.md        完整部署教程
├── hardware.md          硬件连接指南
├── readme.txt           文件说明
└── templates/
    └── index.html       Web 遥控 + 像素预览
```

---

## 文档索引

| 文档 | 内容 |
|------|------|
| [DEPLOYMENT.md](DEPLOYMENT.md) | 从零部署：硬件、系统、依赖、运行、模拟测试、排错 |
| [hardware.md](hardware.md) | 硬件连接：接线、供电、GPIO、排错 |
| [readme.txt](readme.txt) | 各文件功能说明 |

---

## 控制说明

| 操作 | Web | PS4 手柄 |
|------|-----|----------|
| 控制方向 | ▲▼◀▶ 或键盘方向键 | 方向键 |
| 切换模式 | 切换模式 | X |
| 重置游戏 | 重置游戏 | Options |

---

## 依赖说明

- **requirements.txt**：树莓派完整依赖（Flask、NeoPixel、PS4 等，含平台条件）
- **requirements-mock.txt**：仅 Flask，用于无硬件环境测试

---

## 显示参数（重要）

- **逻辑分辨率**：固定为 24×7 个“格子”（时钟/贪吃蛇/Web 预览都按格子绘制）
- **物理 LED 数量**：由 `drivers.py` 中 `LEDS_PER_GRID` 决定  
  - `LEDS_PER_GRID = 1` → 168 颗 LED  
  - `LEDS_PER_GRID = 2` → 336 颗 LED（当前默认）
- **布线要求**：每个格子对应的多颗 LED 在物理序列中必须**连续**，并按**蛇形（Z 字形）**逐行连接（详见 `hardware.md` 第 7 节）
