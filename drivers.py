WIDTH = 23
HEIGHT = 9

# 每个逻辑格子的物理 LED 数量，便于后续按需调整
LEDS_PER_GRID = 2

# 物理 LED 总数 = 宽 × 高 × 每格 LED 数
NUM_PIXELS = WIDTH * HEIGHT * LEDS_PER_GRID
MOCK_MODE = False

# 软件缓冲区，用于 Web 预览（与 LED 同步）
display_buffer = [[(0, 0, 0)] * WIDTH for _ in range(HEIGHT)]

try:
    import board
    import neopixel

    PIXEL_PIN = board.D18
    ORDER = neopixel.GRB
    pixels = neopixel.NeoPixel(
        PIXEL_PIN,
        NUM_PIXELS,
        brightness=0.4,
        auto_write=False,
        pixel_order=ORDER,
    )
except (ImportError, NotImplementedError):
    MOCK_MODE = True
    pixels = type("MockPixels", (), {
        "fill": lambda self, c: None,
        "show": lambda self: None,
        "__setitem__": lambda self, i, c: None,
    })()
    print("硬件未就绪，使用模拟模式（仅 Web 与逻辑可测）")

def set_pixel(x, y, color):
    if not (0 <= x < WIDTH and 0 <= y < HEIGHT):
        return
    display_buffer[y][x] = tuple(color)
    # 逻辑索引（按蛇形排布）
    if y % 2 == 0:
        logical_index = (y * WIDTH) + x
    else:
        logical_index = (y * WIDTH) + (WIDTH - 1 - x)

    # 映射到物理索引：每个逻辑格子连续占用 LEDS_PER_GRID 颗 LED
    base = logical_index * LEDS_PER_GRID
    for i in range(LEDS_PER_GRID):
        idx = base + i
        if 0 <= idx < NUM_PIXELS:
            pixels[idx] = color

def refresh():
    pixels.show()

def fill(color):
    """填充整个矩阵，同时更新显示缓冲区。"""
    c = tuple(color)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            display_buffer[y][x] = c
    pixels.fill(color)

def clear():
    fill((0, 0, 0))
    refresh()

def get_display():
    """返回当前显示缓冲区的 JSON 可序列化格式，供 Web 预览使用。"""
    return [list(row) for row in display_buffer]
