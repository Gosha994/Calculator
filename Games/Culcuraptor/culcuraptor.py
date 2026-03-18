import arcade
import random
from pyglet.event import EVENT_HANDLE_STATE
from pyglet.graphics import Batch

# Константы, необходимые при запуске напрямую из пай файла
with open("setup") as file:
    setting = file.readlines()
    SAVES = {}
    for elem in setting:
        SAVES[f"{elem.split(" = ")[0]}"] = elem.split(" = ")[1]

SIZE = int(SAVES["SIZE"])
DIFFICULTY = int(SAVES["DIFFICULTY"])


# ----------------------------------------------------------------------------------------------------------------------
# Динозаврик (времено робот)
class Raptor(arcade.Sprite):
    def __init__(self, window):
        super().__init__(":resources:/images/animated_characters/robot/robot_idle.png")
        self.window, self.SIZE = window, window.SIZE
        self.width, self.height = 50 * self.SIZE, 100 * self.SIZE

        # Залание парметров, необходимых для коректной работы прыжков
        self.jump_power = 30 * self.SIZE
        self.jump = False

        # Переменные для анимации персонажа
        self.texture_list = [arcade.load_texture(f":resources:/images/animated_characters/robot/robot_walk{i}.png")
                             for i in range(8)]
        self.texture_change_time = 0
        self.texture_num = 0

        # Звук прыжка
        self.jump_sound = arcade.load_sound(":resources:sounds/jump5.wav")
        # Звук смерти
        self.dead_sound = arcade.load_sound(":resources:sounds/error3.wav")

        # Наличие смерти
        self.dead = False

    def update(self, delta_time: float = 1 / 60, *args, **kwargs):
        # Прыжок
        grounded = self.window.engine.can_jump(y_distance=5)
        if self.jump and grounded:
            self.window.engine.jump(self.jump_power)
            arcade.play_sound(self.jump_sound, volume=1.0, pan=0.0, loop=False)

        # Проверка колизии с препядствиями
        if self.collides_with_list(self.window.objects):
            self.window.playing = False
            arcade.play_sound(self.dead_sound, volume=1.0, pan=0.0, loop=False)

        # Анимация персонажа
        self.texture_change_time += delta_time
        if self.texture_change_time >= 0.05:
            self.texture = self.texture_list[self.texture_num]
            self.texture_num = (self.texture_num + 1) % 8
            self.texture_change_time = 0


# ----------------------------------------------------------------------------------------------------------------------
# Препядствия
class Object(arcade.Sprite):
    def __init__(self, window, cords):
        super().__init__(":resources:/images/tiles/cactus.png", scale=5)
        self.window = window
        self.width, self.height = 75 * window.SIZE, 75 * window.SIZE
        self.center_x, self.center_y = cords

        if self.center_y > self.window.ground_level + 37.5 * self.window.SIZE:
            self.texture = arcade.load_texture(":resources:/images/enemies/fly.png")

    def update(self, delta_time: float = 1 / 60, *args, **kwargs):
        # Перемещение
        self.center_x -= self.window.object_speed

        # Уничтожение при вылете за экран
        if self.center_x <= -self.width / 2:
            self.kill()


# ----------------------------------------------------------------------------------------------------------------------
# Сама игра
class Culcuraptor(arcade.View):
    def __init__(self):
        super().__init__()
        global SIZE, DIFFICULTY
        self.SIZE, self.DIFFICULTY = SIZE, DIFFICULTY

        # Константы, связанные с ходом игры
        self.playing = False
        self.time_played = 0

        # Создание поверхности по которой "ходит" игрок
        self.ground_level = 100 * self.SIZE
        self.ground, self.grounds = arcade.Sprite(), arcade.SpriteList()
        self.ground.center_x, self.ground.center_y = self.width / 2, self.ground_level / 2
        self.ground.width, self.ground.height = self.width, self.ground_level
        self.grounds.append(self.ground)

        self.player = Raptor(self)  # Игрок
        self.objects = arcade.SpriteList()  # Список препядствий
        self.sprites = arcade.SpriteList()  # Список отображаемых спрайтов (игрока)
        self.sprites.append(self.player)

        # Константы, связанные с препядствиями
        self.object_timer = 0  # Таймер промежутков между "волнами" препядствий
        self.object_num_limit = 10 + 5 * self.DIFFICULTY  # Лимит сложности "волн"
        self.object_speed = 0
        self.object_a = self.DIFFICULTY / 10  # Ускорение
        self.object_speed_limit = 12 + 3 * self.SIZE * self.DIFFICULTY

        # Словари для генерации "волн"
        self.object_types = {1: ",", 2: ",,", 3: ",,,", 4: "'", 5: "''", 6: "-", 7: ",'"}
        x, y = self.width, self.ground_level + 37.5 * self.SIZE
        self.types_to_obj_cords = {",": (x, y), "'": (x, y + 225 * self.SIZE), "-": (x, y + 150 * self.SIZE)}

        # Текстовое табло
        self.batch = Batch()
        self.label = arcade.Text("Press SPACE to start", 16, 16, arcade.color.GRAY, 14,
                                 batch=self.batch)

        # Физический движок
        self.engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player,
            gravity_constant=2 * self.SIZE,
            walls=self.grounds)

        # Звук обновления счёта
        self.score_update = arcade.load_sound(":resources:sounds/coin1.wav")

        self.setup()

    # ------------------------------------------------------------------------------------------------------------------
    def setup(self):
        self.playing = False
        self.time_played = 0

        self.object_timer = 5
        self.object_speed = 8 * self.SIZE

        self.player.center_x, self.player.center_y = self.width / 2, self.ground_level + self.player.height / 2

    # ------------------------------------------------------------------------------------------------------------------
    def on_draw(self) -> EVENT_HANDLE_STATE:
        self.clear()
        # Задний фон
        arcade.draw_rect_filled(arcade.XYWH(self.width / 2, self.height / 2, self.width, self.height),
                                arcade.color.LIGHT_GRAY)
        arcade.draw_line(0, self.ground_level, self.width, self.ground_level, arcade.color.GRAY, 5)

        # Отображение объектов
        self.objects.draw()
        self.sprites.draw()

        # Отображение текстового табло
        self.batch.draw()

        arcade.draw_circle_filled(self.width * 0.1, self.height * 0.9, 35, arcade.color.YELLOW)
        arcade.draw_circle_outline(self.width * 0.1, self.height * 0.9, 36, arcade.color.ORANGE, 3)

        if not self.playing and self.time_played > 0:  # Игра остановлена
            text = "Press SPACE to restart"
            arcade.draw_text(text,
                             self.width // 2,
                             self.height // 2,
                             arcade.color.GRAY,
                             30, 3,
                             anchor_x="center")

    # ------------------------------------------------------------------------------------------------------------------
    def on_update(self, delta_time: float):
        # Проверка идёт ли процесс игры
        if self.playing:

            # Ограничение скорости объектов
            if self.object_speed < self.object_speed_limit:
                self.object_speed += self.object_a * delta_time
            else:
                self.object_speed = self.object_speed_limit

            if self.object_timer <= 0:  # Отсчёт времени до следующей "волны"
                self.object_timer = random.choice(range(3, 6))  # Перезапуск таймера

                # Расчёт сложности "волны" учитывая время и сложность игры
                object_num = round(2 + self.time_played / 15)
                object_num = self.object_num_limit if object_num >= self.object_num_limit else object_num

                # Генерация "волны"
                x0 = 0
                while object_num > 0:
                    # Выбор возможного фрагмента
                    n_max = 7 if object_num >= 7 else object_num
                    n = random.choice(range(n_max)) + 1

                    # Проверка возможности прохождения фрагмета и исправление его в противном случае
                    if self.object_speed < 10 and n == 3:
                        n = 2

                    object_type = self.object_types[n]  # Расшифровка номера фрагмета как строку
                    object_num -= n

                    x1 = 0
                    for i in object_type:  # Разбитие строки на символы
                        # Расшифровка символов как кординаты препядствия
                        x, y = self.types_to_obj_cords[i]
                        x += x0 + x1
                        x1 += 50 * self.SIZE

                        # Создание препядствия
                        object_ = Object(self, (x, y))
                        self.objects.append(object_)
                    x0 += (150 + 50 * self.DIFFICULTY) * self.SIZE + x1
            else:
                self.object_timer -= delta_time

            # Обновление всех объектов
            self.sprites.update()
            self.objects.update()
            self.engine.update()

            # Отсчёт игрового времени и отображение его
            if (((10 * int(self.time_played)) // 10) % 10 == 0 and
                    self.time_played < (10 * int(self.time_played)) // 10 + 0.02 and self.time_played > 1):
                arcade.play_sound(self.score_update, volume=1.0, pan=0.0, loop=False)

            self.time_played += delta_time
            self.label.text = f"Время: {round(self.time_played, 2)}"

    # ------------------------------------------------------------------------------------------------------------------
    def on_key_press(self, symbol: int, modifiers: int) -> EVENT_HANDLE_STATE:
        if symbol == arcade.key.SPACE:  # Прыжок
            self.player.jump = True

            # Запуск игры в случае если та остановлена
            if not self.playing:
                self.playing = True
                self.player.center_x = 100 * self.SIZE
                self.time_played = 0
                self.object_speed = 8 * self.SIZE

                for obj in self.objects:
                    obj.kill()
                self.objects.clear()

    # ------------------------------------------------------------------------------------------------------------------
    def on_key_release(self, symbol: int, modifiers: int) -> EVENT_HANDLE_STATE:
        if symbol == arcade.key.SPACE:  # Прерывание прыжка
            self.player.jump = False
            if self.player.change_y > 0:
                self.player.change_y *= 0.5


if __name__ == "__main__":
    game = Culcuraptor(SIZE, DIFFICULTY)
    game.setup()
    arcade.run()
