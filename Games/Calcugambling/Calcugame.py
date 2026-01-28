import arcade
import random

# константы
SIZE = 1
DIFFICULTY = 1

# Задаём размеры окна
SCREEN_WIDTH = 370
SCREEN_HEIGHT = 580
SCREEN_TITLE = "CalcuGamble"
SLOTS = "👨‍💼👯‍♀️🪵🍄🍇🎱🎟💵7️⃣🔑🌭❌💀"


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.ASH_GREY)

        # Создаём список спрайтов для монет
        self.layout_list = arcade.SpriteList()
        self.button_list = arcade.SpriteList()
        self.slot_list = arcade.SpriteList()

    def setup(self):
        """Настройка игры, создание монет"""

        slot_x = (self.width // 84) * 10
        slot_y = self.height * 0.6
        for _ in range(5):
            slot = arcade.Sprite("GambleWheal.png", scale=1.1)
            slot.center_x = slot_x
            slot.center_y = slot_y
            self.slot_list.append(slot)
            slot_x += (self.width // 84) * 18.19

        frame = arcade.Sprite("pixil-frame-0(1).png", scale=1.1)
        frame.center_x = SCREEN_WIDTH // 2
        frame.center_y = SCREEN_HEIGHT * 0.6
        self.layout_list.append(frame)

        button = arcade.Sprite("Button.png", scale=1.1)
        button.center_x = SCREEN_WIDTH // 2
        button.center_y = SCREEN_HEIGHT * 0.3
        self.button_list.append(button)
        # for _ in range(10):  # Создаём 10 монет
        #     coin = arcade.Sprite(":resources:images/items/coinGold.png", scale=0.5)
        #     coin.center_x = random.randint(0, SCREEN_WIDTH)
        #     coin.center_y = random.randint(0, SCREEN_HEIGHT)
        #     self.coin_list.append(coin)

    def on_draw(self):
        """Отрисовка всех спрайтов"""
        self.clear()
        self.layout_list.draw()
        self.button_list.draw()
        self.slot_list.draw()  # Отрисовываем все монеты

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка клика мышью"""
        coins_hit_list = arcade.get_sprites_at_point((x, y), self.button_list)  # В какие монеты тыкнул игрок.

        # Удаляем монеты, по которым кликнули
        for coin in self.slot_list:
            # coin.remove_from_sprite_lists()
            coin.texture = arcade.load_texture("img_1.png")
            coin.scale = 0.25

        if not self.slot_list:
            self.setup()  # Если все монеты собраны, создаём новые //злодейский смех//


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()  # Запускаем начальную настройку игры
    arcade.run()


if __name__ == "__main__":
    main()
