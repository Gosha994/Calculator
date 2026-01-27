import arcade
import random
from pyglet.event import EVENT_HANDLE_STATE
from pyglet.graphics import Batch


SIZE = 1
DIFFICULTY = 1


class Raptor(arcade.Sprite):
    def __init__(self, window):
        super().__init__()
        self.window, self.SIZE = window, window.SIZE
        self.width, self.height = 50 * self.SIZE, 100 * self.SIZE

        self.jump_power = 30 * self.SIZE
        self.jump_timer_max = 0.2
        self.jump_timer = 0
        self.jump = False

    def update(self, delta_time: float = 1 / 60, *args, **kwargs):
        if self.jump_timer > 0:
            self.jump_timer -= delta_time

        grounded = self.window.engine.can_jump(y_distance=5)
        want_jump = self.jump or (self.jump_timer > 0)
        if want_jump and grounded:
            self.window.engine.jump(self.jump_power)
            self.jump_timer = 0

        if self.collides_with_list(self.window.objects):
            self.window.playing = False
            self.window.label.text = "Press SPACE to restart"


class Object(arcade.Sprite):
    def __init__(self, window, cords):
        super().__init__()
        self.window = window
        self.width, self.height = 50 * window.SIZE, 50 * window.SIZE
        self.center_x, self.center_y = cords


class Culcuraptor(arcade.Window):
    def __init__(self, size: float, difficulty: float):
        super().__init__(round(800 * size), round(600 * size))
        self.SIZE, self.DIFFICULTY = size, difficulty

        self.playing = False
        self.time_played = 0

        self.ground_level = 100 * self.SIZE
        self.ground, self.grounds = arcade.Sprite(), arcade.SpriteList()
        self.ground.center_x, self.ground.center_y = self.width / 2, self.ground_level / 2
        self.ground.width, self.ground.height = self.width, self.ground_level
        self.grounds.append(self.ground)

        self.player = Raptor(self)
        self.objects = arcade.SpriteList()
        self.sprites = arcade.SpriteList()
        self.sprites.append(self.player)

        self.object_timer = 0
        self.object_speed = 0
        self.object_a = self.DIFFICULTY / 10
        self.object_speed_limit = 15 * self.SIZE * self.DIFFICULTY

        self.object_types = {1: ",", 2: ",,", 3: ",,,", 4: "'", 5: "''", 6: "-", 7: ",'"}
        x, y = self.width, self.ground_level + 25 * self.SIZE
        self.types_to_obj_cords = {",": (x, y), "'": (x, y + 200 * self.SIZE), "-": (x, y + 150 * self.SIZE)}

        self.batch = Batch()
        self.label = arcade.Text("Press SPACE to start", 16, 16, arcade.color.GRAY, 14,
                                 batch=self.batch)

        self.engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player,
            gravity_constant=2 * self.SIZE,
            walls=self.grounds)

    def setup(self):
        self.playing = False
        self.time_played = 0

        self.object_timer = 15
        self.object_speed = 0

        self.player.center_x, self.player.center_y = self.width / 2, self.ground_level + self.player.height / 2

    def on_draw(self) -> EVENT_HANDLE_STATE:
        self.clear()
        arcade.draw_rect_filled(arcade.XYWH(self.width / 2, self.height / 2, self.width, self.height),
                                arcade.color.LIGHT_GRAY)
        arcade.draw_line(0, self.ground_level, self.width, self.ground_level, arcade.color.GRAY, 5)

        self.sprites.draw()

        self.batch.draw()

    def on_update(self, delta_time: float):
        if self.playing:

            if self.object_speed < self.object_speed_limit:
                self.object_speed += self.object_a * delta_time
            else:
                self.object_speed = self.object_speed_limit

            if self.object_timer <= 0:
                pass
            else:
                self.object_timer -= delta_time

            self.sprites.update()
            self.engine.update()

            self.time_played += delta_time
            self.label.text = f"Time: {round(self.time_played, 2)}"

    def on_key_press(self, symbol: int, modifiers: int) -> EVENT_HANDLE_STATE:
        if symbol == arcade.key.SPACE:
            if not self.playing:
                self.playing = True
                self.player.center_x = 100 * self.SIZE

                for obj in self.objects:
                    obj.kill()
                self.objects.clear()

            self.player.jump = True
            self.player.jump_timer = self.player.jump_timer_max

    def on_key_release(self, symbol: int, modifiers: int) -> EVENT_HANDLE_STATE:
        if symbol == arcade.key.SPACE:
            self.player.jump = False
            if self.player.change_y > 0:
                self.player.change_y *= 0.5


if __name__ == "__main__":
    game = Culcuraptor(SIZE, DIFFICULTY)
    game.setup()
    arcade.run()
