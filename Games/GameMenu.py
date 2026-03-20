import arcade
from Games.Arculator.arculator import Arculator
from Games.Calcublock.Calcublock import Tetris
from Games.Calcugambling.Calcugambling import Calcugambling
from Games.Culcuraptor.culcuraptor import Culcuraptor
from Games.Platformer.Platformer import GameWindow
from Games.Snakulator.snakulator import Snakulator

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

# Цветовая схема как в калькуляторе (переведена в RGB)
COLORS = {
    "background": (26, 26, 26),  # #1a1a1a - темный фон
    "button": (50, 50, 50),  # #323232 - цвет кнопок
    "button_hover": (64, 64, 64),  # #404040 - при наведении
    "button_pressed": (40, 40, 40),  # #282828 - при нажатии
    "text": (255, 255, 255),  # white - белый текст
    "border": (80, 80, 80)  # #505050 - цвет границы
}

WIDTH = 800
HEIGHT = 800


class Menu(arcade.View):
    def __init__(self):
        super().__init__()
        # Устанавливаем цвет фона как в калькуляторе
        arcade.set_background_color(COLORS["background"])

        # --------------------------------------------------------------------------------------------------------------
        # Создание кнопок для открытия игр
        # TODO: ауф
        self.arculator_btn = arcade.SpriteSolidColor(int(75 * SIZE), int(75 * SIZE), WIDTH * 0.375,
                                                     HEIGHT * 0.2, COLORS["button"])
        self.arculator_btn_list = arcade.SpriteList()
        self.arculator_btn_list.append(self.arculator_btn)

        self.calcublock_btn = arcade.SpriteSolidColor(int(75 * SIZE), int(75 * SIZE), WIDTH * 0.25,
                                                      HEIGHT * 0.35, COLORS["button"])
        self.calcublock_btn_list = arcade.SpriteList()
        self.calcublock_btn_list.append(self.calcublock_btn)

        self.calcugambling_btn = arcade.SpriteSolidColor(int(75 * SIZE), int(75 * SIZE), WIDTH * 0.6,
                                                         HEIGHT * 0.1, COLORS["button"])
        self.calcugambling_btn_list = arcade.SpriteList()
        self.calcugambling_btn_list.append(self.calcugambling_btn)

        self.culuraptor_btn = arcade.SpriteSolidColor(int(75 * SIZE), int(75 * SIZE), WIDTH * 0.5,
                                                      HEIGHT * 0.35, COLORS["button"])
        self.culuraptor_btn_list = arcade.SpriteList()
        self.culuraptor_btn_list.append(self.culuraptor_btn)

        self.platformer_btn = arcade.SpriteSolidColor(int(75 * SIZE), int(75 * SIZE), WIDTH * 0.5,
                                                      HEIGHT * 0.5, COLORS["button"])
        self.platformer_btn_list = arcade.SpriteList()
        self.platformer_btn_list.append(self.platformer_btn)

        self.snakulator_btn = arcade.SpriteSolidColor(int(75 * SIZE), int(75 * SIZE), WIDTH * 0.25,
                                                      HEIGHT * 0.5, COLORS["button"])
        self.snakulator_btn_list = arcade.SpriteList()
        self.snakulator_btn_list.append(self.snakulator_btn)

        # --------------------------------------------------------------------------------------------------------------

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> bool | None:
        if self.arculator_btn.visible and arcade.get_sprites_at_point((x, y), self.arculator_btn_list):
            self.window.width, self.window.height = round(600 * SIZE), round(800 * SIZE)
            self.window.title = "arcanoid"
            game_view = Arculator()
            self.window.show_view(game_view)

        elif self.calcublock_btn.visible and arcade.get_sprites_at_point((x, y), self.calcublock_btn_list):
            self.window.width, self.window.height = round(430 * SIZE), round(840 * SIZE)
            self.window.title = "tetris"
            game_view = Tetris()
            self.window.show_view(game_view)

        elif self.calcugambling_btn.visible and arcade.get_sprites_at_point((x, y), self.calcugambling_btn_list):
            self.window.width, self.window.height = round(528 * SIZE), round(828 * SIZE)
            self.window.title = "gamble"
            game_view = Calcugambling()
            self.window.show_view(game_view)

        elif self.culuraptor_btn.visible and arcade.get_sprites_at_point((x, y), self.culuraptor_btn_list):
            self.window.width, self.window.height = round(800 * SIZE), round(600 * SIZE)
            self.window.title = "raptor"
            game_view = Culcuraptor()
            self.window.show_view(game_view)

        elif self.platformer_btn.visible and arcade.get_sprites_at_point((x, y), self.platformer_btn_list):
            self.window.width, self.window.height = round(1000), round(600)
            self.window.title = "platformer"
            game_view = GameWindow()
            self.window.show_view(game_view)

        # elif self.snakulator_btn.visible and arcade.get_sprites_at_point((x, y), self.snakulator_btn_list):
        #     self.window.width, self.window.height = round(600 * SIZE), round(600 * SIZE)
        #     game_view = Snakulator
        #     self.window.show_view(game_view)

    def on_draw(self):
        self.clear()

        # Отрисовка кнопок
        self.arculator_btn_list.draw()
        self.calcublock_btn_list.draw()
        self.calcugambling_btn_list.draw()
        self.culuraptor_btn_list.draw()
        self.platformer_btn_list.draw()
        # self.snakulator_btn_list.draw()
        arcade.draw_text("arc", WIDTH * 0.355, HEIGHT * 0.190, arcade.color.WHITE, 20 ,font_name="Segoe UI")
        arcade.draw_text("ttr", WIDTH * 0.235, HEIGHT * 0.340, arcade.color.WHITE, 20, font_name="Segoe UI")
        arcade.draw_text("rnd", WIDTH * 0.575, HEIGHT * 0.090, arcade.color.WHITE, 20, font_name="Segoe UI")
        arcade.draw_text("trx", WIDTH * 0.480, HEIGHT * 0.340, arcade.color.WHITE, 20, font_name="Segoe UI")
        arcade.draw_text("ptf", WIDTH * 0.480, HEIGHT * 0.490, arcade.color.WHITE, 20, font_name="Segoe UI")
        arcade.draw_circle_outline(WIDTH * 0.375, HEIGHT * 0.200, 50, COLORS["background"], 15)
        arcade.draw_circle_outline(WIDTH * 0.250, HEIGHT * 0.350, 50, COLORS["background"], 15)
        arcade.draw_circle_outline(WIDTH * 0.600, HEIGHT * 0.100, 50, COLORS["background"], 15)
        arcade.draw_circle_outline(WIDTH * 0.500, HEIGHT * 0.350, 50, COLORS["background"], 15)
        arcade.draw_circle_outline(WIDTH * 0.500, HEIGHT * 0.500, 50, COLORS["background"], 15)
        # arcade.draw_circle_outline(WIDTH * 0.250, HEIGHT * 0.500, 50, COLORS["background"], 15)
        # arcade.draw_text("", WIDTH * 0.225, HEIGHT * 0.490, arcade.color.WHITE, 20, font_name="Segoe UI")


class Start:
    def __init__(self):
        ...

    def open(self):
        print("starting")
        arcade.clear_timings()
        arcade.close_window()
        game_window = arcade.Window(round(WIDTH * SIZE), round(HEIGHT * SIZE), "Древо игр")
        view = Menu()
        game_window.show_view(view)
        arcade.run()

    def close(self):
        arcade.close_window()
