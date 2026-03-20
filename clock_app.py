import time
import drivers

DIGITS = {
    '0': [0x3, 0x3, 0x3, 0x3, 0x3],
    '1': [0x1, 0x1, 0x1, 0x1, 0x1],
    '2': [0x3, 0x1, 0x3, 0x2, 0x3],
    '3': [0x3, 0x1, 0x3, 0x1, 0x3],
    '4': [0x3, 0x3, 0x3, 0x1, 0x1],
    '5': [0x3, 0x2, 0x3, 0x1, 0x3],
    '6': [0x3, 0x2, 0x3, 0x3, 0x3],
    '7': [0x3, 0x1, 0x1, 0x1, 0x1],
    '8': [0x3, 0x3, 0x3, 0x3, 0x3],
    '9': [0x3, 0x3, 0x3, 0x1, 0x1],
    ':': [0x0, 0x1, 0x0, 0x1, 0x0]
}

def draw_char(char, start_x, start_y, color):
    bitmap = DIGITS.get(char, [0]*5)
    char_width = 1 if char == ':' else 2
    for row in range(5):
        for col in range(char_width):
            if (bitmap[row] >> (char_width - 1 - col)) & 1:
                drivers.set_pixel(start_x + col, start_y + row, color)
    return char_width

def update():
    current_time = time.strftime("%H:%M:%S")
    drivers.fill((0, 0, 0))

    x_offset = 1
    y_offset = 2

    for char in current_time:
        color = (0, 255, 255) if char != ':' else (255, 255, 0)
        width = draw_char(char, x_offset, y_offset, color)
        x_offset += width + 1

    drivers.refresh()
