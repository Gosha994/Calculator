import sys
import random

import PyQt6
from PyQt6.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from random import randint
from TitleBar import CustomTitleBar

# Открываем сохранённый результат

with open("Games/MiniGamesAssets/MiniGamesSaves") as file:
    setting = file.readlines()
    SAVES = {}
    for elem in setting:
        SAVES[f"{elem.split(": ")[0]}"] = elem.split()[1]


class Gamble(QWidget):
    def __init__(self, parent_calculator=None, parent_pos=None, parent_size=None, run=False):
        if not run:
            self.parent.close()
            QApplication.quit()
        self.sou = int(SAVES["GAMBLE_BOXES"])
        self.buz = int(SAVES["GAMBLE_BUZ_SAUSAGE"])
        self.balance = int(SAVES["GAMBLE_BALANCE"])
        self.parent_calculator = parent_calculator  # Сохраняем ссылку на калькулятор
        self.parent_pos = parent_pos
        self.parent_size = parent_size
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Сэчуанский Соус!")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.setFixedSize(370, 580)
        self.setStyleSheet("background-color: #1a1a1a;")

        if self.parent_pos:
            self.move(self.parent_pos)

        # Создаем основной layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)

        # ВАЖНО: Добавляем "растягиватель", чтобы title bar оставался вверху
        main_layout.addStretch(1)

        # Устанавливаем layout для окна
        self.setLayout(main_layout)

        # Стиль текста
        self.text_style = """
                    QLabel {
                        background-color: #323232;
                        color: white;
                        font-size: 18px;
                        font-weight: 600;
                        font-family: "Segoe UI";
                        border-radius: 10px;
                        padding: 5px;
                        border: none;
                        selection-background-color: #505050;
                    }
                """

        if self.balance > -10:
            self.button = QPushButton("Коробочка с соусом! Жми!", self)
            self.button.move(25, 80)
            self.button.resize(250, 60)
            self.button.clicked.connect(self.btc)
            self.button.setStyleSheet(f"background-color: #{str(random.randint(100000, 999999))}")
        else:
            self.button = QPushButton("Продать колбасы", self)
            self.button.move(25, 80)
            self.button.resize(250, 60)
            self.button.clicked.connect(self.b_plus)
            self.button.setStyleSheet(f"background-color: #{str(random.randint(100000, 999999))}")

        self.lable_buz = QLabel(f"Бузулукский\nколбас: {self.buz}", self)
        self.lable_buz.move(25, 500)
        self.lable_buz.resize(150, 60)
        self.lable_buz.setStyleSheet(self.text_style)

        self.lable_sou = QLabel(f"Коробочка\nсоуса: {self.buz}", self)
        self.lable_sou.move(190, 500)
        self.lable_sou.resize(150, 60)
        self.lable_sou.setStyleSheet(self.text_style)

        self.lable_balance = QLabel(f"Баланс: {self.balance}", self)
        self.lable_balance.move(10, 40)
        self.lable_balance.resize(350, 30)
        self.lable_balance.setStyleSheet(self.text_style)

        # ДОБАВЛЯЕМ КНОПКУ ВОЗВРАТА В КАЛЬКУЛЯТОР
        self.back_button = QPushButton("Вернуться в калькулятор", self)
        self.back_button.move(150, 8)  # Позиция вверху
        self.back_button.resize(150, 25)
        self.back_button.clicked.connect(self.return_to_calculator)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #404040;
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 12px;
                font-weight: 400;
                font-family: "Segoe UI";
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QPushButton:pressed {
                background-color: #303030;
            }
        """)

        button_style = """
                    QPushButton {
                        background-color: #323232;
                        color: white;
                        border: none;
                        border-radius: 5px;
                        font-size: 16px;
                        font-weight: 600;
                        font-family: "Segoe UI";
                        padding: 12px;
                        margin: 5px;
                    }
                    QPushButton:hover {
                        background-color: #404040;
                        border: 1px solid #505050;
                    }
                    QPushButton:pressed {
                        background-color: #282828;
                    }
                """
        self.button.setStyleSheet(button_style)

    def return_to_calculator(self):
        """Возвращаемся в калькулятор"""
        if self.parent_calculator:
            # Передаем текущую позицию игры калькулятору
            game_position = self.pos()
            self.parent_calculator.move(game_position)  # Калькулятор наследует позицию игры
            self.parent_calculator.show()
            self.parent_calculator.activateWindow()
        self.close()

    def closeEvent(self, event):
        """Обрабатываем закрытие окна игры (крестиком)"""
        if self.parent_calculator:
            # При закрытии крестиком тоже передаем позицию
            game_position = self.pos()
            self.parent_calculator.move(game_position)
            self.parent_calculator.show()
            self.parent_calculator.activateWindow()
        event.accept()

    def btc(self):
        if not self.balance <= -10:
            if random.randint(0, 89) == 0:  # Шанс
                self.balance += random.randint(25, 75)
                self.sou += 1
                self.lable_sou.setText(f"Коробочка\nсоуса: {self.sou}")
                self.lable_balance.setText(f"Баланс: {self.balance}₽")
            else:
                self.balance -= 1
                self.lable_balance.setText(f"Баланс: {self.balance}₽")
                if self.balance > -10:
                    self.buz += 1
                    self.lable_buz.setText(f"Бузулукский\nколбас: {self.buz}")
                    self.lable_balance.setText(f"Баланс: {self.balance}₽")
                else:
                    self.button.setText("Продать колбасы")
                    self.button.clicked.disconnect()
                    self.button.clicked.connect(self.b_plus)

            self.button.move(random.randint(10, 50), (random.randint(80, 440)))
            self.button.setStyleSheet(f"""
                            QPushButton {{
                                background-color: #{str(random.randint(100000, 999999))};
                                color: white;
                                border: none;
                                border-radius: 5px;
                                font-size: 16px;
                                font-weight: 600;
                                font-family: "Segoe UI";
                                padding: 12px;
                                margin: 5px;
                            }}
                            QPushButton:hover {{
                                background-color: #404040;
                                border: 1px solid #505050;
                            }}
                            QPushButton:pressed {{
                                background-color: #282828;
                            }}
                        """)
        SAVES["GAMBLE_BOXES"] = str(self.sou)
        SAVES["GAMBLE_BUZ_SAUSAGE"] = str(self.buz)
        SAVES["GAMBLE_BALANCE"] = str(self.balance)

        with open("Games/MiniGamesAssets/MiniGamesSaves", 'w', encoding='utf-8') as file2:
            lines = []
            for key, value in SAVES.items():
                lines.append(f"{key}: {value}")
            file2.write("\n".join(lines))

    def b_plus(self):
        self.button.setText("Коробочка с соусом! Жми!")
        self.balance += self.buz / 4
        self.buz = 0
        self.lable_balance.setText(f"Баланс: {self.balance}₽")
        self.button.clicked.disconnect()
        self.button.clicked.connect(self.btc)


class Platformer(QWidget):
    def __init__(self, parent_calculator=None, parent_pos=None, parent_size=None, run=False):
        if not run:
            self.parent.close()
            QApplication.quit()
        self.sou = 0
        self.buz = 0
        self.balance = 50
        self.parent_calculator = parent_calculator  # Сохраняем ссылку на калькулятор
        self.parent_pos = parent_pos
        self.parent_size = parent_size
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Сэчуанский Соус!")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.setFixedSize(600, 400)
        self.setStyleSheet("background-color: #6dd6ed;")

        if self.parent_pos:
            self.move(self.parent_pos)

        # Создаем основной layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)

        main_layout.addStretch(1)

        # Устанавливаем layout для окна
        self.setLayout(main_layout)

        # Стиль текста
        self.text_style = """
                    QLabel {
                        background-color: #323232;
                        color: white;
                        font-size: 18px;
                        font-weight: 600;
                        font-family: "Segoe UI";
                        border-radius: 10px;
                        padding: 5px;
                        border: none;
                        selection-background-color: #505050;
                    }
                """
        platform = QLabel(self)
        platform.setGeometry(0, 300, 600, 20)
        platform.setStyleSheet("background-color: #61b50d; border: 1px solid #61b50d;")

        dirt = QLabel(self)
        dirt.setGeometry(0, 320, 600, 40)
        dirt.setStyleSheet("background-color: #8B4513; border: 1px solid #654321;")

        if True:
            floor = QLabel(self)
            floor.setGeometry(0, 380, 600, 20)
            floor.setStyleSheet("""
                background-color: #8B4513;
                border-top: 2px solid #654321;
                border-radius: 0px;  # Без скругления
            """)

            # Обычные платформы (среднее скругление)
            platforms = [
                (100, 300, 100, 15),
                (250, 250, 80, 15),
                (400, 200, 120, 15)
            ]

            for x, y, w, h in platforms:
                platform = QLabel(self)
                platform.setGeometry(x, y, w, h)
                platform.setStyleSheet("""
                    background-color: #8B4513;
                    border: 1px solid #654321;
                    border-radius: 5px;
                """)

            # Подвижные платформы (больше скругление)
            moving_platform = QLabel(self)
            moving_platform.setGeometry(150, 150, 60, 12)
            moving_platform.setStyleSheet("""
                background-color: #A0522D;
                border: 1px solid #8B4513;
                border-radius: 6px;
            """)

            fragile_platform = QLabel(self)
            fragile_platform.setGeometry(300, 180, 70, 10)
            fragile_platform.setStyleSheet("""
                background-color: #DEB887;
                border: 1px solid #CD853F;
                border-radius: 5px;  # Полукруг для тонкой платформы
            """)

        self.button = QPushButton("Тест 001", self)
        self.button.move(25, 80)
        self.button.resize(250, 60)
        self.button.clicked.connect(self.btc)
        self.button.setStyleSheet(f"background-color: #{str(random.randint(100000, 999999))}")

        self.lable_buz = QLabel("Тест\n002", self)
        self.lable_buz.move(300, 80)
        self.lable_buz.resize(150, 60)
        self.lable_buz.setStyleSheet(self.text_style)

        self.lable_sou = QLabel("Тест\n003", self)
        self.lable_sou.move(500, 80)
        self.lable_sou.resize(150, 60)
        self.lable_sou.setStyleSheet(self.text_style)

        self.lable_balance = QLabel("Здоровье (Тест 004)", self)
        self.lable_balance.move(10, 40)
        self.lable_balance.resize(350, 30)
        self.lable_balance.setStyleSheet(self.text_style)

        # ДОБАВЛЯЕМ КНОПКУ ВОЗВРАТА В КАЛЬКУЛЯТОР
        self.back_button = QPushButton("Вернуться в калькулятор", self)
        self.back_button.move(150, 8)  # Позиция вверху
        self.back_button.resize(150, 25)
        self.back_button.clicked.connect(self.return_to_calculator)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #404040;
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 12px;
                font-weight: 400;
                font-family: "Segoe UI";
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QPushButton:pressed {
                background-color: #303030;
            }
        """)

        button_style = """
                    QPushButton {
                        background-color: #323232;
                        color: white;
                        border: none;
                        border-radius: 5px;
                        font-size: 16px;
                        font-weight: 600;
                        font-family: "Segoe UI";
                        padding: 12px;
                        margin: 5px;
                    }
                    QPushButton:hover {
                        background-color: #404040;
                        border: 1px solid #505050;
                    }
                    QPushButton:pressed {
                        background-color: #282828;
                    }
                """
        self.button.setStyleSheet(button_style)

    def return_to_calculator(self):
        """Возвращаемся в калькулятор"""
        if self.parent_calculator:
            # Передаем текущую позицию игры калькулятору
            game_position = self.pos()
            self.parent_calculator.move(game_position)  # Калькулятор наследует позицию игры
            self.parent_calculator.show()
            self.parent_calculator.activateWindow()
        self.close()

    def closeEvent(self, event):
        """Обрабатываем закрытие окна игры (крестиком)"""
        if self.parent_calculator:
            # При закрытии крестиком тоже передаем позицию
            game_position = self.pos()
            self.parent_calculator.move(game_position)
            self.parent_calculator.show()
            self.parent_calculator.activateWindow()
        event.accept()

    def btc(self):
        if not self.balance <= -10:
            if random.randint(0, 89) == 0:  # Шанс
                self.balance += random.randint(25, 75)
                self.sou += 1
                self.lable_sou.setText(f"Коробочка\nсоуса: {self.sou}")
                self.lable_balance.setText(f"Баланс: {self.balance}₽")
            else:
                self.balance -= 1
                self.lable_balance.setText(f"Баланс: {self.balance}₽")
                if self.balance > -10:
                    self.buz += 1
                    self.lable_buz.setText(f"Бузулукский\nколбас: {self.buz}")
                    self.lable_balance.setText(f"Баланс: {self.balance}₽")
                else:
                    self.button.setText("Продать колбасы")
                    self.button.clicked.disconnect()
                    self.button.clicked.connect(self.b_plus)

            self.button.move(random.randint(10, 50), (random.randint(80, 440)))
            self.button.setStyleSheet(f"""
                            QPushButton {{
                                background-color: #{str(random.randint(100000, 999999))};
                                color: white;
                                border: none;
                                border-radius: 5px;
                                font-size: 16px;
                                font-weight: 600;
                                font-family: "Segoe UI";
                                padding: 12px;
                                margin: 5px;
                            }}
                            QPushButton:hover {{
                                background-color: #404040;
                                border: 1px solid #505050;
                            }}
                            QPushButton:pressed {{
                                background-color: #282828;
                            }}
                        """)

    def b_plus(self):
        self.button.setText("Коробочка с соусом! Жми!")
        self.balance += self.buz / 4
        self.buz = 0
        self.lable_balance.setText(f"Баланс: {self.balance}₽")
        self.button.clicked.disconnect()
        self.button.clicked.connect(self.btc)
