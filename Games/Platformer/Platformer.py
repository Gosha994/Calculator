import arcade
import random
import math

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Полоса препятствий"
GRAVITY = 0.8
JUMP_FORCE = 15
MOVE_SPEED = 5

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
    print("Open, code 0")

SIZE = int(SAVES["SIZE"])
DIFFICULTY = int(SAVES["DIFFICULTY"])
BALANCE = int(INVENTORY["BALANCE"])


class GameWindow(arcade.View):
    def __init__(self):
        global SIZE, DIFFICULTY, BALANCE
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
            print("Open, code 0")

        SIZE = int(SAVES["SIZE"])
        DIFFICULTY = int(SAVES["DIFFICULTY"])
        BALANCE = int(INVENTORY["BALANCE"])

        self.balance = BALANCE

        super().__init__()

        self.background_color = arcade.color.SKY_BLUE

        self.player = None
        self.player_list = arcade.SpriteList()
        self.player_x_vel = 0
        self.player_y_vel = 0
        self.is_on_ground = False
        self.on_moving_platform = None
        self.sound_player = None

        self.walk_textures = []
        self.current_texture = 0
        self.texture_timer = 0
        self.texture_change_speed = 0.1
        self.is_walking = False
        self.facing_right = True

        self.platform_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.bomb_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        self.coins_collected = 0
        self.total_coins = 0
        self.game_time = 0
        self.lives = 3

        self.coin_sound = None
        self.jump_sound = None
        self.hurt_sound = None

        self.particle_list = []

        self.left_pressed = False
        self.right_pressed = False

        self.level_width = 2000

        self.game_started = False
        self.game_over = False
        self.win = False

        self.camera_x = 0

        self.enemy_timer = 0
        self.enemy_spawn_time = 0

        self.finish_flag = None

        self.setup()

    def setup(self):
        for i in range(8):
            texture = arcade.load_texture(
                f":resources:images/animated_characters/female_adventurer/femaleAdventurer_walk{i}.png"
            )
            self.walk_textures.append(texture)

        self.player = arcade.Sprite()
        self.player.texture = self.walk_textures[0]
        self.player.scale = 0.5
        self.player.center_x = 100
        self.player.center_y = 200
        self.player.width = 40
        self.player.height = 80
        self.player_list.append(self.player)

        self.coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump3.wav")
        self.hurt_sound = arcade.load_sound(":resources:sounds/hurt3.wav")

        # Очистка списков при перезапуске
        self.platform_list.clear()
        self.coin_list.clear()
        self.bomb_list.clear()
        self.enemy_list.clear()
        self.particle_list.clear()

        for x in range(0, self.level_width, 64):
            platform = arcade.Sprite(":resources:images/tiles/grassMid.png", scale=0.5)
            platform.center_x = x
            platform.center_y = 32
            platform.width = 64
            platform.height = 64
            self.platform_list.append(platform)

        self.create_platforms()
        self.create_coins()
        self.create_obstacles()
        self.create_moving_platforms()
        self.create_start_and_finish()

        self.total_coins = len(self.coin_list)

    def create_platforms(self):
        box_positions = [
            (300, 150), (500, 200), (700, 250), (900, 180),
            (1100, 220), (1300, 170), (1500, 240), (1700, 190)
        ]

        for x, y in box_positions:
            platform = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", scale=0.5)
            platform.center_x = x
            platform.center_y = y
            platform.width = 64
            platform.height = 64
            self.platform_list.append(platform)

        stone_positions = [
            (350, 120), (850, 140), (1350, 120)
        ]

        for x, y in stone_positions:
            platform = arcade.Sprite(":resources:images/tiles/stoneCenter.png", scale=0.5)
            platform.center_x = x
            platform.center_y = y
            platform.width = 64
            platform.height = 64
            self.platform_list.append(platform)

    def create_coins(self):
        for platform in self.platform_list:
            if platform.center_y > 100:
                safe_x = platform.center_x
                safe_y = platform.center_y + 60

                if random.random() < 0.7:
                    coin = arcade.Sprite(":resources:images/items/coinGold.png", scale=0.5)
                    coin.center_x = safe_x
                    coin.center_y = safe_y
                    self.coin_list.append(coin)

        for i in range(10):
            coin = arcade.Sprite(":resources:images/items/coinGold.png", scale=0.4)

            attempts = 0
            placed = False

            while not placed and attempts < 50:
                coin.center_x = random.randint(200, self.level_width - 200)
                coin.center_y = random.randint(200, 450)

                too_close = False
                for platform in self.platform_list:
                    distance = math.sqrt(
                        (coin.center_x - platform.center_x) ** 2 +
                        (coin.center_y - platform.center_y) ** 2
                    )
                    if distance < 80:
                        too_close = True
                        break

                if not too_close:
                    coin.is_floating = True
                    coin.float_speed = random.uniform(-0.3, 0.3)
                    coin.float_range = random.randint(40, 80)
                    coin.original_y = coin.center_y
                    coin.float_timer = random.random() * 2
                    self.coin_list.append(coin)
                    placed = True

                attempts += 1

    def create_obstacles(self):
        bomb_positions = [
            600, 750, 900, 1050, 1200, 1350, 1500, 1650, 1800
        ]

        for x in bomb_positions:
            bomb = arcade.Sprite(":resources:images/tiles/bomb.png", scale=0.4)
            bomb.center_x = x
            bomb.center_y = 64
            bomb.width = 50
            bomb.height = 50
            bomb.rotation_speed = random.uniform(-2, 2)
            self.bomb_list.append(bomb)

        saw_positions = [(400, 300), (800, 350), (1200, 280), (1600, 320)]

        for x, y in saw_positions:
            saw = arcade.Sprite(":resources:images/tiles/lavaTop_high.png", scale=0.3)
            saw.center_x = x
            saw.center_y = y
            saw.change_x = random.uniform(-1, 1)
            saw.boundary_left = x - 50
            saw.boundary_right = x + 50
            saw.is_saw = True  # Маркируем как пилу
            self.bomb_list.append(saw)

    def create_moving_platforms(self):
        moving_platforms = [
            {"x": 400, "y": 120, "speed": 1.5, "range": 80},
            {"x": 700, "y": 150, "speed": -2, "range": 100},
            {"x": 1000, "y": 180, "speed": 1.8, "range": 70},
            {"x": 1200, "y": 100, "speed": 1, "range": 60}
        ]

        for mp in moving_platforms:
            platform = arcade.Sprite(":resources:images/tiles/grassHalf_mid.png", scale=0.5)
            platform.center_x = mp["x"]
            platform.center_y = mp["y"]
            platform.width = 64
            platform.height = 32
            platform.change_x = mp["speed"]
            platform.boundary_left = mp["x"] - mp["range"]
            platform.boundary_right = mp["x"] + mp["range"]
            platform.is_moving = True
            self.platform_list.append(platform)

    def create_start_and_finish(self):
        self.finish_flag = arcade.Sprite(":resources:images/tiles/signRight.png", scale=0.5)
        self.finish_flag.center_x = self.level_width - 100
        self.finish_flag.center_y = 300
        self.platform_list.append(self.finish_flag)

        finish_base = arcade.Sprite(":resources:images/tiles/stoneCenter.png", scale=0.5)
        finish_base.center_x = self.level_width - 150
        finish_base.center_y = 200
        finish_base.width = 64
        finish_base.height = 64
        self.platform_list.append(finish_base)

    def spawn_enemy(self):
        if len(self.enemy_list) < 2:
            enemy = arcade.Sprite(":resources:images/enemies/slimeBlue.png", scale=0.5)

            available_platforms = [p for p in self.platform_list if p.center_y > 100]
            if available_platforms:
                platform = random.choice(available_platforms)
                enemy.center_x = platform.center_x
                enemy.center_y = platform.center_y + 40
                enemy.change_x = random.choice([-1, 1]) * random.uniform(1, 2)
                enemy.boundary_left = platform.center_x - 100
                enemy.boundary_right = platform.center_x + 100
                self.enemy_list.append(enemy)

    def create_particle_effect(self, x, y, color, count=10):
        for _ in range(count):
            self.particle_list.append({
                'x': x,
                'y': y,
                'dx': random.uniform(-3, 3),
                'dy': random.uniform(-3, 3),
                'size': random.randint(3, 8),
                'life': random.uniform(0.5, 1.5),
                'max_life': random.uniform(0.5, 1.5),
                'color': color
            })

    def on_draw(self):
        self.clear()

        # Рисуем фон с учетом камеры
        arcade.draw_lrbt_rectangle_filled(
            self.camera_x, SCREEN_WIDTH + self.camera_x, 0, SCREEN_HEIGHT,
            arcade.color.SKY_BLUE
        )

        # Облака
        for i in range(3):
            cloud_x = (i * 400 + self.camera_x * 0.1) % (self.level_width + 800) - 400
            cloud_y = SCREEN_HEIGHT - 100 - i * 40

            arcade.draw_circle_filled(cloud_x, cloud_y, 30, arcade.color.WHITE)
            arcade.draw_circle_filled(cloud_x + 25, cloud_y + 10, 35, arcade.color.WHITE)
            arcade.draw_circle_filled(cloud_x + 50, cloud_y, 30, arcade.color.WHITE)

        # Частицы
        for particle in self.particle_list[:]:
            if 'dx' not in particle:
                continue
            life_ratio = particle['life'] / particle['max_life']
            # Ограничиваем альфа-канал в пределах 0-255
            alpha = int(255 * max(0, min(1, life_ratio)))
            arcade.draw_circle_filled(
                particle['x'] - self.camera_x, particle['y'],
                particle['size'],
                (particle['color'][0], particle['color'][1], particle['color'][2], alpha)
            )

        # Временные списки для отрисовки с учетом камеры
        temp_platform_list = arcade.SpriteList()
        temp_bomb_list = arcade.SpriteList()
        temp_enemy_list = arcade.SpriteList()
        temp_coin_list = arcade.SpriteList()
        temp_player_list = arcade.SpriteList()

        # Копируем и смещаем платформы
        for platform in self.platform_list:
            temp_platform = arcade.Sprite()
            temp_platform.texture = platform.texture
            temp_platform.scale = platform.scale
            temp_platform.center_x = platform.center_x - self.camera_x
            temp_platform.center_y = platform.center_y
            temp_platform.width = platform.width
            temp_platform.height = platform.height
            temp_platform_list.append(temp_platform)

        # Копируем и смещаем бомбы/пилы
        for bomb in self.bomb_list:
            temp_bomb = arcade.Sprite()
            temp_bomb.texture = bomb.texture
            temp_bomb.scale = bomb.scale
            temp_bomb.center_x = bomb.center_x - self.camera_x
            temp_bomb.center_y = bomb.center_y
            temp_bomb.width = bomb.width
            temp_bomb.height = bomb.height
            temp_bomb.angle = bomb.angle
            temp_bomb_list.append(temp_bomb)

        # Копируем и смещаем врагов
        for enemy in self.enemy_list:
            temp_enemy = arcade.Sprite()
            temp_enemy.texture = enemy.texture
            temp_enemy.scale = enemy.scale
            temp_enemy.center_x = enemy.center_x - self.camera_x
            temp_enemy.center_y = enemy.center_y
            temp_enemy.width = enemy.width
            temp_enemy.height = enemy.height
            temp_enemy_list.append(temp_enemy)

        # Копируем и смещаем монеты
        for coin in self.coin_list:
            temp_coin = arcade.Sprite()
            temp_coin.texture = coin.texture
            temp_coin.scale = coin.scale
            temp_coin.center_x = coin.center_x - self.camera_x
            temp_coin.center_y = coin.center_y
            temp_coin.width = coin.width
            temp_coin.height = coin.height
            temp_coin_list.append(temp_coin)

        # Копируем и смещаем игрока
        for player in self.player_list:
            temp_player = arcade.Sprite()
            temp_player.texture = player.texture
            temp_player.scale = player.scale
            temp_player.center_x = player.center_x - self.camera_x
            temp_player.center_y = player.center_y
            temp_player.width = player.width
            temp_player.height = player.height
            temp_player_list.append(temp_player)

        # Рисуем все временные списки
        temp_platform_list.draw()
        temp_bomb_list.draw()
        temp_enemy_list.draw()
        temp_coin_list.draw()
        temp_player_list.draw()

        # UI (без смещения камеры)
        self.draw_ui()

        if not self.game_started:
            self.draw_start_screen()
        elif self.game_over:
            self.player_list = arcade.SpriteList()
            self.draw_game_over_screen()
        elif self.win:
            self.player_list = arcade.SpriteList()
            self.draw_win_screen()

    def draw_ui(self):
        # Панель сверху
        arcade.draw_lrbt_rectangle_filled(0, SCREEN_WIDTH, SCREEN_HEIGHT - 50, SCREEN_HEIGHT,
                                          arcade.color.LIGHT_GRAY)

        arcade.draw_text(f"🟡: {self.coins_collected}/{self.total_coins}",
                         SCREEN_WIDTH // 25, SCREEN_HEIGHT - 140, arcade.color.YELLOW, 20)

        time_text = f"Время: {int(self.game_time)}с"
        arcade.draw_text(time_text, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 40,
                         arcade.color.BLACK, 20)

        lives_text = ("❤️" * self.lives) + ("🖤" * (3 - self.lives))
        arcade.draw_text(lives_text, SCREEN_WIDTH // 25, SCREEN_HEIGHT - 100,
                         arcade.color.WHITE, 20)

        # Прогресс-бар
        progress = min(1.0, self.player.center_x / self.level_width)
        arcade.draw_lrbt_rectangle_filled(50, SCREEN_WIDTH - 50, SCREEN_HEIGHT - 65, SCREEN_HEIGHT - 55,
                                          arcade.color.GRAY)
        arcade.draw_lrbt_rectangle_filled(50, 50 + progress * (SCREEN_WIDTH - 100),
                                          SCREEN_HEIGHT - 65, SCREEN_HEIGHT - 55,
                                          arcade.color.GREEN)

        if self.game_started and not self.game_over and not self.win:
            arcade.draw_text("A/D или ←/→ - Движение, Пробел - Прыжок",
                             SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40, arcade.color.BLACK, 16,
                             anchor_x="center")

            arcade.draw_text("Соберите все монеты и коснитесь стрелки стоя на камне чтобы пройти игру.",
                             SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20, arcade.color.BLACK, 16,
                             anchor_x="center")

    def draw_start_screen(self):
        arcade.draw_lrbt_rectangle_filled(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT,
                                          (0, 0, 0, 200))

        arcade.draw_text("ПОЛОСА ПРЕПЯТСТВИЙ", SCREEN_WIDTH // 2,
                         SCREEN_HEIGHT // 2 + 100, arcade.color.WHITE, 48,
                         anchor_x="center", bold=True)

        arcade.draw_text("Собери все монетки и достигни флага!",
                         SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30,
                         arcade.color.WHITE, 24, anchor_x="center")

        arcade.draw_text("Нажми ПРОБЕЛ чтобы начать",
                         SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50,
                         arcade.color.YELLOW, 28, anchor_x="center")

        arcade.draw_text("Управление: A/D или стрелки - движение, SPACE - прыжок",
                         SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120,
                         arcade.color.LIGHT_GRAY, 18, anchor_x="center")

    def draw_game_over_screen(self):
        self.player_list = arcade.SpriteList()
        arcade.draw_lrbt_rectangle_filled(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT,
                                          (0, 0, 0, 200))

        arcade.draw_text("ИГРА ОКОНЧЕНА", SCREEN_WIDTH // 2,
                         SCREEN_HEIGHT // 2 + 50, arcade.color.RED, 48,
                         anchor_x="center", bold=True)

        arcade.draw_text(f"Собрано монет: {self.coins_collected}/{self.total_coins}",
                         SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                         arcade.color.WHITE, 28, anchor_x="center")

        arcade.draw_text(f"Время: {int(self.game_time)} секунд",
                         SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50,
                         arcade.color.WHITE, 24, anchor_x="center")

        arcade.draw_text("Нажми R для перезапуска",
                         SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120,
                         arcade.color.YELLOW, 28, anchor_x="center")

    def draw_win_screen(self):
        arcade.draw_lrbt_rectangle_filled(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT,
                                          (0, 0, 0, 200))

        arcade.draw_text("ПОБЕДА!", SCREEN_WIDTH // 2,
                         SCREEN_HEIGHT // 2 + 100, arcade.color.GOLD, 64,
                         anchor_x="center", bold=True)

        arcade.draw_text(f"Вы собрали все {self.total_coins} монет!",
                         SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30,
                         arcade.color.WHITE, 32, anchor_x="center")

        arcade.draw_text(f"Затраченное время: {int(self.game_time)} секунд",
                         SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30,
                         arcade.color.WHITE, 24, anchor_x="center")

        score = self.coins_collected * 100 - int(self.game_time) * 10
        arcade.draw_text(f"Итоговый счет: {score}",
                         SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80,
                         arcade.color.GOLD, 36, anchor_x="center")

        arcade.draw_text("Нажми R для новой игры",
                         SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150,
                         arcade.color.YELLOW, 28, anchor_x="center")

    def update_animation(self, delta_time):
        if self.is_walking:
            self.texture_timer += delta_time
            if self.texture_timer >= self.texture_change_speed:
                self.texture_timer = 0
                self.current_texture += 1
                if self.current_texture >= len(self.walk_textures):
                    self.current_texture = 0

                texture = self.walk_textures[self.current_texture]
                if not self.facing_right:
                    texture = texture.flip_horizontally()
                self.player.texture = texture
        else:
            texture = self.walk_textures[0]
            if not self.facing_right:
                texture = texture.flip_horizontally()
            self.player.texture = texture

    def check_collision_with_platforms(self):
        self.is_on_ground = False
        self.on_moving_platform = None

        ground_level = 64
        if self.player.center_y - self.player.height / 2 <= ground_level:
            self.player.center_y = ground_level + self.player.height / 2
            self.player_y_vel = 0
            self.is_on_ground = True
            return

        for platform in self.platform_list:
            if platform.center_y == 32:
                continue

            # Простая проверка AABB коллизии
            if (self.player.center_x + self.player.width / 2 > platform.center_x - platform.width / 2 and
                    self.player.center_x - self.player.width / 2 < platform.center_x + platform.width / 2 and
                    self.player.center_y + self.player.height / 2 > platform.center_y - platform.height / 2 and
                    self.player.center_y - self.player.height / 2 < platform.center_y + platform.height / 2):

                # Проверяем, падает ли игрок на платформу сверху
                if (self.player.center_y > platform.center_y and
                        self.player_y_vel <= 0 and
                        abs(self.player.center_y - platform.center_y - platform.height / 2 - self.player.height / 2) < 10):

                    self.player.center_y = platform.center_y + platform.height / 2 + self.player.height / 2
                    self.player_y_vel = 0
                    self.is_on_ground = True

                    if hasattr(platform, 'is_moving') and platform.is_moving:
                        self.on_moving_platform = platform
                    break

    def on_update(self, delta_time):

        if not self.game_started or self.game_over or self.win:
            return

        self.game_time += delta_time

        self.player_y_vel -= GRAVITY

        self.player_x_vel = 0
        if self.left_pressed and not self.right_pressed:
            self.player_x_vel = -MOVE_SPEED
            self.is_walking = True
            self.facing_right = False
        elif self.right_pressed and not self.left_pressed:
            self.player_x_vel = MOVE_SPEED
            self.is_walking = True
            self.facing_right = True
        else:
            self.is_walking = False

        platform_x_vel = 0
        if self.on_moving_platform:
            platform_x_vel = self.on_moving_platform.change_x

        self.player.center_x += self.player_x_vel + platform_x_vel
        self.player.center_y += self.player_y_vel

        self.update_camera()

        if self.player.center_x < 20:
            self.player.center_x = 20
        if self.player.center_x > self.level_width - 20:
            self.player.center_x = self.level_width - 20

        self.update_animation(delta_time)

        # Обновление движущихся платформ
        for platform in self.platform_list:
            if hasattr(platform, 'is_moving') and platform.is_moving:
                platform.center_x += platform.change_x
                if platform.center_x < platform.boundary_left:
                    platform.center_x = platform.boundary_left
                    platform.change_x = -platform.change_x
                elif platform.center_x > platform.boundary_right:
                    platform.center_x = platform.boundary_right
                    platform.change_x = -platform.change_x

        # Обновление плавающих монет
        for coin in self.coin_list:
            if hasattr(coin, 'is_floating') and coin.is_floating:
                coin.float_timer += delta_time
                coin.center_y = coin.original_y + math.sin(coin.float_timer) * coin.float_range

        # Спавн врагов
        self.enemy_timer += delta_time
        if self.enemy_timer >= self.enemy_spawn_time:
            self.spawn_enemy()
            self.enemy_timer = 0

        # Обновление врагов
        for enemy in self.enemy_list:
            enemy.center_x += enemy.change_x
            if enemy.center_x < enemy.boundary_left:
                enemy.center_x = enemy.boundary_left
                enemy.change_x = -enemy.change_x
            elif enemy.center_x > enemy.boundary_right:
                enemy.center_x = enemy.boundary_right
                enemy.change_x = -enemy.change_x

        # Обновление бомб/пил
        for bomb in self.bomb_list:
            if hasattr(bomb, 'rotation_speed'):
                bomb.angle += bomb.rotation_speed

            # Обновляем только пилы (у них есть change_x и boundary_left)
            if hasattr(bomb, 'is_saw') and bomb.is_saw:
                bomb.center_x += bomb.change_x
                if hasattr(bomb, 'boundary_left') and bomb.center_x < bomb.boundary_left:
                    bomb.center_x = bomb.boundary_left
                    bomb.change_x = -bomb.change_x
                elif hasattr(bomb, 'boundary_right') and bomb.center_x > bomb.boundary_right:
                    bomb.center_x = bomb.boundary_right
                    bomb.change_x = -bomb.change_x

        # Обновление частиц
        particles_to_remove = []
        for i, particle in enumerate(self.particle_list):
            if 'dx' in particle:
                particle['x'] += particle['dx'] * delta_time * 60
                particle['y'] += particle['dy'] * delta_time * 60
                particle['life'] -= delta_time

                if particle['life'] <= 0:
                    particles_to_remove.append(i)

        for i in sorted(particles_to_remove, reverse=True):
            self.particle_list.pop(i)

        self.check_collision_with_platforms()

        # Сбор монет
        coins_hit = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in coins_hit:
            coin.remove_from_sprite_lists()
            self.coins_collected += 1
            self.create_particle_effect(coin.center_x, coin.center_y,
                                        arcade.color.GOLD, 8)
            arcade.play_sound(self.coin_sound)

        # Столкновение с врагами
        enemies_hit = arcade.check_for_collision_with_list(self.player, self.enemy_list)
        if enemies_hit:
            self.lives -= 1
            self.create_particle_effect(self.player.center_x, self.player.center_y,
                                        arcade.color.RED, 15)
            arcade.play_sound(self.hurt_sound)

            for enemy in enemies_hit:
                enemy.remove_from_sprite_lists()

            if self.lives <= 0:
                self.game_over = True
            else:
                self.player.center_x = 100
                self.player.center_y = 200
                self.player_y_vel = 0
                self.on_moving_platform = None

        # Столкновение с бомбами/пилами
        bombs_hit = arcade.check_for_collision_with_list(self.player, self.bomb_list)
        if bombs_hit:
            self.lives -= 1
            self.create_particle_effect(self.player.center_x, self.player.center_y,
                                        arcade.color.ORANGE_RED, 20)
            arcade.play_sound(self.hurt_sound)

            if self.lives <= 0:
                self.game_over = True
            else:
                self.player.center_x = 100
                self.player.center_y = 200
                self.player_y_vel = 0
                self.on_moving_platform = None

        # Проверка финиша
        if self.finish_flag and (abs(self.player.center_x - self.finish_flag.center_x) < 50 and
                                 abs(self.player.center_y - self.finish_flag.center_y) < 50):
            if self.coins_collected >= self.total_coins:
                self.win = True
                self.create_particle_effect(self.finish_flag.center_x,

                                            self.finish_flag.center_y + 50,
                                            arcade.color.GOLD, 30)

        # Падение в пропасть
        if self.player.center_y < -100:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            else:
                self.player.center_x = 100
                self.player.center_y = 200
                self.player_y_vel = 0
                self.on_moving_platform = None

    def update_camera(self):
        target_x = self.player.center_x - SCREEN_WIDTH // 2
        self.camera_x = max(0, min(target_x, self.level_width - SCREEN_WIDTH))

    def on_key_press(self, key, modifiers):
        if not self.game_started:
            if key == arcade.key.SPACE:
                self.game_started = True
                self.sound = arcade.load_sound(":resources:music/funkyrobot.mp3", streaming=True)
                self.sound_player = arcade.play_sound(self.sound, volume=1, pan=0.0, loop=True)
            return

        if self.game_over or self.win:
            if key == arcade.key.R:
                self.setup()
                self.game_started = True
                self.game_over = False
                self.win = False
                self.lives = 3
                self.coins_collected = 0
                self.game_time = 0
                self.left_pressed = False
                self.right_pressed = False
                arcade.stop_sound(self.sound_player)
                self.sound = arcade.load_sound(":resources:music/funkyrobot.mp3", streaming=True)
                self.sound_player = arcade.play_sound(self.sound, volume=1, pan=0.0, loop=True)
            return

        if key in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = True
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = True
        elif key == arcade.key.SPACE or key == arcade.key.W:
            if self.is_on_ground:
                self.player_y_vel = JUMP_FORCE
                self.is_on_ground = False
                self.on_moving_platform = None
                arcade.play_sound(self.jump_sound)

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = False
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = False

    def on_close(self):
        # Останавливаем музыку, чтобы она не ушла в главное меню

        if self.win:
            self.balance += int(self.total_coins) * int(DIFFICULTY) * 10
        INVENTORY["BALANCE"] = self.balance
        # Сохраняем в файл
        try:
            with open("inventory", "w", encoding="utf-8") as file:
                lines = []
                for key, value in INVENTORY.items():
                    lines.append(f"{key} = {value}")
                file.write("\n".join(lines))
            print("Save, code 0")
        except Exception as e:
            print(f"Ошибка при сохранении баланса: {e}")

        # Сохранение настроек
        SAVES["IS_GAME_STARTED"] = False
        try:
            with open("setup", "w", encoding="utf-8") as file:
                lines = []
                for key, value in SAVES.items():
                    lines.append(f"{key} = {value}")
                file.write("".join(lines))
            print("Save, code 0")
        except Exception as e:
            print(f"Ошибка при сохранении настроек: {e}")

        arcade.close_window()
        arcade.stop_sound(self.sound_player)
        super().on_close()


if __name__ == "__main__":
    window = GameWindow()
    window.setup()
    arcade.run()
