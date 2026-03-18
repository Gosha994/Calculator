import arcade
from Games.Arculator.arculator import Arculator

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

        print(self.width, self.height)

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
            self.window.width, self.window.height = 600, 800
            game_view = Arculator()
            self.window.show_view(game_view)

        elif self.calcublock_btn.visible and arcade.get_sprites_at_point((x, y), self.calcublock_btn_list):
            game_view = None
            self.window.show_view(game_view)

        elif self.calcugambling_btn.visible and arcade.get_sprites_at_point((x, y), self.calcugambling_btn_list):
            game_view = None
            self.window.show_view(game_view)

        elif self.culuraptor_btn.visible and arcade.get_sprites_at_point((x, y), self.culuraptor_btn_list):
            game_view = None
            self.window.show_view(game_view)

        elif self.platformer_btn.visible and arcade.get_sprites_at_point((x, y), self.platformer_btn_list):
            game_view = None
            self.window.show_view(game_view)

        elif self.snakulator_btn.visible and arcade.get_sprites_at_point((x, y), self.snakulator_btn_list):
            game_view = None
            self.window.show_view(game_view)


class Start:
    def __init__(self):
        ...
    def open(self):
        print("starting")
        game_window = arcade.Window(round(800 * SIZE), round(800 * SIZE), "game")
        view = Arculator()
        game_window.show_view(view)
        arcade.run()

    def close(self):
        arcade.close_window()