import arcade
import random
from pyglet.graphics import Batch
from arcade.particles import FadeParticle, Emitter, EmitBurst, EmitInterval, EmitMaintainCount, EternalParticle
from arcade.sound import Sound
from arcade.particles import make_burst_emitter

with open("setup") as file:
    setting = file.readlines()
    SAVES = {}
    for elem in setting:
        key, value = elem.strip().split(" = ")
        SAVES[key] = value

DIFFICULTY = int(SAVES["DIFFICULTY"])
SIZE = int(SAVES["SIZE"]) * 0.7

with open("inventory") as file:
    setting = file.readlines()
    INVENTORY = {}
    for elem in setting:
        key, value = elem.strip().split(" = ")
        INVENTORY[key] = value

BALANCE = int(INVENTORY["BALANCE"])

# Константы
CELL_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
SPARK_TEX = [
    arcade.make_soft_circle_texture(8, arcade.color.PASTEL_YELLOW),
    arcade.make_soft_circle_texture(8, arcade.color.PEACH),
    arcade.make_soft_circle_texture(8, arcade.color.BABY_BLUE),
    arcade.make_soft_circle_texture(8, arcade.color.ELECTRIC_CRIMSON),
]

# Фигуры тетриса (тетрамино)
SHAPES = [
    [[1, 1, 1, 1]],  # I

    [[1, 1, 1],  # T
     [0, 1, 0]],

    [[1, 1, 1],  # L
     [1, 0, 0]],

    [[1, 1, 1],  # J
     [0, 0, 1]],

    [[1, 1],  # O
     [1, 1]],

    [[0, 1, 1],  # S
     [1, 1, 0]],

    [[1, 1, 0],  # Z
     [0, 1, 1]]
]

COLORS = [
    arcade.color.CYAN,  # I
    arcade.color.ORIOLES_ORANGE,  # T
    arcade.color.ORANGE,  # L
    arcade.color.BLUE,  # J
    arcade.color.YELLOW,  # O
    arcade.color.GREEN,  # S
    arcade.color.RED  # Z
]


class Tetris(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Тетрис")
        arcade.set_background_color(arcade.color.SILVER)

        # Игровое поле (0 — пусто, 1-7 — фигура)
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

        # Текущая фигура
        self.current_piece = None
        self.current_color = None
        self.current_x = 0
        self.current_y = 0

        # Скорость игры
        self.fall_speed = 0.5  # Секунд на клетку
        self.fall_timer = 0
        self.paused = False
        self.game_over = False
        self.score = 0

        # Батч для текста
        self.batch = Batch()

        self.new_piece()

        # Музыка
        self.sound = arcade.load_sound(":resources:music/1918.mp3", streaming=True)

        self.sound_player = arcade.play_sound(self.sound, volume=1, pan=0.0, loop=True)

        # Создаём частицы
        self.emitter = None

        self.particle_line()

    def new_piece(self):
        """ Создание новой фигуры """
        shape_idx = random.randint(0, len(SHAPES) - 1)
        self.current_piece = SHAPES[shape_idx]
        self.current_color = COLORS[shape_idx]

        # Начальная позиция (центр верхней части)
        self.current_x = GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
        self.current_y = GRID_HEIGHT - 1

        # Проверка на завершение игры
        if not self.is_valid_position():
            self.game_over = True

    def rotate_piece(self):
        """ Поворот фигуры """
        # Транспонирование матрицы с последующим обращением строк
        rotated = [[self.current_piece[y][x]
                    for y in range(len(self.current_piece) - 1, -1, -1)]
                   for x in range(len(self.current_piece[0]))]

        old_piece = self.current_piece
        self.current_piece = rotated

        # Если поворот невозможен, возвращаем исходную
        if not self.is_valid_position():
            self.current_piece = old_piece

    def is_valid_position(self, dx=0, dy=0):
        """ Проверка возможности размещения фигуры """
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    # Координаты в сетке
                    grid_x = self.current_x + x + dx
                    grid_y = self.current_y - y + dy

                    # Проверка границ
                    if grid_x < 0 or grid_x >= GRID_WIDTH or grid_y < 0:
                        return False

                    # Проверка столкновения с другими фигурами
                    if grid_y < GRID_HEIGHT and self.grid[grid_y][grid_x]:
                        return False
        return True

    def place_piece(self):
        """ Фиксация фигуры на поле """
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    grid_x = self.current_x + x
                    grid_y = self.current_y - y
                    if 0 <= grid_y < GRID_HEIGHT:
                        self.grid[grid_y][grid_x] = self.current_color
                        hit = arcade.load_sound(":resources:sounds/hurt3.wav")
                        arcade.play_sound(hit)


        # Проверка заполненных линий
        self.check_lines()

        # Создание новой фигуры
        self.new_piece()

    def check_lines(self):
        """ Проверка и удаление заполненных линий """
        lines_cleared = 0
        y = GRID_HEIGHT - 1
        while y >= 0:
            if all(self.grid[y]):
                # Удаление линии
                for y2 in range(y, GRID_HEIGHT - 1):
                    self.grid[y2] = self.grid[y2 + 1][:]

                # Очистка верхней линии
                self.grid[GRID_HEIGHT - 1] = [0] * GRID_WIDTH
                lines_cleared += 1
            else:
                y -= 1

        # Начисление очков
        if lines_cleared > 0:
            self.score += [100, 300, 500, 800][min(lines_cleared - 1, 3)]

    def hard_drop(self):
        """ Мгновенное падение фигуры """
        while self.is_valid_position(dy=-1):
            self.current_y -= 1
        self.place_piece()

    # Функция частиц
    def particle_line(self):
        self.emitter = Emitter(
            center_xy=(0, -5),
            emit_controller=EmitMaintainCount(100),
            particle_factory=lambda emitter: FadeParticle(
                filename_or_texture="Assets/particle.png",
                # Полоса по горизонтали от 0 до 300
                center_xy=(random.uniform(0, 300), 0),
                change_xy=(0, random.uniform(0.5, 0.5)),  # Скорость вверх
                lifetime=random.uniform(0.5, 1),  # Время жизни
                scale=0.2
            )

        )

    def on_draw(self):
        self.clear()

        # Рисуем сетку
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x]:
                    color = self.grid[y][x]
                    arcade.draw_rect_filled(
                        arcade.rect.XYWH(x * CELL_SIZE + CELL_SIZE // 2,
                                         y * CELL_SIZE + CELL_SIZE // 2,
                                         CELL_SIZE - 1, CELL_SIZE - 1), color
                    )

        # Рисуем текущую фигуру
        if not self.game_over:
            for y, row in enumerate(self.current_piece):
                for x, cell in enumerate(row):
                    if cell:
                        screen_x = (self.current_x + x) * CELL_SIZE + CELL_SIZE // 2
                        screen_y = (self.current_y - y) * CELL_SIZE + CELL_SIZE // 2
                        arcade.draw_rect_filled(
                            arcade.rect.XYWH(screen_x, screen_y,
                                             CELL_SIZE - 1, CELL_SIZE - 1), self.current_color
                        )

        # Сетка
        for i in range(GRID_WIDTH + 1):
            x = i * CELL_SIZE
            arcade.draw_line(x, 0, x, SCREEN_HEIGHT, arcade.color.OLD_SILVER)

        for i in range(GRID_HEIGHT + 1):
            y = i * CELL_SIZE
            arcade.draw_line(0, y, SCREEN_WIDTH, y, arcade.color.OLD_SILVER)

        # Информация
        info = arcade.Text(f"Счет: {self.score}", 10, SCREEN_HEIGHT - 30,
                           arcade.color.BLACK, 16, batch=self.batch)
        balance = arcade.Text(f"Монеты: {(self.score * DIFFICULTY) // 10}", 10, SCREEN_HEIGHT - 50,
                              arcade.color.BLACK, 16, batch=self.batch)
        # particles = arcade.particles.EternalParticle()
        game_over = arcade.Text("ИГРА ОКОНЧЕНА!",
                                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                arcade.color.CANDY_APPLE_RED, 30,
                                anchor_x="center", batch=None)
        # restart = arcade.Text("Нажмите R для продолжения!",
        #                         SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.3,
        #                         arcade.color.CADMIUM_GREEN, 17,
        #                         anchor_x="center", batch=None)
        pause = arcade.Text("ПАУЗА",
                            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40,
                            arcade.color.YELLOW, 30, anchor_x="center",
                            batch=None)

        if self.game_over:
            game_over.batch = self.batch
            # restart.batch = self.batch
        else:
            game_over.batch = None

        if self.paused:
            pause.batch = self.batch
        else:
            pause.batch = None
        self.batch.draw()

        # Рисуем частицы
        if self.emitter:
            self.emitter.draw()

    def on_update(self, delta_time):
        if self.paused or self.game_over:
            return

        self.fall_timer += delta_time
        if self.fall_timer > self.fall_speed:
            self.fall_timer = 0

            if self.is_valid_position(dy=-1):
                self.current_y -= 1
            else:
                self.place_piece()

        # Обновляем частицы
        if self.emitter:
            self.emitter.update()

    def on_key_press(self, key, modifiers):
        if self.game_over:
            arcade.stop_sound(self.sound_player)
            return

        if key == arcade.key.P:
            self.paused = not self.paused
            return

        if self.paused:
            return

        if key == arcade.key.LEFT and self.is_valid_position(dx=-1):
            self.current_x -= 1
        elif key == arcade.key.RIGHT and self.is_valid_position(dx=1):
            self.current_x += 1
        elif key == arcade.key.DOWN and self.is_valid_position(dy=-1):
            self.current_y -= 1
        elif key == arcade.key.UP:
            self.rotate_piece()
        elif key == arcade.key.SPACE:
            self.hard_drop()

    # def (self):

    def on_close(self):
        # Останавливаем музыку, чтобы она не ушла в главное меню
        arcade.stop_sound(self.sound_player)
        super().on_close()


def main():
    game = Tetris()
    arcade.run()


if __name__ == "__main__":
    main()
