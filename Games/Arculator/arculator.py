import arcade
import random
import math
from Games.Arculator.collision import bounce
from pyglet.event import EVENT_HANDLE_STATE

# ВРЕМЕННЫЙ словарь для перевода хп блока в текстуру
NUM_TO_CARDS = {0: "A", 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: "K"}

with open("Games/Arculator/saves") as file:
    settings = file.readlines()
    SIZE = float(settings[0].split(": ")[1])
    DIFFICULTY = float(settings[1].split(": ")[1])


# Игрок - платформа, отбивающая мяч
class Player(arcade.Sprite):
    def __init__(self, window):
        super().__init__(":resources:/images/tiles/snowCenter.png")
        self.width, self.height = 100 * SIZE, 30 * SIZE
        self.speed = (500 + DIFFICULTY * 250) * SIZE

        self.window = window

    def update(self, delta_time: float = 1 / 60, *args, **kwargs):
        # Рассчёт направления движения
        direction = 0
        if 97 in self.window.key_pressed:
            direction -= 1
        if 100 in self.window.key_pressed:
            direction += 1

        # Движение, с учётом колизии со стенами и мячом
        a = self.width // 2
        if not self.collides_with_sprite(self.window.boll):
            self.center_x = max(a, min(self.window.width - a, self.center_x + self.speed * direction * delta_time))


# Мяч - шарик, ломающий блоки
class Boll(arcade.Sprite):
    def __init__(self, window):
        super().__init__(":resources:/images/pinball/pool_cue_ball.png", scale=3)
        self.width, self.height = 20 * SIZE, 20 * SIZE
        # Параметры для рассчёта траектории: dx, dy - перемещение по x, y соответственно
        self.speed, self.dx, self.dy = 0, 0, 0

        self.window = window

    def update(self, delta_time: float = 1 / 60, *args, **kwargs):
        # Коллизия с игроком и рассчёт угла полёта
        if self.collides_with_sprite(self.window.player):
            angle = math.atan2(self.center_y - 50 * SIZE, self.center_x - self.window.player.center_x)
            self.dx = math.cos(angle) * self.speed
            self.dy = math.sin(angle) * self.speed
        self.dx, self.dy = round(self.dx), round(self.dy)

        # Коллизия со стенами
        a = self.width // 2
        if not (a <= self.center_x + self.dx * delta_time <= self.window.width - a):
            self.dx *= -1
        if self.center_y + self.dy * delta_time > self.window.height - a:
            self.dy *= -1
        elif self.center_y < 0:
            self.window.setup()
            pass

        # Перемещение и коллизия с блоками
        start_x, start_y = self.center_x, self.center_y

        self.center_x += self.dx * delta_time
        self.center_y += self.dy * delta_time

        # Нахождение блока с которым соприкоснулись
        if self.collides_with_list(self.window.blocks):
            for block in self.window.blocks:
                if self.collides_with_sprite(block):
                    # Изменение номера и удаление при попадании по 0
                    if block.num == 0:
                        block.kill_time = 1

                        # Изменение скорости мяча
                        self.dx /= self.speed
                        self.dy /= self.speed

                        self.speed += (2.5 + DIFFICULTY / 2) * 8 * SIZE

                        self.dx = round(self.dx * self.speed)
                        self.dy = round(self.dy * self.speed)
                    else:
                        block.num -= 1
                        block.texture = arcade.load_texture(
                            f":resources:/images/cards/cardClubs{NUM_TO_CARDS[block.num]}.png")

        self.window.engine.update()

        dx, dy = round((self.center_x - start_x) / delta_time), round((self.center_y - start_y) / delta_time)
        bounce(self, dx, dy, delta_time)


# Блоки - платформы, которые необходимо сломать
class Block(arcade.Sprite):
    def __init__(self, x, y, start_num, window):
        super().__init__(f":resources:/images/cards/cardClubs{NUM_TO_CARDS[start_num]}.png")
        self.center_x, self.center_y = x, y
        self.width, self.height = 75 * SIZE, 75 * SIZE
        self.start_num = start_num
        self.num = start_num
        self.kill_time = 0

        self.window = window

    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        if self.kill_time == 1:
            self.kill_time += 1
        elif self.kill_time == 2:
            self.kill_time = 0
            self.window.blocks.remove(self)
            self.window.sprites.remove(self)


class MyGame(arcade.Window):
    def __init__(self, parent_pos=None):
        super().__init__(round(600 * SIZE), round(800 * SIZE), "Arculator")
        self.background = arcade.load_texture(":resources:/images/backgrounds/abstract_1.jpg")

        # Передача позиции
        # res = list(map(int, "".join([x if x.isnumeric() else " " for x in str(parent_pos)]).split()))
        # self.set_location(int(res[1]), int(res[2]))

        # Создание управляемой платформы
        self.player = Player(self)

        # Создание мяча
        self.boll = Boll(self)

        # Генерация блоков
        self.blocklist = arcade.SpriteList()
        a = 75 * SIZE
        b = round(2 + DIFFICULTY)
        for height in range(b):
            y = self.height - a / 2 - a * height
            for width in range(-(height + 1) % (b + 1)):
                num = -(height + 1) % b + -(width + 1) % (-(height + 1) % (b + 1))
                if width == 0:
                    x = self.width / 2
                    block = Block(x, y, num, self)
                    self.blocklist.append(block)
                else:
                    x1, x2 = self.width / 2 - a * width, self.width / 2 + a * width
                    block1, block2 = Block(x1, y, num, self), Block(x2, y, num, self)
                    self.blocklist.extend([block1, block2])

        # Спрайтлист для отображаемых спрайтов
        self.sprites = arcade.SpriteList()
        self.sprites.extend([self.player, self.boll])
        self.sprites.extend(self.blocklist)

        # Спрайтлист для неразрушенных блоков
        self.blocks = arcade.SpriteList()
        self.blocks.extend(self.blocklist)

        # Множество нажатых клавиш
        self.key_pressed = set()

        # Физический движок
        self.engine = arcade.PhysicsEngineSimple(self.boll, self.blocks)

    def setup(self):
        self.player.center_x, self.player.center_y = self.width / 2, 50 * SIZE

        self.boll.center_x, self.boll.center_y = random.choice(range(250, 350)) * SIZE, 70 * SIZE
        self.boll.speed = 500 * SIZE

        for block in self.blocklist:
            block.num = block.start_num
            block.texture = arcade.load_texture(f":resources:/images/cards/cardClubs{NUM_TO_CARDS[block.num]}.png")
            if block not in self.sprites:
                self.sprites.append(block)
                self.blocks.append(block)

    def on_key_press(self, symbol: int, modifiers: int) -> EVENT_HANDLE_STATE:
        self.key_pressed.add(symbol)

    def on_key_release(self, symbol: int, modifiers: int) -> EVENT_HANDLE_STATE:
        self.key_pressed.discard(symbol)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.XYWH(self.width / 2, self.height / 2, self.width, self.height))
        self.sprites.draw()

    def on_update(self, delta_time: float):
        self.sprites.update()


if __name__ == "__main__":
    game = MyGame()
    game.setup()
    arcade.run()
