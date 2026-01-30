import arcade
import random
import math

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Полоса препятствий"
GRAVITY = 0.8
JUMP_FORCE = 15
MOVE_SPEED = 5


class GameWindow(arcade.Window):
    def init(self):
        super().init(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.background_color = arcade.color.SKY_BLUE

        # Игрок
        self.player = None
        self.player_list = arcade.SpriteList()
        self.player_x_vel = 0
        self.player_y_vel = 0
        self.is_on_ground = False
        self.on_moving_platform = None

        # Анимация ходьбы
        self.walk_textures = []
        self.current_texture = 0
        self.texture_timer = 0
        self.texture_change_speed = 0.1
        self.is_walking = False
        self.facing_right = True

        # Платформы
        self.platform_list = arcade.SpriteList()

        # Монетки
        self.coin_list = arcade.SpriteList()

        # Препятствия
        self.bomb_list = arcade.SpriteList()

        # Враги
        self.enemy_list = arcade.SpriteList()

        # Счет и время
        self.coins_collected = 0
        self.total_coins = 0
        self.game_time = 0
        self.lives = 3

        # Звуки
        self.coin_sound = None
        self.jump_sound = None
        self.hurt_sound = None

        # Эффекты частиц
        self.particle_list = arcade.ShapeElementList()

        # Управление
        self.left_pressed = False
        self.right_pressed = False

        # Границы уровня
        self.level_width = 2500

        # Состояние игры
        self.game_started = False
        self.game_over = False
        self.win = False

        # Камера
        self.camera_x = 0

        # Таймеры для врагов
        self.enemy_timer = 0
        self.enemy_spawn_time = 3.0

    def setup(self):
        # Загружаем анимацию ходьбы
        for i in range(8):
            texture = arcade.load_texture(
                f":resources:images/animated_characters/female_adventurer/femaleAdventurer_walk{i}.png"
            )
            self.walk_textures.append(texture)

        # Создаем игрока
        self.player = arcade.Sprite()
        self.player.texture = self.walk_textures[0]
        self.player.scale = 0.5
        self.player.center_x = 100
        self.player.center_y = 200
        self.player.width = 40
        self.player.height = 80
        self.player_list.append(self.player)

        # Загружаем звуки
        self.coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump3.wav")
        self.hurt_sound = arcade.load_sound(":resources:sounds/hurt3.wav")

        # Создаем землю
        for x in range(0, self.level_width, 64):
            platform = arcade.Sprite(":resources:images/tiles/grassMid.png", scale=0.5)
            platform.center_x = x
            platform.center_y = 32
            platform.width = 64
            platform.height = 64
            self.platform_list.append(platform)

        # Создаем разные типы платформ
        self.create_platforms()

        # Создаем монетки
        self.create_coins()

        # Создаем препятствия
        self.create_obstacles()

        # Создаем движущиеся платформы
        self.create_moving_platforms()

        # Создаем стартовую и конечную точки
        self.create_start_and_finish()

        # Создаем эффекты частиц для фона
        self.create_background_particles()

        # Инициализируем общее количество монет
        self.total_coins = len(self.coin_list)

    def create_platforms(self):
        """Создаем различные платформы"""
        # Коробки
        box_positions = [
            (300, 150), (500, 200), (700, 250), (900, 180),
            (1100, 220), (1300, 170), (1500, 240), (1700, 190),
            (1900, 160), (2100, 210), (2300, 180)
        ]

        for x, y in box_positions:
            platform = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", scale=0.5)
            platform.center_x = x
            platform.center_y = y
            platform.width = 64
            platform.height = 64
            self.platform_list.append(platform)

        # Камни
        stone_positions = [
            (350, 120), (850, 140), (1350, 120), (1850, 100)
        ]

        for x, y in stone_positions:
            platform = arcade.Sprite(":resources:images/tiles/stoneCenter.png", scale=0.5)
            platform.center_x = x
            platform.center_y = y
            platform.width = 64
            platform.height = 64
            self.platform_list.append(platform)

    def create_coins(self):
        """Создаем монетки"""
        # Монетки над платформами
        for platform in self.platform_list:
            if platform.center_y > 100:
                # Проверяем, не слишком ли близко к краю платформы
                safe_x = platform.center_x
                safe_y = platform.center_y + 60

                # Добавляем несколько монеток над некоторыми платформами
                if random.random() < 0.7:  # 70% шанс
                    coin = arcade.Sprite(":resources:images/items/coinGold.png", scale=0.5)
                    coin.center_x = safe_x
                    coin.center_y = safe_y
                    self.coin_list.append(coin)

        # Летающие монетки
        for i in range(15):
            coin = arcade.Sprite(":resources:images/items/coinGold.png", scale=0.4)

            # Ищем безопасное место
            attempts = 0
            placed = False

            while not placed and attempts < 50:
                coin.center_x = random.randint(200, self.level_width - 200)
                coin.center_y = random.randint(200, 450)

                # Проверяем расстояние до платформ
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
        """Создаем препятствия"""
        # Бомбы
        bomb_positions = [
            600, 750, 900, 1050, 1200, 1350, 1500,
            1650, 1800, 1950, 2100, 2250
        ]

        for x in bomb_positions:
            bomb = arcade.Sprite(":resources:images/tiles/bomb.png", scale=0.4)
            bomb.center_x = x
            bomb.center_y = 64
            bomb.width = 50
            bomb.height = 50
            bomb.rotation_speed = random.uniform(-2, 2)
            self.bomb_list.append(bomb)

        # Пилы (дополнительные препятствия)
        saw_positions = [(400, 300), (800, 350), (1200, 280), (1600, 320), (2000, 290)]

        for x, y in saw_positions:
            saw = arcade.Sprite(":resources:images/tiles/lavaTop_high.png", scale=0.3)
            saw.center_x = x
            saw.center_y = y
            saw.change_x = random.uniform(-1, 1)
            saw.boundary_left = x - 50
            saw.boundary_right = x + 50
            self.bomb_list.append(saw)

    def create_moving_platforms(self):
        """Создаем движущиеся платформы"""
        moving_platforms = [
            {"x": 400, "y": 120, "speed": 1.5, "range": 80},
            {"x": 700, "y": 150, "speed": -2, "range": 100},
            {"x": 1000, "y": 180, "speed": 1.8, "range": 70},
            {"x": 1200, "y": 100, "speed": 1, "range": 60},
            {"x": 1600, "y": 140, "speed": -1.5, "range": 90},
            {"x": 1900, "y": 160, "speed": 2, "range": 80},
            {"x": 2200, "y": 120, "speed": -1.2, "range": 70}
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
        """Создаем стартовую и конечную точки"""
        # Стартовая платформа
        start_platform = arcade.Sprite(":resources:images/tiles/signExit.png", scale=0.5)
        start_platform.center_x = 100
        start_platform.center_y = 64
        self.platform_list.append(start_platform)

        # Финальная платформа
        self.finish_flag = arcade.Sprite(":resources:images/tiles/signRight.png", scale=0.5)
        self.finish_flag.center_x = self.level_width - 100
        self.finish_flag.center_y = 300
        self.platform_list.append(self.finish_flag)

        # Платформа под флагом
        finish_base = arcade.Sprite(":resources:images/tiles/stoneCenter.png", scale=0.5)
        finish_base.center_x = self.level_width - 100
        finish_base.center_y = 200
        finish_base.width = 64
        finish_base.height = 64
        self.platform_list.append(finish_base)

    def create_background_particles(self):
        """Создаем частицы для фона"""
        for _ in range(20):
            x = random.randint(0, self.level_width)
            y = random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT - 50)
            size = random.randint(2, 5)
            speed = random.uniform(0.1, 0.5)

            particle = arcade.shape_list.create_ellipse_filled(
                x, y, size, size, arcade.color.LIGHT_BLUE
            )
            particle.speed = speed
            particle.original_x = x
            self.particle_list.append(particle)

    def spawn_enemy(self):
        """Создаем врага"""
        if len(self.enemy_list) < 3:  # Не более 3 врагов одновременно
            enemy = arcade.Sprite(":resources:images/enemies/slimeBlue.png", scale=0.5)

            # Размещаем врага на случайной платформе
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
        """Создаем эффект частиц"""
        for _ in range(count):
            size = random.randint(3, 8)
            dx = random.uniform(-3, 3)
            dy = random.uniform(-3, 3)
            life = random.uniform(0.5, 1.5)

            particle = arcade.shape_list.create_ellipse_filled(
                x, y, size, size, color
            )
            particle.dx = dx
            particle.dy = dy
            particle.life = life
            particle.max_life = life
            self.particle_list.append(particle)

    def on_draw(self):
        self.clear()

        # Рисуем фон
        arcade.draw_lrbt_rectangle_filled(
            0, self.level_width, 0, SCREEN_HEIGHT,
            arcade.color.SKY_BLUE
        )

        # Рисуем облака на заднем плане
        self.draw_background()

        # Смещаем все для камеры
        arcade.push_state()
        arcade.translate(-self.camera_x, 0)

        # Рисуем игровые объекты
        self.platform_list.draw()
        self.bomb_list.draw()
        self.enemy_list.draw()
        self.coin_list.draw()
        self.player_list.draw()
        self.particle_list.draw()

        arcade.pop_state()

        # Рисуем интерфейс
        self.draw_ui()

        # Рисуем экраны состояний
        if not self.game_started:
            self.draw_start_screen()
        elif self.game_over:
            self.draw_game_over_screen()
        elif self.win:
            self.draw_win_screen()

    def draw_background(self):
        """Рисуем фон с облаками"""
        # Облака на заднем плане (медленно движутся)
        for i in range(5):
            cloud_x = (i * 400 + self.camera_x * 0.1) % (self.level_width + 800) - 400
            cloud_y = SCREEN_HEIGHT - 100 - i * 40

            arcade.draw_circle_filled(cloud_x, cloud_y, 30, arcade.color.WHITE)
            arcade.draw_circle_filled(cloud_x + 25, cloud_y + 10, 35, arcade.color.WHITE)
            arcade.draw_circle_filled(cloud_x + 50, cloud_y, 30, arcade.color.WHITE)
            arcade.draw_circle_filled(cloud_x + 25, cloud_y - 10, 25, arcade.color.WHITE)

    def draw_ui(self):
        """Рисуем пользовательский интерфейс"""
        # Панель статистики
        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 25,
                                     SCREEN_WIDTH, 50, arcade.color.LIGHT_GRAY)

        # Счет
        arcade.draw_text(f"Монеты: {self.coins_collected}/{self.total_coins}",
                         20, SCREEN_HEIGHT - 40, arcade.color.BLACK, 20)

        # Время
        time_text = f"Время: {int(self.game_time)}с"
        arcade.draw_text(time_text, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 40,
                         arcade.color.BLACK, 20)

        # Жизни
        lives_text = f"Жизни: {self.lives}"
        arcade.draw_text(lives_text, SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 40,
                         arcade.color.BLACK, 20)

        # Прогресс
        progress = min(1.0, self.player.center_x / self.level_width)
        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60,
                                     SCREEN_WIDTH - 100, 10, arcade.color.GRAY)
        arcade.draw_rectangle_filled(50 + progress * (SCREEN_WIDTH - 100),
                                     SCREEN_HEIGHT - 60,
                                     progress * (SCREEN_WIDTH - 100), 10,
                                     arcade.color.GREEN)

        # Подсказки управления
        if self.game_started and not self.game_over and not self.win:
            arcade.draw_text("A/D или ←/→ - Движение, SPACE - Прыжок",
                             SCREEN_WIDTH // 2, 30, arcade.color.DARK_GRAY, 16,
                             anchor_x="center")

            def draw_start_screen(self):
                """Рисуем стартовый экран"""
                arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                             SCREEN_WIDTH, SCREEN_HEIGHT,
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
                """Рисуем экран проигрыша"""
                arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                             SCREEN_WIDTH, SCREEN_HEIGHT,
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
        """Рисуем экран победы"""
        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                     SCREEN_WIDTH, SCREEN_HEIGHT,
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

                # Проверяем землю
                ground_level = 64
                if self.player.center_y - self.player.height / 2 <= ground_level:
                    self.player.center_y = ground_level + self.player.height / 2
                    self.player_y_vel = 0
                    self.is_on_ground = True
                    return

                # Проверяем другие платформы
                for platform in self.platform_list:
                    if platform.center_y == 32:
                        continue

                    player_bottom = self.player.center_y - self.player.height / 2
                    platform_top = platform.center_y + platform.height / 2

                    player_above_platform = (
                            self.player.center_x > platform.center_x - platform.width / 2 and
                            self.player.center_x < platform.center_x + platform.width / 2 and
                            player_bottom <= platform_top + 5 and
                            player_bottom >= platform_top - 15 and
                            self.player_y_vel <= 0
                    )

                    if player_above_platform:
                        self.player.center_y = platform_top + self.player.height / 2
                        self.player_y_vel = 0
                        self.is_on_ground = True

                        if hasattr(platform, 'is_moving') and platform.is_moving:
                            self.on_moving_platform = platform
                        break

    def on_update(self, delta_time):
        if not self.game_started or self.game_over or self.win:
            return

        # Обновляем время игры
        self.game_time += delta_time

        # Гравитация
        self.player_y_vel -= GRAVITY

        # Движение игрока
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

        # Движение с платформой
        platform_x_vel = 0
        if self.on_moving_platform:
            platform_x_vel = self.on_moving_platform.change_x

        # Обновляем позицию игрока
        self.player.center_x += self.player_x_vel + platform_x_vel
        self.player.center_y += self.player_y_vel

        # Обновляем камеру
        self.update_camera()

        # Границы уровня
        if self.player.center_x < 20:
            self.player.center_x = 20
        if self.player.center_x > self.level_width - 20:
            self.player.center_x = self.level_width - 20

        # Обновляем анимацию
        self.update_animation(delta_time)

        # Обновляем движущиеся платформы
        for platform in self.platform_list:
            if hasattr(platform, 'is_moving') and platform.is_moving:
                platform.center_x += platform.change_x
                if platform.center_x < platform.boundary_left:
                    platform.center_x = platform.boundary_left
                    platform.change_x = -platform.change_x
                elif platform.center_x > platform.boundary_right:
                    platform.center_x = platform.boundary_right
                    platform.change_x = -platform.change_x

                    # Обновляем летающие монетки
                for coin in self.coin_list:
                    if hasattr(coin, 'is_floating') and coin.is_floating:
                        coin.float_timer += delta_time
                        coin.center_y = coin.original_y + math.sin(
                            coin.float_timer) * coin.float_range

                    # Обновляем врагов
                self.enemy_timer += delta_time
                if self.enemy_timer >= self.enemy_spawn_time:
                    self.spawn_enemy()
                    self.enemy_timer = 0

                for enemy in self.enemy_list:
                    enemy.center_x += enemy.change_x
                    if enemy.center_x < enemy.boundary_left:
                        enemy.center_x = enemy.boundary_left
                        enemy.change_x = -enemy.change_x
                        enemy.texture = enemy.texture.flip_horizontally()
                    elif enemy.center_x > enemy.boundary_right:
                        enemy.center_x = enemy.boundary_right
                        enemy.change_x = -enemy.change_x
                        enemy.texture = enemy.texture.flip_horizontally()

                # Обновляем бомбы
                for bomb in self.bomb_list:
                    if hasattr(bomb, 'rotation_speed'):
                        bomb.angle += bomb.rotation_speed

                    if hasattr(bomb, 'change_x'):
                        bomb.center_x += bomb.change_x
                        if bomb.center_x < bomb.boundary_left:
                            bomb.center_x = bomb.boundary_left
                            bomb.change_x = -bomb.change_x
                        elif bomb.center_x > bomb.boundary_right:
                            bomb.center_x = bomb.boundary_right
                            bomb.change_x = -bomb.change_x

                # Обновляем частицы
                particles_to_remove = []
                for particle in self.particle_list:
                    if hasattr(particle, 'speed'):
                        particle.center_x = (
                                                    particle.original_x + self.camera_x * 0.05) % self.level_width

                    if hasattr(particle, 'dx'):
                        particle.center_x += particle.dx * delta_time * 60
                        particle.center_y += particle.dy * delta_time * 60
                        particle.life -= delta_time

                        # Прозрачность по времени жизни
                        if hasattr(particle, 'max_life'):
                            alpha = int(255 * (particle.life / particle.max_life))
                            particle.color = (particle.color[0], particle.color[1],
                                              particle.color[2], alpha)

                        if particle.life <= 0:
                            particles_to_remove.append(particle)

                for particle in particles_to_remove:
                    particle.remove_from_sprite_lists()

                # Проверяем столкновения
                self.check_collision_with_platforms()

                # Сбор монеток
                coins_hit = arcade.check_for_collision_with_list(self.player, self.coin_list)
                for coin in coins_hit:
                    coin.remove_from_sprite_lists()
                    self.coins_collected += 1
                    self.create_particle_effect(coin.center_x, coin.center_y,
                                                arcade.color.GOLD, 8)
                    arcade.play_sound(self.coin_sound)

                # Столкновения с врагами
                enemies_hit = arcade.check_for_collision_with_list(self.player, self.enemy_list)
                if enemies_hit:
                    self.lives -= 1
                    self.create_particle_effect(self.player.center_x, self.player.center_y,
                                                arcade.color.RED, 15)
                    arcade.play_sound(self.hurt_sound)

                    # Удаляем всех врагов при столкновении
                    for enemy in enemies_hit:
                        enemy.remove_from_sprite_lists()

                        if self.lives <= 0:
                            self.game_over = True
                        else:
                            # Респавн игрока
                            self.player.center_x = 100
                            self.player.center_y = 200
                            self.player_y_vel = 0
                            self.on_moving_platform = None

                        # Столкновения с бомбами
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

                    # Проверяем достижение флага
                    if (abs(self.player.center_x - self.finish_flag.center_x) < 50 and
                            abs(self.player.center_y - self.finish_flag.center_y) < 50):
                        if self.coins_collected >= self.total_coins:
                            self.win = True
                            self.create_particle_effect(self.finish_flag.center_x,
                                                        self.finish_flag.center_y + 50,
                                                        arcade.color.GOLD, 30)

                    # Проверяем падение
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
        """Обновляем положение камеры"""
        target_x = self.player.center_x - SCREEN_WIDTH // 2
        self.camera_x = max(0, min(target_x, self.level_width - SCREEN_WIDTH))

    def on_key_press(self, key, modifiers):
        if not self.game_started:
            if key == arcade.key.SPACE:
                self.game_started = True
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
            return

        if key in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = True
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = True
        elif key == arcade.key.SPACE:
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

def main():
    window = GameWindow()
    window.setup()
    arcade.run()

if __name__ == "main":
        main()
