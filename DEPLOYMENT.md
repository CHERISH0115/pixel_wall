# Pixel Wall 像素墙 - 从零部署教程

本文档提供从零开始部署 Pixel Wall 项目的完整步骤，包括硬件准备、系统安装、环境配置和运行。

---

## 目录

1. [硬件清单](#1-硬件清单)
2. [NeoPixel 接线](#2-neopixel-接线)
3. [树莓派系统安装](#3-树莓派系统安装)
4. [首次启动与基础配置](#4-首次启动与基础配置)
5. [启用 GPIO 与依赖安装](#5-启用-gpio-与依赖安装)
6. [项目部署](#6-项目部署)
7. [运行程序](#7-运行程序)
8. [Web 遥控访问](#8-web-遥控访问)
9. [PS4 手柄连接（可选）](#9-ps4-手柄连接可选)
10. [开机自启动](#10-开机自启动)
11. [无树莓派模拟测试](#11-无树莓派模拟测试)
12. [常见问题与排错](#12-常见问题与排错)

---

## 1. 硬件清单

| 物品 | 规格说明 | 数量 |
|------|----------|------|
| 树莓派 | Raspberry Pi 3/4/5（推荐 4 或 5） | 1 |
| microSD 卡 | 32GB 及以上，Class 10 | 1 |
| NeoPixel LED 矩阵 | WS2812B，逻辑 24×7（物理 LED 数 = 168 × LEDS_PER_GRID），或兼容 WS2812 的矩阵 | 1 |
| 电源 | 5V 3A 以上（建议 5V 5A，LED 全亮时电流较大） | 1 |
| 数据线 | 杜邦线或排线，连接树莓派 GPIO 与 NeoPixel | 若干 |
| 电源线 | 为 NeoPixel 供电（需匹配矩阵接口） | 若干 |
| 网线 / WiFi | 树莓派联网用 | 1 / 内置 |
| PS4 手柄（可选） | 原装 DualShock 4，USB 或蓝牙 | 1 |

### NeoPixel 规格说明

- **型号**：WS2812B 或兼容（如 SK6812、APA102 需改驱动）
- **排列**：24 列 × 7 行，蛇形排布（偶数行从左往右，奇数行从右往左）
- **电压**：5V
- **数据接口**：单线串行（DIN）

本项目支持一个逻辑格子对应多颗物理 LED（默认 `LEDS_PER_GRID = 2`，即 336 颗）。若你的硬件是 168 颗，请将 `LEDS_PER_GRID` 改为 1。

若你的矩阵尺寸或排布不同，需修改 `drivers.py` 中的 `WIDTH`、`HEIGHT`、`LEDS_PER_GRID` 和 `set_pixel` 的映射逻辑。

---

## 2. NeoPixel 接线

### 2.1 接口说明

NeoPixel 矩阵一般有 3～4 个接口：

| 标号 | 含义 | 接法 |
|------|------|------|
| VCC / +5V | 电源正极 | 接 5V 电源正极 |
| GND | 地 | 接电源负极，并与树莓派 GND 共地 |
| DIN / DATA / IN | 数据输入 | 接树莓派 **GPIO 18** |
| DOUT（部分型号） | 数据输出 | 仅级联时使用，此处不接 |

> 重要：树莓派 GND 必须与 NeoPixel 电源的 GND 连接，否则数据不稳定。

### 2.2 接线示意

```
树莓派 GPIO 18 ────────────── NeoPixel DIN
树莓派 GND    ────────────── NeoPixel GND
5V 电源 +5V  ────────────── NeoPixel VCC
5V 电源 GND  ────────────── NeoPixel GND（并与树莓派 GND 相连）
```

### 2.3 供电建议

- **小功率测试**：可用树莓派 5V 和 GND 给少量 LED 供电（不推荐长时间全亮）。
- **正式使用**：建议外接 5V 3A～5A 独立电源给 NeoPixel 供电，树莓派仅提供数据信号和共地。

### 2.4 电平匹配（可选）

部分 NeoPixel 对 3.3V 信号不敏感，若出现闪烁、花屏，可在 DIN 与 GPIO 18 之间加 1 个 330Ω～470Ω 电阻，或使用 74HCT245 等电平转换芯片。

---

## 3. 树莓派系统安装

### 3.1 下载 Raspberry Pi Imager

1. 访问 [https://www.raspberrypi.com/software/](https://www.raspberrypi.com/software/)
2. 下载并安装 **Raspberry Pi Imager**
3. 将 microSD 卡插入电脑读卡器

### 3.2 烧录系统

1. 打开 Raspberry Pi Imager
2. 选择操作系统：**Raspberry Pi OS (64-bit)**，建议选带桌面的版本
3. 选择存储设备：你的 microSD 卡
4. 点击 **设置**（齿轮图标）进行预配置：
   - 设置主机名（如 `pixelwall`）
   - 启用 SSH，使用密码认证或密钥
   - 设置用户名和密码
   - 配置 WiFi（SSID 与密码）
   - 设置时区（如 Asia/Shanghai）
   - 勾选「在首次启动时运行»（完成设置向导）
5. 点击 **保存**，再点击 **下一步** 开始烧录
6. 烧录完成后弹出 microSD 卡，插入树莓派

---

## 4. 首次启动与基础配置

1. 连接 HDMI、键盘、鼠标、电源，上电启动
2. 按提示完成语言、时区、用户、密码等设置
3. 更新系统（可选，建议执行）：
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```
4. 如需远程 SSH，确保树莓派与电脑在同一网络，使用：
   ```bash
   ssh 用户名@pixelwall.local
   ```
   或 `ssh 用户名@树莓派IP`

---

## 5. 启用 GPIO 与依赖安装

### 5.1 启用 SPI（NeoPixel 所需）

```bash
sudo raspi-config
```

依次选择：

- **Interface Options** → **SPI** → **Yes**
- 完成后选择 **Finish**，按提示重启

### 5.2 安装系统依赖

```bash
sudo apt install -y python3-pip python3-venv
```

### 5.3 创建虚拟环境（推荐）

```bash
cd ~
mkdir -p projects
cd projects
git clone <你的项目地址> pixel_wall
# 若没有 git，可手动上传项目文件夹
cd pixel_wall

python3 -m venv venv
source venv/bin/activate
```

> Windows 用户：虚拟环境激活命令为 `venv\Scripts\activate`，但本项目需在树莓派上运行。

### 5.4 安装 Python 依赖

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

若使用 `adafruit-blinka` 出现兼容性问题，可尝试：

```bash
pip install adafruit-blinka
pip install adafruit-circuitpython-neopixel
pip install RPi.GPIO
```

### 5.5 权限配置

使用 GPIO 需要相应权限：

```bash
sudo usermod -aG gpio $USER
```

修改后需重新登录或重启才能生效。

---

## 6. 项目部署

### 6.1 目录结构确认

确保项目目录结构如下：

```
pixel_wall/
├── main.py
├── drivers.py
├── clock_app.py
├── snake_app.py
├── requirements.txt
├── requirements-mock.txt
├── run.bat
└── templates/
    └── index.html
```

### 6.2 修改引脚（如需要）

默认使用 **GPIO 18**。若使用其他引脚，编辑 `drivers.py`：

```python
PIXEL_PIN = board.D18  # 改为 board.D12 等
```

### 6.3 修改矩阵尺寸（如需要）

若矩阵不是 24×7，修改 `drivers.py`：

```python
WIDTH = 24
HEIGHT = 7
```

同时需修改 `snake_app.py`、`clock_app.py` 中对应尺寸与坐标。

### 6.4 修改每格 LED 数量（LEDS_PER_GRID）

如果你的硬件是“一个逻辑像素格子对应多颗物理 LED”（例如每格 2 颗），可通过 `drivers.py` 调整：

```python
LEDS_PER_GRID = 2  # 每个格子的物理 LED 数量
```

注意事项：

- **物理 LED 总数**：`WIDTH × HEIGHT × LEDS_PER_GRID`，需与你实际灯珠数量一致  
  例如 24×7：`168 × LEDS_PER_GRID`，`LEDS_PER_GRID=2` 则为 336 颗
- **布线要求**：同一格子的多颗 LED 在物理序列中必须连续，且整墙按蛇形（Z 字形）逐行连接；否则会出现错位显示
- **供电**：LED 数量翻倍意味着最大电流也近似翻倍，请按 `hardware.md` 的供电建议选电源

---

## 7. 运行程序

### 7.1 激活虚拟环境并启动

```bash
cd ~/projects/pixel_wall
source venv/bin/activate
python main.py
```

### 7.2 正常输出

- 有 NeoPixel 硬件时：无特殊提示，LED 应显示时钟
- 无 NeoPixel 时：输出 `硬件未就绪，使用模拟模式（仅 Web 与逻辑可测）`，模拟模式下默认进入贪吃蛇并自动打开浏览器

### 7.3 停止程序

按 `Ctrl+C` 结束，程序会清空 LED 后退出。

### 7.4 Windows 快捷启动

双击 `run.bat` 即可启动。若存在 `.venv` 虚拟环境会自动激活。

---

## 8. Web 遥控访问

### 8.1 获取树莓派 IP

```bash
hostname -I
```

或连接显示器时在桌面右上角网络图标处查看。

### 8.2 打开遥控页面

在同一局域网内的手机或电脑浏览器访问：

```
http://<树莓派IP>:5000
```

例如：`http://192.168.1.100:5000`

### 8.3 操作说明

| 按钮 | 功能 |
|------|------|
| ▲▼◀▶ | 方向键，贪吃蛇模式下控制蛇头方向 |
| 切换模式 | 时钟 ⇄ 贪吃蛇 |
| 重置游戏 | 贪吃蛇模式下重新开始 |

支持键盘方向键和触摸操作。

### 8.4 像素预览

页面顶部提供 **像素预览** 区域，与实体 LED 矩阵同步显示。若显示「已连接」则表示预览正常；若显示「无法连接」，请确认 `main.py` 已运行。

---

## 9. PS4 手柄连接（可选）

### 9.1 USB 连接

1. 用 USB 线连接 PS4 手柄到树莓派
2. 检查是否识别：
   ```bash
   ls /dev/input/js*
   ```
   应能看到 `/dev/input/js0` 等设备

### 9.2 蓝牙连接

1. 安装蓝牙工具（若无）：
   ```bash
   sudo apt install -y bluez pi-bluetooth
   ```
2. 重启后进入蓝牙配置：
   ```bash
   bluetoothctl
   ```
3. 在 `bluetoothctl` 中执行：
   ```
   power on
   agent on
   default-agent
   scan on
   ```
4. 手柄进入配对模式（长按 Share+PS 约 3 秒，指示灯快闪）
5. 记下显示的 MAC 地址，例如 `XX:XX:XX:XX:XX:XX`
6. 配对并信任：
   ```
   pair XX:XX:XX:XX:XX:XX
   trust XX:XX:XX:XX:XX:XX
   connect XX:XX:XX:XX:XX:XX
   quit
   ```
7. 若蓝牙手柄映射到 `/dev/input/js0` 以外的设备，可修改 `main.py` 中 `interface` 参数

### 9.3 手柄按键映射

| 按键 | 功能 |
|------|------|
| 方向键 | 控制蛇头方向 |
| X | 切换模式 |
| Options | 重置游戏 |

---

## 10. 开机自启动

### 10.1 创建 systemd 服务

```bash
sudo nano /etc/systemd/system/pixelwall.service
```

写入（注意替换实际路径和用户名）：

```ini
[Unit]
Description=Pixel Wall LED Matrix Controller
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/projects/pixel_wall
ExecStart=/home/pi/projects/pixel_wall/venv/bin/python main.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

保存后执行：

```bash
sudo systemctl daemon-reload
sudo systemctl enable pixelwall.service
sudo systemctl start pixelwall.service
```

### 10.2 常用命令

```bash
sudo systemctl status pixelwall   # 查看状态
sudo systemctl stop pixelwall     # 停止
sudo systemctl start pixelwall    # 启动
sudo journalctl -u pixelwall -f   # 查看日志
```

---

## 11. 无树莓派模拟测试

在没有树莓派和 NeoPixel 的情况下，可在 Windows / Mac 上通过浏览器玩贪吃蛇并查看像素预览。

### 11.1 安装依赖

```bash
pip install -r requirements-mock.txt
```

或直接 `pip install flask`（requirements-mock.txt 仅包含 flask）。

### 11.2 运行

```bash
python main.py
```

或双击 `run.bat`（Windows）。

### 11.3 使用说明

- 程序会自动打开默认浏览器；若未打开，请手动访问 `http://localhost:5000`
- 模拟模式下默认进入贪吃蛇，可直接用方向键或页面按钮游玩
- 页面顶部像素预览会同步显示游戏画面
- PS4 手柄在非 Linux 环境下不可用，仅支持 Web 遥控

---

## 12. 常见问题与排错

### 12.1 LED 不亮或花屏

- 检查 VCC、GND、DIN 接线是否正确
- 确认树莓派 GND 与 NeoPixel 电源 GND 已共地
- 检查 `drivers.py` 中 `ORDER` 是否为 `neopixel.GRB`（部分灯带为 GRB，需根据实际型号调整）
- 尝试降低亮度：`brightness=0.2`

### 12.2 提示 "Permission denied" 或无法访问 GPIO

```bash
sudo usermod -aG gpio $USER
```

然后重新登录或重启。

### 12.3 提示 "No module named 'board'" 或 "No module named 'neopixel'"

确认已在虚拟环境中安装依赖：

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 12.4 PS4 手柄未检测到

- USB：确认 `ls /dev/input/js*` 有输出
- 蓝牙：确认 `bluetoothctl` 中已 connect，并检查 `js0` 等设备是否存在
- 若使用 ds4drv，可尝试 `connecting_using_ds4drv=True` 并先启动 ds4drv

### 12.5 Web 页面无法访问

- 确认防火墙未阻止 5000 端口：`sudo ufw allow 5000`（若使用 ufw）
- 确认手机/电脑与树莓派在同一局域网
- 使用 `http://` 而非 `https://`

### 12.6 在 Windows / Mac 上运行（模拟模式）

在 PC 上运行会进入模拟模式：Web 遥控和贪吃蛇逻辑可完整测试，浏览器像素预览同步显示，LED 无输出。使用 `pip install -r requirements-mock.txt` 安装依赖即可。详见 [11. 无树莓派模拟测试](#11-无树莓派模拟测试)。

### 12.7 浏览器像素预览不显示

- 确认程序已运行，预览下方显示「已连接」
- 若显示「无法连接」，检查 `main.py` 是否运行，端口 5000 是否被占用
- 模拟模式下会自动打开浏览器，亦可手动访问 `http://localhost:5000`

---

## 附录：快速命令汇总

```bash
# 树莓派：进入项目并运行
cd ~/projects/pixel_wall
source venv/bin/activate
python main.py

# 无树莓派：PC 模拟测试
pip install -r requirements-mock.txt
python main.py

# 查看树莓派 IP
hostname -I

# 开机自启
sudo systemctl enable pixelwall
sudo systemctl start pixelwall
```

---

部署过程中遇到问题，可结合上述排错章节逐项检查；若硬件或矩阵型号特殊，需要对照 `drivers.py` 做相应修改。
