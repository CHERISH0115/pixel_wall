import random
import drivers

class SnakeGame:
    def __init__(self):
        self.reset()

    def reset(self):
        self.snake = [(5, 3), (4, 3), (3, 3)]
        self.direction = (1, 0)
        self.food = self.gen_food()
        self.alive = True
        self.score = 0

    def gen_food(self):
        empty = [(x, y) for x in range(23) for y in range(9) if (x, y) not in self.snake]
        if not empty:
            return (0, 0)
        return random.choice(empty)

    def set_direction(self, new_dir):
        """仅更新方向，不移动。避免按键与定时器重复移动。"""
        if self.alive and not (
            new_dir[0] == -self.direction[0] and new_dir[1] == -self.direction[1]
        ):
            self.direction = new_dir

    def step(self):
        """按当前方向移动一格。"""
        if not self.alive:
            return

        head = self.snake[0]
        next_pos = (head[0] + self.direction[0], head[1] + self.direction[1])

        if not (0 <= next_pos[0] < 23 and 0 <= next_pos[1] < 9) or next_pos in self.snake:
            self.alive = False
            return

        self.snake.insert(0, next_pos)
        if next_pos == self.food:
            self.score += 1
            self.food = self.gen_food()
        else:
            self.snake.pop()

    def draw(self):
        drivers.fill((0, 0, 0))
        if self.alive:
            drivers.set_pixel(self.food[0], self.food[1], (255, 0, 0))
            for i, (x, y) in enumerate(self.snake):
                color = (0, 255, 0) if i > 0 else (200, 255, 200)
                drivers.set_pixel(x, y, color)
        else:
            for x in range(23):
                for y in range(9):
                    drivers.set_pixel(x, y, (255, 0, 0))
        drivers.refresh()
