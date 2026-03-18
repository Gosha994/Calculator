import arcade

class Menu(arcade.View):
    def __init__(self):
        super().__init__()

        arculator_btn = arcade.Sprite()
        calcublock_btn = arcade.Sprite()
        calcugambling_btn = arcade.Sprite()
        culuraptor_btn = arcade.Sprite()
        platformer_btn = arcade.Sprite()
        snakulator_btn = arcade.Sprite()

if __name__ == "__main__":
    game_window = arcade.Window(800, 800, "game")
    view = Menu()
    game_window.show_view(view)
    arcade.run()