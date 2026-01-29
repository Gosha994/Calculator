import arcade
import random
from pyglet.event import EVENT_HANDLE_STATE


# Константы, необходимые при запуске напрямую из пай файла
# Загружаем константы
with open("setup") as file:
    setting = file.readlines()
    SAVES = {}
    for elem in setting:
        SAVES[f"{elem.split(" = ")[0]}"] = elem.split(" = ")[1]

SIZE = int(SAVES["SIZE"])
DIFFICULTY = int(SAVES["DIFFICULTY"])


# Еда
class Food(arcade.Sprite):
    def __init__(self, window, x, y):
        super().__init__(":resources:/images/tiles/mushroomRed.png")
        self.cell_size = window.cell_size
        self.window = window
        self.width, self.height = self.cell_size * SIZE, self.cell_size * SIZE

        self.x, self.y = x, y
        self.center_x, self.center_y = self.cell_size * (0.5 + x), self.cell_size * (0.5 + y)

    def update(self, delta_time: float = 1 / 60, *args, **kwargs):
        if self.window.grid[self.y][self.x] == -1:
            self.kill()
            self.window.make_food()


# Змейка (а точнее секторы змейки)
class Snake(arcade.Sprite):
    def __init__(self, window, x, y, direction):
        super().__init__(window.textures[0])
        self.cell_size = window.cell_size
        self.window = window
        self.width, self.height = self.cell_size * SIZE, self.cell_size * SIZE
        self.angle = direction

        self.x, self.y = x, y
        self.window.grid[self.y][self.x] = -1
        self.center_x, self.center_y = self.cell_size * (0.5 + x), self.cell_size * (0.5 + y)

        self.len_num = 0

    def update(self, delta_time: float = 1 / 60, *args, **kwargs):
        self.len_num += 1

        if self.len_num == self.window.snake_length:
            self.window.grid[self.y][self.x] = 0
            self.kill()
        else:
            self.texture = arcade.load_texture(self.window.textures[self.len_num % 2 + 1])


class Snakulator(arcade.Window):
    def __init__(self):
        super().__init__(round(550 * SIZE), round(550 * SIZE), "Snakulator")
        self.textures = {0: ":resources:/images/tiles/grassMid.png", 1: ":resources:/images/tiles/grassCenter.png",
                         2: ":resources:/images/tiles/grassCenter.png"}
        self.keys_to_degrees = {100: 90, 65363: 90, 119: 0, 65362: 0, 97: 270, 65361: 270, 115: 180, 65364: 180}
        self.degrees_to_direction = {0: (0, 1), 90: (1, 0), 180: (0, -1), 270: (-1, 0)}

        self.cell_size = 50 * SIZE
        self.rows = int(self.height // self.cell_size)
        self.cols = int(self.width // self.cell_size)

        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        self.food_power = 1

        self.snake_length = 3
        self.snake_x, self.snake_y = 0, 5
        self.snake_direction = 90
        self.last_direction = 90

        self.sprites = arcade.SpriteList()

        self.move_timer = 0

    def on_key_press(self, symbol: int, modifiers: int) -> EVENT_HANDLE_STATE:
        if symbol in self.keys_to_degrees:
            direction = self.keys_to_degrees[symbol]
            if direction != (self.last_direction + 180) % 360:
                self.snake_direction = direction

    def setup(self):
        self.food_power = 1

        self.snake_length = 4
        self.snake_x, self.snake_y = 0, 5
        self.snake_direction = 90

        for sprite in self.sprites:
            sprite.kill()

        self.sprites.clear()

        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        snake = Snake(self, 0, 5, 90)
        self.sprites.append(snake)

        for i in range(3):
            self.make_food()

    def on_draw(self) -> EVENT_HANDLE_STATE:
        self.clear()
        arcade.draw_rect_filled(arcade.XYWH(self.width / 2, self.height / 2, self.width, self.height),
                                arcade.color.APPLE_GREEN)
        for row in range(self.rows):
            for col in range(row % 2, self.cols, 2):
                x = self.cell_size * (0.5 + col)
                y = self.cell_size * (0.5 + row)
                arcade.draw_rect_filled(arcade.XYWH(x, y, self.cell_size, self.cell_size),
                                        arcade.color.ANDROID_GREEN)

        self.sprites.draw()

    def on_update(self, delta_time: float):
        self.move_timer += delta_time
        if self.move_timer >= 0.5:
            self.move_timer = 0

            dx, dy = self.degrees_to_direction[self.snake_direction]
            self.last_direction = self.snake_direction
            self.snake_x += dx
            self.snake_y += dy

            self.sprites.update()

            if (self.snake_x in [-1, self.cols] or self.snake_y in [-1, self.cols] or
                    self.grid[self.snake_y][self.snake_x] == -1):
                self.setup()
                pass
            elif self.grid[self.snake_y][self.snake_x] >= 1:
                self.snake_length += self.grid[self.snake_y][self.snake_x]

            snake = Snake(self, self.snake_x, self.snake_y, self.snake_direction)
            self.sprites.append(snake)

    def make_food(self):
        # Список всех пустых клеток
        free_space = [(x, y) for x in range(self.cols) for y in range(self.rows) if self.grid[y][x] == 0]
        x, y = random.choice(free_space)

        food = Food(self, x, y)
        self.sprites.append(food)
        self.grid[y][x] = self.food_power


if __name__ == "__main__":
    game = Snakulator()
    game.setup()
    arcade.run()
