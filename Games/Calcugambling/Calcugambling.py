import arcade
import random
import time

from arcade.uicolor import BLACK

# константы
with open("setup") as file:
    setting = file.readlines()
    SAVES = {}
    for elem in setting:
        SAVES[f"{elem.split(" = ")[0]}"] = elem.split(" = ")[1]

with open("inventory") as file:
    setting = file.readlines()
    INVENTORY = {}
    for elem in setting:
        INVENTORY[f"{elem.split(" = ")[0]}"] = elem.split(" = ")[1]

SIZE = int(SAVES["SIZE"])
DIFFICULTY = int(SAVES["DIFFICULTY"])
BALANCE = int(INVENTORY["BALANCE"])

# Задаём размеры окна
SCREEN_WIDTH = 370 * SIZE
SCREEN_HEIGHT = 580 * SIZE
SCREEN_TITLE = "CalcuGamble"

# Тестовые слоты, позже будут заменены на текст для других игровых механик
# SLOTS = "👨‍💼👯‍♀️🪵🍄🍇🎱🎟💵7️⃣🔑🌭❌💀"
SLOTS = "1234567890+-*"


class WheelSlot(arcade.Sprite):
    def __init__(self, scale=1.1):
        super().__init__("Games/Calcugambling/GambleWheal/GambleWheal0.png", scale=scale)
        self.is_spinning = False
        self.spin_start_time = 0
        self.spin_duration = 3.0
        self.current_frame = 0
        self.textures = []
        self.fixed_scale = scale

        # Добавляем символ для отображения поверх колеса
        # self.symbol = random.choice(["👨‍💼", "👯‍♀️", "🪵", "🍄", "🍇", "🎱", "🎟", "💵", "7️⃣", "🔑", "🌭", "❌", "💀"])
        self.symbol = random.choice(["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "+", "-", "*"])

        # Параметры скорости анимации
        self.animation_speed = 10.0
        self.slowdown_factor = 0.8

        self.load_textures()

    def load_textures(self):
        for i in range(3):
            texture = arcade.load_texture(f"Games/Calcugambling/GambleWheal/GambleWheal{i}.png")
            self.textures.append(texture)

    def start_spin(self):
        """Начинаем вращение"""
        self.is_spinning = True
        self.spin_start_time = time.time()
        self.current_frame = 0
        self.animation_speed = 15.0

        # При начале вращения выбираем новый случайный символ
        # self.symbol = random.choice(["👨‍💼", "👯‍♀️", "🪵", "🍄", "🍇", "🎱", "🎟", "💵", "7️⃣", "🔑", "🌭", "❌", "💀"])
        self.symbol = random.choice(["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "+", "-", "*"])

    def update_animation(self):
        if not self.is_spinning:
            return

        elapsed_time = time.time() - self.spin_start_time

        if elapsed_time >= self.spin_duration:
            self.is_spinning = False
            self.set_texture(0)
            return

        progress = elapsed_time / self.spin_duration

        if progress < 0.7:
            current_speed = 30.0 - (progress * 10)
        else:
            current_speed = 5.0 * (1.0 - (progress - 0.7) / 0.3)

        total_frames = elapsed_time * current_speed
        frame_index = int(total_frames) % 3

        self.set_texture(frame_index)

    def set_texture(self, texture_index):
        self.texture = self.textures[texture_index]
        self.scale = self.fixed_scale


class Calcugambling(arcade.Window):
    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=SCREEN_TITLE):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.ASH_GREY)

        # Баланс игрока
        self.balance = BALANCE

        # Создаём список спрайтов
        self.layout_list = arcade.SpriteList()
        self.button_list = arcade.SpriteList()
        self.slot_list = arcade.SpriteList()
        self.wheel_slots = []

        # Создаем шрифт для текста
        self.font_size = 24
        self.font_color = arcade.color.WHITE

    def setup(self):
        """Настройка игры, создание элементов"""
        self.wheel_slots.clear()
        self.slot_list.clear()

        # Создаем слоты (колеса)
        slot_x = (self.width // 84) * 10
        slot_y = self.height * 0.6
        for _ in range(5):
            wheel_slot = WheelSlot(scale=1.1)
            wheel_slot.center_x = slot_x
            wheel_slot.center_y = slot_y
            self.slot_list.append(wheel_slot)
            self.wheel_slots.append(wheel_slot)
            slot_x += (self.width // 84) * 18.19

        # Добавляем рамку
        frame = arcade.Sprite("Games/Calcugambling/pixil-frame-0(1).png", scale=1.1)
        frame.center_x = SCREEN_WIDTH // 2
        frame.center_y = SCREEN_HEIGHT * 0.6
        self.layout_list.append(frame)

        # Добавляем кнопку
        button = arcade.Sprite("Games/Calcugambling/Button.png", scale=1.1)
        button.center_x = SCREEN_WIDTH // 2
        button.center_y = SCREEN_HEIGHT * 0.3
        self.button_list.append(button)

    def on_draw(self):
        """Отрисовка всех спрайтов и текста"""
        self.clear()

        # Отрисовываем спрайты
        self.layout_list.draw()
        self.button_list.draw()
        self.slot_list.draw()

        # Отрисовываем текст поверх спрайтов
        self.draw_text_over_wheels()

    def draw_text_over_wheels(self):
        """Отрисовка текста поверх колес"""
        # Отображаем символы на каждом колесе
        for wheel in self.wheel_slots:
            # Текст отображается только когда колесо не вращается
            if not wheel.is_spinning:
                arcade.draw_text(
                    wheel.symbol,
                    wheel.center_x,
                    wheel.center_y,
                    arcade.color.BLACK,
                    self.font_size,
                    anchor_x="center",
                    anchor_y="center",
                    bold=True
                )
            else:
                # Можно отображать что-то другое во время вращения
                arcade.draw_text(
                    "",  # Текст во время вращения
                    wheel.center_x,
                    wheel.center_y,
                    arcade.color.GOLD,
                    self.font_size - 4,
                    anchor_x="center",
                    anchor_y="center"
                )

        # Можно добавить статический текст где-нибудь еще
        # Например, заголовок или счет
        arcade.draw_text(
            f"Монеты: {self.balance}",
            SCREEN_WIDTH // 5,
            SCREEN_HEIGHT * 0.7,
            arcade.color.GOLD,
            20,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

        arcade.draw_text(
            "Крутить",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT * 0.3,
            arcade.color.DARK_BLUE,
            16,
            anchor_x="center",
            anchor_y="center"
        )

    def on_update(self, delta_time):
        """Обновление логики игры"""
        for wheel in self.wheel_slots:
            wheel.update_animation()

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка клика мышью"""
        buttons_hit = arcade.get_sprites_at_point((x, y), self.button_list)

        if buttons_hit and self.balance >= 100:
            self.balance -= 100
            for wheel in self.wheel_slots:
                wheel.start_spin()


if __name__ == "__main__":
    game = Calcugambling()
    game.setup()
    arcade.run()
