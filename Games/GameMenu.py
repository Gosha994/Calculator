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


class Menu(arcade.View):
    def __init__(self):
        super().__init__()

        # --------------------------------------------------------------------------------------------------------------
        # Создание кнопок для открытия игр
        self.arculator_btn = arcade.Sprite()
        self.arculator_btn_list = arcade.SpriteList()
        self.arculator_btn_list.append(self.arculator_btn)

        self.calcublock_btn = arcade.Sprite()
        self.calcublock_btn_list = arcade.SpriteList()
        self.calcublock_btn_list.append(self.calcublock_btn)

        self.calcugambling_btn = arcade.Sprite()
        self.calcugambling_btn_list = arcade.SpriteList()
        self.calcugambling_btn_list.append(self.calcugambling_btn)

        self.culuraptor_btn = arcade.Sprite()
        self.culuraptor_btn_list = arcade.SpriteList()
        self.culuraptor_btn_list.append(self.culuraptor_btn)

        self.platformer_btn = arcade.Sprite()
        self.platformer_btn_list = arcade.SpriteList()
        self.platformer_btn_list.append(self.platformer_btn)

        self.snakulator_btn = arcade.Sprite()
        self.snakulator_btn_list = arcade.SpriteList()
        self.snakulator_btn_list.append(self.snakulator_btn)
        # --------------------------------------------------------------------------------------------------------------

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> bool | None:
        if self.arculator_btn.visible and arcade.get_sprites_at_point((x, y), self.arculator_btn_list):
            self.window.width, self.window.height = round(600 * SIZE), round(800 * SIZE)
            game_view = Arculator()
            self.window.show_view(game_view)

        elif self.calcublock_btn.visible and arcade.get_sprites_at_point((x, y), self.calcublock_btn_list):
            self.window.width, self.window.height = round(430 * SIZE), round(840 * SIZE)
            game_view = Tetris()
            self.window.show_view(game_view)

        elif self.calcugambling_btn.visible and arcade.get_sprites_at_point((x, y), self.calcugambling_btn_list):
            self.window.width, self.window.height = round(528 * SIZE), round(828 * SIZE)
            game_view = Calcugambling()
            self.window.show_view(game_view)

        elif self.culuraptor_btn.visible and arcade.get_sprites_at_point((x, y), self.culuraptor_btn_list):
            self.window.width, self.window.height = round(800 * SIZE), round(600 * SIZE)
            game_view = Culcuraptor()
            self.window.show_view(game_view)

        elif self.platformer_btn.visible and arcade.get_sprites_at_point((x, y), self.platformer_btn_list):
            self.window.width, self.window.height = round(1000), round(600)
            game_view = GameWindow()
            self.window.show_view(game_view)

        elif self.snakulator_btn.visible and arcade.get_sprites_at_point((x, y), self.snakulator_btn_list):
            self.window.width, self.window.height = round(600 * SIZE), round(600 * SIZE)
            game_view = Snakulator
            self.window.show_view(game_view)


class Start:
    def __init__(self):
        ...
    def open(self):
        print("starting")
        game_window = arcade.Window(round(600 * SIZE), round(600 * SIZE), "game")
        view = Menu()
        game_window.show_view(view)
        arcade.run()

    def close(self):
        arcade.close_window()