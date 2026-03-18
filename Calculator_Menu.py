import math
import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QMessageBox, QMenu)
from PyQt6.QtCore import Qt, QPoint, QSettings
from PyQt6.QtGui import QIcon, QAction

import arcade

import Games.GameMenu
from TitleBar import CustomTitleBar

from Games.Arculator.arculator import Arculator

from Games.Culcuraptor.culcuraptor import Culcuraptor

from Games.Calcugambling.Calcugambling import Calcugambling

from Games.Calcublock.Calcublock import Tetris

from Games.Platformer.Platformer import GameWindow

from Games.GameMenu import Start

# from Games.Platformer.exp import GameWindowP

from Games.Snakulator.snakulator import Snakulator

# Загружаем константы
with open("setup") as file:
    setting = file.readlines()
    SAVES = {}
    for elem in setting:
        SAVES[f"{elem.split(" = ")[0]}"] = elem.split(" = ")[1]

# SAVES["IS_GAME_STARTED"] = False
#
# try:
#     with open("setup", "w", encoding="utf-8") as file:
#         lines = []
#         for key, value in SAVES.items():
#               lines.append(f"{key} = {value}")
#         file.write("".join(lines))
#         print("Save, code 0")
# except Exception as e:
#     print(f"Ошибка при сохранении настроек: {e}")
# print("IS_GAME_STARTED: Calcublock:", str(SAVES["IS_GAME_STARTED"]))

SIZE = int(SAVES["SIZE"])
DIFFICULTY = int(SAVES["DIFFICULTY"])
IS_GAME_STARTED = eval(SAVES["IS_GAME_STARTED"])

SIZE = 1


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.dragging = False
        self.drag_position = QPoint()
        self.count = "0"
        self.old_inp = "ClrEntr"
        self.old_command_inp = ""
        self.memory = "0"
        self.old_type = "num"
        self.game_mode = False
        self.old_count = ""
        self.is_game_started = False
        self.evo_tree_is_started = False

    def initUI(self):
        # Создание GUI
        self.setWindowTitle("Калькулятор")
        self.setFixedSize(int(370 * SIZE), int(620 * SIZE))  # Увеличил высоту на 40px для title bar
        self.setStyleSheet("background-color: #1a1a1a;")  # Темный фон
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # Удаление title-bar

        # Создаем основной layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Добавляем кастомный title bar
        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)

        # Создаем контейнер для контента калькулятора
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #1a1a1a;")
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)

        # --------------------------------------------------------------------------------------------------------------

        # секретная кнопка
        self.secret_button = QPushButton("", content_widget)
        self.secret_button.setFixedSize(40, 40)  # Размер невидимой области
        self.secret_button.move(320, 10)  # Позиция в правом верхнем углу поля ввода
        self.secret_button.setStyleSheet("""
                        QPushButton {
                            background-color: transparent;
                            border: none;
                        }
                        QPushButton:hover {
                            background-color: rgba(255, 255, 255, 0.1);
                            border: none;
                            border-radius: 5px;
                        }
                    """)
        self.secret_button.clicked.connect(self.show_secret_popup)
        # -------------------------------------Блок отвечающий за кнопки-------------------------------------------------------

        # Создание кнопок
        settings = QPushButton("≡", content_widget)
        evo_tree = QPushButton("🌳", content_widget)
        btn1 = QPushButton("1", content_widget)
        btn2 = QPushButton("2", content_widget)
        btn3 = QPushButton("3", content_widget)
        btn4 = QPushButton("4", content_widget)
        btn5 = QPushButton("5", content_widget)
        btn6 = QPushButton("6", content_widget)
        btn7 = QPushButton("7", content_widget)
        btn8 = QPushButton("8", content_widget)
        btn9 = QPushButton("9", content_widget)
        btn0 = QPushButton("0", content_widget)
        btn_plus = QPushButton("+", content_widget)
        btn_minus = QPushButton("-", content_widget)
        btn_multiply = QPushButton("*", content_widget)
        btn_share = QPushButton("/", content_widget)
        btn_equally = QPushButton("=", content_widget)
        btn_dot = QPushButton(".", content_widget)
        btn_delete = QPushButton("←", content_widget)
        btn_clear_entry = QPushButton("CE", content_widget)
        btn_memory_clear = QPushButton("MC", content_widget)
        btn_memory_read = QPushButton("MR", content_widget)
        btn_memory_store = QPushButton("MS", content_widget)
        btn_memory_plus = QPushButton("M+", content_widget)
        btn_memory_minus = QPushButton("M-", content_widget)
        btn_clear = QPushButton("C", content_widget)
        btn_plus_minus = QPushButton("±", content_widget)
        btn_root = QPushButton("√", content_widget)
        btn_percent = QPushButton("%", content_widget)
        btn_inverse_value = QPushButton("1/x", content_widget)

        # Размер кнопок
        btn_small_x = int(70 * SIZE)
        btn_small_y = int(70 * SIZE)
        settings_btn_x = 50
        settings_btn_y = 50
        settings.resize(int(settings_btn_x * SIZE), int(settings_btn_y * SIZE))
        evo_tree.resize(int(settings_btn_x * SIZE), int(settings_btn_y * SIZE))
        btn1.resize(btn_small_x, btn_small_y)
        btn2.resize(btn_small_x, btn_small_y)
        btn3.resize(btn_small_x, btn_small_y)
        btn4.resize(btn_small_x, btn_small_y)
        btn5.resize(btn_small_x, btn_small_y)
        btn6.resize(btn_small_x, btn_small_y)
        btn7.resize(btn_small_x, btn_small_y)
        btn8.resize(btn_small_x, btn_small_y)
        btn9.resize(btn_small_x, btn_small_y)
        btn0.resize(btn_small_x * 2, btn_small_y)
        btn_plus.resize(btn_small_x, btn_small_y)
        btn_minus.resize(btn_small_x, btn_small_y)
        btn_multiply.resize(btn_small_x, btn_small_y)
        btn_share.resize(btn_small_x, btn_small_y)
        btn_equally.resize(btn_small_x, btn_small_y * 2)
        btn_dot.resize(btn_small_x, btn_small_y)
        btn_delete.resize(btn_small_x, btn_small_y)
        btn_clear_entry.resize(btn_small_x, btn_small_y)
        btn_memory_clear.resize(btn_small_x, btn_small_y)
        btn_memory_read.resize(btn_small_x, btn_small_y)
        btn_memory_store.resize(btn_small_x, btn_small_y)
        btn_memory_plus.resize(btn_small_x, btn_small_y)
        btn_memory_minus.resize(btn_small_x, btn_small_y)
        btn_clear.resize(btn_small_x, btn_small_y)
        btn_plus_minus.resize(btn_small_x, btn_small_y)
        btn_root.resize(btn_small_x, btn_small_y)
        btn_percent.resize(btn_small_x, btn_small_y)
        btn_inverse_value.resize(btn_small_x, btn_small_y)

        # Расположение кнопок
        # Верхние меню
        settings.move(int(10 * SIZE), int(0 * SIZE))
        evo_tree.move(int(60 * SIZE), int(0 * SIZE))
        # Цифры и основные операции
        btn1.move(int(10 * SIZE), int(290 * SIZE))
        btn2.move(int(80 * SIZE), int(290 * SIZE))
        btn3.move(int(150 * SIZE), int(290 * SIZE))
        btn4.move(int(10 * SIZE), int(360 * SIZE))
        btn5.move(int(80 * SIZE), int(360 * SIZE))
        btn6.move(int(150 * SIZE), int(360 * SIZE))
        btn7.move(int(10 * SIZE), int(430 * SIZE))
        btn8.move(int(80 * SIZE), int(430 * SIZE))
        btn9.move(int(150 * SIZE), int(430 * SIZE))
        btn0.move(int(10 * SIZE), int(500 * SIZE))
        btn_dot.move(int(150 * SIZE), int(500 * SIZE))

        # Операторы справа
        btn_plus.move(int(220 * SIZE), int(290 * SIZE))
        btn_minus.move(int(220 * SIZE), int(360 * SIZE))
        btn_multiply.move(int(220 * SIZE), int(430 * SIZE))
        btn_share.move(int(220 * SIZE), int(500 * SIZE))

        # Кнопка равно (большая, справа)
        btn_equally.move(int(290 * SIZE), int(430 * SIZE))

        # Верхний ряд (управление)
        btn_delete.move(int(10 * SIZE), int(220 * SIZE))
        btn_clear_entry.move(int(80 * SIZE), int(220 * SIZE))
        btn_clear.move(int(150 * SIZE), int(220 * SIZE))
        btn_plus_minus.move(int(220 * SIZE), int(220 * SIZE))
        btn_root.move(int(290 * SIZE), int(220 * SIZE))

        # Память (самый верх)
        btn_memory_clear.move(int(10 * SIZE), int(150 * SIZE))
        btn_memory_read.move(int(80 * SIZE), int(150 * SIZE))
        btn_memory_store.move(int(150 * SIZE), int(150 * SIZE))
        btn_memory_plus.move(int(220 * SIZE), int(150 * SIZE))
        btn_memory_minus.move(int(290 * SIZE), int(150 * SIZE))

        # Дополнительные функции
        btn_percent.move(int(290 * SIZE), int(290 * SIZE))
        btn_inverse_value.move(int(290 * SIZE), int(360 * SIZE))

        # Функционал кнопок
        settings.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        settings.customContextMenuRequested.connect(lambda: self.setting_open("open", "context_menu"))
        settings.clicked.connect(lambda: self.setting_open("open", "context_menu"))

        evo_tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        evo_tree.customContextMenuRequested.connect(lambda: self.evo_tree_open(True))
        evo_tree.clicked.connect(lambda: self.evo_tree_open(True))

        btn1.clicked.connect(lambda: self.keyboard_input("1", "num"))
        btn2.clicked.connect(lambda: self.keyboard_input("2", "num"))
        btn3.clicked.connect(lambda: self.keyboard_input("3", "num"))
        btn4.clicked.connect(lambda: self.keyboard_input("4", "num"))
        btn5.clicked.connect(lambda: self.keyboard_input("5", "num"))
        btn6.clicked.connect(lambda: self.keyboard_input("6", "num"))
        btn7.clicked.connect(lambda: self.keyboard_input("7", "num"))
        btn8.clicked.connect(lambda: self.keyboard_input("8", "num"))
        btn9.clicked.connect(lambda: self.keyboard_input("9", "num"))
        btn0.clicked.connect(lambda: self.keyboard_input("0", "num"))
        btn_plus.clicked.connect(lambda: self.keyboard_input("+", "operation"))
        btn_minus.clicked.connect(lambda: self.keyboard_input("-", "operation"))
        btn_multiply.clicked.connect(lambda: self.keyboard_input("*", "operation"))
        btn_share.clicked.connect(lambda: self.keyboard_input("/", "operation"))
        btn_equally.clicked.connect(lambda: self.result("equal"))
        btn_dot.clicked.connect(lambda: self.keyboard_input(".", "operation"))
        btn_delete.clicked.connect(lambda: self.keyboard_input("del", "operation"))
        btn_clear_entry.clicked.connect(lambda: self.keyboard_input("ClrEntr", "operation"))
        btn_memory_clear.clicked.connect(lambda: self.f_memory("MClear", "operation"))
        btn_memory_read.clicked.connect(lambda: self.f_memory("MRead", "operation"))
        btn_memory_store.clicked.connect(lambda: self.f_memory("MStore", "operation"))
        btn_memory_plus.clicked.connect(lambda: self.f_memory("MPlus", "operation"))
        btn_memory_minus.clicked.connect(lambda: self.f_memory("MMinus", "operation"))
        btn_clear.clicked.connect(lambda: self.keyboard_input("Clear", "operation"))
        btn_plus_minus.clicked.connect(lambda: self.keyboard_input("PlsMns", "operation"))
        btn_root.clicked.connect(lambda: self.keyboard_input("Root", "operation"))
        btn_percent.clicked.connect(lambda: self.keyboard_input("Perc", "operation"))
        btn_inverse_value.clicked.connect(lambda: self.keyboard_input("1/inp", "operation"))

        # Стили кнопок в темной теме
        button_style = """
            QPushButton {
                background-color: #323232;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 20px;
                font-weight: 300;
                font-family: "Segoe UI";
                padding: 2px;
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

        for btn in [evo_tree, settings, btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn0, btn_plus, btn_minus,
                    btn_equally,
                    btn_share, btn_multiply, btn_dot, btn_delete, btn_clear_entry, btn_memory_clear, btn_memory_read,
                    btn_memory_store, btn_memory_plus, btn_memory_minus, btn_clear, btn_plus_minus, btn_root,
                    btn_percent, btn_inverse_value]:
            btn.setStyleSheet(button_style)

        evo_tree.clearFocus()
        settings.clearFocus()
        btn1.clearFocus()
        btn2.clearFocus()
        btn3.clearFocus()
        btn4.clearFocus()
        btn5.clearFocus()
        btn6.clearFocus()
        btn7.clearFocus()
        btn8.clearFocus()
        btn9.clearFocus()
        btn0.clearFocus()
        btn_plus.clearFocus()
        btn_minus.clearFocus()
        btn_multiply.clearFocus()
        btn_share.clearFocus()
        btn_equally.clearFocus()
        btn_dot.clearFocus()
        btn_delete.clearFocus()
        btn_clear_entry.clearFocus()
        btn_memory_clear.clearFocus()
        btn_memory_read.clearFocus()
        btn_memory_store.clearFocus()
        btn_memory_plus.clearFocus()
        btn_memory_minus.clearFocus()
        btn_clear.clearFocus()
        btn_plus_minus.clearFocus()
        btn_root.clearFocus()
        btn_percent.clearFocus()
        btn_inverse_value.clearFocus()

        # --------------------------------------------------------------------------------------------------------------

        # Создание основного текстового окна
        self.text_count = QLineEdit(content_widget)
        self.text_count.setReadOnly(True)
        self.text_count.setText("0")
        self.text_count.move(int(15 * SIZE), int(55 * SIZE))
        self.text_count.setFixedWidth(int(340 * SIZE))
        self.text_count.resize(int(260 * SIZE), int(90 * SIZE))
        self.text_count.setFrame(False)
        self.text_count.setStyleSheet("""
            QLineEdit {
                background-color: #323232;
                color: white;
                font-size: 48px;
                font-weight: 300;
                font-family: "Segoe UI";
                border-radius: 10px;
                padding: 5px;
                border: none;
                selection-background-color: #505050;
            }
        """)
        self.text_count.setAlignment(Qt.AlignmentFlag.AlignRight)

        # --------------------------------------------------------------------------------------------------------------

        # Текстовое окно памяти
        self.memory_text_count = QLineEdit(content_widget)
        self.memory_text_count.setReadOnly(True)
        self.memory_text_count.setText("")
        self.memory_text_count.move(int(25 * SIZE), int(60 * SIZE))
        self.memory_text_count.setFixedWidth(int(320 * SIZE))
        self.memory_text_count.resize(int(260 * SIZE), int(15 * SIZE))
        self.memory_text_count.setFrame(False)
        self.memory_text_count.setStyleSheet("""
            QLineEdit {
                background-color: transparent;
                color: white;
                font-size: 14px;
                font-weight: 500;
                font-family: "Segoe UI";
                border: none;
                padding: 0px;
            }
        """)
        self.memory_text_count.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # --------------------------------------------------------------------------------------------------------------

        # Выделение и копирование
        self.text_count.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.text_count.setCursorMoveStyle(Qt.CursorMoveStyle.VisualMoveStyle)
        self.memory_text_count.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.memory_text_count.setCursorMoveStyle(Qt.CursorMoveStyle.VisualMoveStyle)

        # Меню копирования для основного поля
        self.text_count.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        copy_action_main = QAction("Копировать", self.text_count)
        copy_action_main.triggered.connect(lambda: self.copy_text("main"))

        # --------------------------------------------------------------------------------------------------------------
        self.text_count.addAction(copy_action_main)

        # Меню копирования для поля памяти+

        self.memory_text_count.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        copy_action_memory = QAction("Копировать из памяти", self.memory_text_count)
        copy_action_memory.triggered.connect(lambda: self.copy_text("memory"))
        self.memory_text_count.addAction(copy_action_memory)

        self.count = "0"

        # Добавляем контент в основной layout
        content_layout.addWidget(content_widget)
        main_layout.addWidget(content_widget)
        self.setLayout(main_layout)

    def copy_text(self, source=""):
        # Копирование из разных полей
        clipboard = QApplication.clipboard()

        if source == "memory":
            # Копирование из поля памяти
            selected_text = self.memory_text_count.selectedText()
            if selected_text:
                clipboard.setText(selected_text)
            else:
                text_to_copy = self.memory_text_count.text()
                if text_to_copy.startswith("M "):
                    text_to_copy = text_to_copy[2:]
                clipboard.setText(text_to_copy)
        else:
            # Копирование из основного поля
            selected_text = self.text_count.selectedText()
            if selected_text:
                clipboard.setText(selected_text)
            else:
                clipboard.setText(self.text_count.text())

    def keyboard_input(self, inp="", type_f=""):
        nums = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "√")
        if type_f == "num":
            if self.count == "0":
                self.count = inp
                self.old_type = "num"
            elif self.count == "√0":
                self.count = "√" + inp
                self.old_type = "num"
            elif self.old_type == "num":
                self.count += inp
                self.old_type = "num"
            else:
                self.count += (" " + inp)
                self.old_type = "num"
        else:
            # Простые числовые операции
            if inp == "+" and self.old_type == "num":
                self.count += " +"
                self.old_type = "opr"
            elif inp == "-" and self.old_type == "num":
                self.count += " -"
                self.old_type = "opr"
            elif inp == "*" and self.old_type == "num":
                self.count += " *"
                self.old_type = "opr"
            elif inp == "/" and self.old_type == "num":
                self.count += " /"
                self.old_type = "opr"
            elif inp == "." and self.old_type == "num" and "." not in list(self.count.split()[-1]):
                self.count += "."
                self.old_type = "num"

            # Функциональные кнопки
            elif inp == "del":
                ln_cn = len(self.count)
                if ln_cn == 1:
                    self.count = "0"
                elif self.count[-2] == " ":
                    self.count = self.count[:-2]
                else:
                    self.count = self.count[:-1]

                if self.count[-1] in nums:
                    self.old_type = "num"
                else:
                    self.old_type = "opr"

            elif inp == "Clear":
                self.count = "0"
                self.old_type = "num"

            elif inp == "ClrEntr":
                if self.old_type == "num":
                    if len(self.count) == 1:
                        if self.count == "0":
                            pass
                        else:
                            self.count = "0"
                    else:
                        if len(self.count.split()) == 1:
                            self.count = "0"
                        else:
                            self.count = " ".join(self.count.split()[:-1])

                    if self.count[-1] in nums:
                        self.old_type = "num"
                    else:
                        self.old_type = "opr"

            # Усложненные математические операции
            elif inp == "PlsMns":
                if self.old_type == "num":
                    if len(self.count) == 1:
                        if self.count == "0":
                            pass
                        else:
                            self.count = str(eval(self.count) * (-1))
                    else:
                        if len(self.count.split()) == 1:
                            self.count = str(eval(self.count) * (-1))
                        else:
                            self.count = (" ".join(self.count.split()[:-1]) + " " +
                                          "".join(str(eval(self.count.split()[-1]) * (-1))))

                    if self.count[-1] in nums:
                        self.old_type = "num"
                    else:
                        self.old_type = "opr"

            elif inp == "Root":
                if self.old_type == "num":
                    if self.count == "0":
                        self.count = "√0"
                    else:
                        if len(self.count.split()) == 1:
                            self.count = (" ".join(self.count.split()[:-1]) + "√" +
                                          "".join(self.count.split()[-1]))
                        else:
                            self.count = (" ".join(self.count.split()[:-1]) + " " + "√" +
                                          "".join(self.count.split()[-1]))
                else:
                    self.count += " √"
                    self.old_type = "num"

            elif inp == "Perc":
                if self.old_type == "num":
                    self.count = (" ".join(self.count.split()[:-1]) + " " +
                                  "".join(str(eval(self.count.split()[-1]) / 100)))

            elif inp == "1/inp":
                if self.old_type == "num":
                    self.count = (" ".join(self.count.split()[:-1]) + " " +
                                  "".join(str(1 / eval(self.count.split()[-1]))))

            elif inp == "(":
                if self.old_type != "num":
                    self.count += " ("
                    self.old_type = "num"
                elif self.count == "0":
                    self.count = "("
                    self.old_type = "num"
                elif self.old_type == "num":
                    self.count += "("
                    self.old_type = "num"

            elif inp == ")":
                if self.old_type == "num":
                    self.count += ")"
                    self.old_type = "num"

        self.text_count.setText(str(self.count))

    def setting_open(self, arg="settings", type_f=""):
        # self.setFixedSize(int(370 * SIZE * 2), int(580 * SIZE))
        print("good clicked settings")
        ...

    def evo_tree_open(self, is_opend=False):
        print("good clicked evo_tree")
        self.start = Start()
        if not self.evo_tree_is_started:
            self.evo_tree_is_started = True
            self.start.open()
            print(self.evo_tree_is_started)
        if self.evo_tree_is_started:
            self.evo_tree_is_started = False
            self.start.close()
            print(self.evo_tree_is_started)

    def result(self, arg="result"):
        self.old_count = self.count
        # Результат (В будущем будут проверки для вызова событий)
        nums = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")

        # Защита от пустой строки
        if not self.count:
            self.count = "0"
            return None

        # Автоматически добавляем операторы умножения по математическим правилам
        processed_expression = ""
        i = 0
        while i < len(self.count):
            current_char = self.count[i]
            next_char = self.count[i + 1] if i < len(self.count) - 1 else ""

            processed_expression += current_char

            # Правила для автоматической вставки *
            # 1. Число( -> число*(
            if current_char in nums and next_char == '(':
                processed_expression += '*'
            # 2. )( -> )*(
            elif current_char == ')' and next_char == '(':
                processed_expression += '*'
            # 3. )число -> )*число
            elif current_char == ')' and next_char in nums:
                processed_expression += '*'

            i += 1

        self.count = processed_expression

        res_count = []

        if self.count[-1] == "√":
            self.count += "0"
            self.old_type = "num"

        try:
            for elem in self.count.split():
                roots_op = list(elem)
                n = 0
                open_brackets = 0
                for root in roots_op:
                    if root == "√":
                        roots_op[n] = "math.sqrt("
                        open_brackets += 1
                    n += 1
                # Добавляем закрывающие скобки для всех открытых
                roots_op.extend([")"] * open_brackets)
                res_count.append("".join(roots_op))

            self.count = " ".join(res_count)
        except:
            self.text_count.setText("Ошибка")
            return None

        if self.count[-1] in nums or self.count[-1] == ")" or self.count[-1] != "√":
            try:
                result = eval(self.count)

                if result % 1 == 0:
                    self.count = str(int(result))
                else:
                    self.count = format(result, '.10f').rstrip('0').rstrip('.')

                if arg == "MOpr":
                    output = self.count
                    self.count = self.old_count
                    return output

                else:
                    self.text_count.setText(self.count)
                    with open('WorkSave.txt', 'w', encoding='utf-8') as l:
                        l.write(f'Last result:{self.count}')
                    if self.game_mode:
                        self.mini_games_and_events(eval(self.count))

            except (SyntaxError, ValueError, ZeroDivisionError) as e:
                self.text_count.setText("Ошибка")
                print(f"Ошибка вычисления: {e}")

        return None

    def f_memory(self, opr, type_f):
        try:
            if opr == "MClear":
                self.memory = "0"
                self.memory_text_count.setText("")
            elif opr == "MRead":
                self.count = self.memory
                self.old_type = "num"
                self.text_count.setText(self.count)
            elif opr == "MStore":
                if self.count == "0":
                    self.memory_text_count.setText("")
                else:
                    current_result = self.result("MOpr")
                    if current_result:
                        # Убираем .0 у целых чисел
                        if float(current_result) % 1 == 0:
                            self.memory = str(int(float(current_result)))
                        else:
                            self.memory = current_result
                        self.memory_text_count.setText("M " + self.memory)
            elif opr == "MPlus" and self.count != "0":
                current_result = self.result("MOpr")
                if current_result:
                    # Убираем .0 у целых чисел
                    result_value = float(self.memory) + float(current_result)
                    if result_value % 1 == 0:
                        self.memory = str(int(result_value))
                    else:
                        self.memory = str(result_value)
                    self.memory_text_count.setText("M " + self.memory)
            elif opr == "MMinus" and self.count != "0":
                current_result = self.result("MOpr")
                if current_result:
                    # Убираем .0 у целых чисел
                    result_value = float(self.memory) - float(current_result)
                    if result_value % 1 == 0:
                        self.memory = str(int(result_value))
                    else:
                        self.memory = str(result_value)
                    self.memory_text_count.setText("M " + self.memory)
        except (ValueError, TypeError):
            self.text_count.setText("Ошибка памяти")

    def keyPressEvent(self, event):
        # Обрабатываем нажатия цифровых клавиш
        if event.key() == Qt.Key.Key_1:
            self.keyboard_input("1", "num")
        elif event.key() == Qt.Key.Key_2:
            self.keyboard_input("2", "num")
        elif event.key() == Qt.Key.Key_3:
            self.keyboard_input("3", "num")
        elif event.key() == Qt.Key.Key_4:
            self.keyboard_input("4", "num")
        elif event.key() == Qt.Key.Key_5:
            self.keyboard_input("5", "num")
        elif event.key() == Qt.Key.Key_6:
            self.keyboard_input("6", "num")
        elif event.key() == Qt.Key.Key_7:
            self.keyboard_input("7", "num")
        elif event.key() == Qt.Key.Key_8:
            self.keyboard_input("8", "num")
        elif event.key() == Qt.Key.Key_9:
            self.keyboard_input("9", "num")
        elif event.key() == Qt.Key.Key_0:
            self.keyboard_input("0", "num")
        elif event.key() == Qt.Key.Key_Plus:
            self.keyboard_input("+", "opr")
        elif event.key() == Qt.Key.Key_Minus:
            self.keyboard_input("-", "opr")
        elif event.key() == Qt.Key.Key_Asterisk:
            self.keyboard_input("*", "opr")
        elif event.key() == Qt.Key.Key_Slash:
            self.keyboard_input("/", "opr")
        elif event.key() == Qt.Key.Key_Period:
            self.keyboard_input(".", "opr")
        elif event.key() == Qt.Key.Key_Comma:
            self.keyboard_input(".", "opr")
        elif event.key() == Qt.Key.Key_ParenLeft:
            self.keyboard_input("(", "opr")
        elif event.key() == Qt.Key.Key_ParenRight:
            self.keyboard_input(")", "opr")
        elif event.key() == Qt.Key.Key_Percent:
            self.keyboard_input("%", "opr")
        elif event.key() == Qt.Key.Key_Backspace:
            self.keyboard_input("del", "opr")
        elif event.key() == Qt.Key.Key_Delete:
            self.keyboard_input("ClrEntr", "opr")
        elif event.key() == Qt.Key.Key_Q and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.keyboard_input("Clear", "opr")
        elif event.key() == Qt.Key.Key_Equal:
            self.result("equal")
        elif event.key() == Qt.Key.Key_Enter:
            self.result("equal")

    def show_secret_popup(self):
        """Показывает всплывающее окно при нажатии на невидимую кнопку"""
        if self.game_mode:
            name = "Вы выключили режим мини-игр"
            message = ("Вы выключили режим мини-игр\n\n"
                       "Чтобы включть игрвой режим, нажмите кнопку ещё раз")
            self.game_mode = False
        else:
            name = "Открыта новая функция!"
            message = ("🎉 Поздравляем! Теперь вам доступен режим мини-игр!\n\n"
                       "Попробуйте поэксперементировать с расчётами :)")
            self.game_mode = True

        # Создаем всплывающее окно
        msg = QMessageBox()
        msg.setWindowTitle(name)
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Information)

        # Стиль окна
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #2b2b2b;
                color: white;
            }
            QMessageBox QLabel {
                color: white;
                font-size: 14px;
            }
            QMessageBox QPushButton {
                background-color: #323232;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 14px;
            }
            QMessageBox QPushButton:hover {
                background-color: #404040;
            }
        """)

        msg.exec()

    def mini_games_and_events(self, result):
        self.n = None
        # with open("setup") as file1:
        #     setting1 = file1.readlines()
        #     SAVES1 = {}
        #     for elem1 in setting1:
        #         SAVES1[f"{elem1.split(" = ")[0]}"] = elem1.split(" = ")[1]
        #
        # IS_GAME_STARTED1 = eval(SAVES1["IS_GAME_STARTED"])
        # print("IS_GAME_STARTED:", str(IS_GAME_STARTED1))
        # self.is_game_started = IS_GAME_STARTED1
        self.is_game_started = False
        if result == 777 and not self.is_game_started:
            self.is_game_started = True
            # Сохраняем текущую позицию калькулятора
            self.calculator_position = self.pos()
            # self.hide()
            calc_pos = self.pos()
            self.n = Calcugambling()
            self.n.setup()
            self.n.run()

        # elif result == 99 and not self.is_game_open:
        # self.is_game_open = True
        #     Сохраняем текущую позицию калькулятора
        # self.calculator_position = self.pos()
        # self.hide()
        # calc_pos = self.pos()
        # self.n = Platformer(parent_calculator=self, parent_pos=calc_pos, run=True)
        # self.n.show()
        elif result == 69 and not self.is_game_started:
            self.is_game_started = True
            # Сохраняем текущую позицию калькулятора
            self.calculator_position = self.pos()
            # self.hide()
            calc_pos = self.pos()
            # print(calc_pos)
            self.n = Arculator()
            self.n.setup()
            self.n.run()
            ...
        elif result == 404 and not self.is_game_started:
            self.is_game_started = True
            self.calculator_position = self.pos()
            calc_pos = self.pos()
            self.n = Culcuraptor(SIZE, DIFFICULTY)
            self.n.setup()
            self.n.run()
        # TODO: исправить змейку (крашит все игры сразу)
        # elif result == 1000 and not self.is_game_open:
        #     self.is_game_open = True
        #     self.calculator_position = self.pos()
        #     calc_pos = self.pos()
        #     self.n = Snakulator()
        #     self.n.setup()
        #     self.n.run()
        elif result == 111 and not self.is_game_started:
            self.is_game_started = True
            self.calculator_position = self.pos()
            calc_pos = self.pos()
            self.n = Tetris()
            self.n.run()
        elif result == 100 and not self.is_game_started:
            self.is_game_started = True
            self.calculator_position = self.pos()
            calc_pos = self.pos()
            self.n = GameWindow()
            self.n.setup()
            self.n.run()
        # elif result == 101:
        #     self.is_game_open = True
        #     self.calculator_position = self.pos()
        #     calc_pos = self.pos()
        #     self.n = GameWindowP()
        #     self.n.setup()
        #     self.n.run()
        SAVES["IS_GAME_STARTED"] = True
        try:
            with open("setup", "w", encoding="utf-8") as file:
                lines = []
                for key, value in SAVES.items():
                    lines.append(f"{key} = {value}")
                file.write("".join(lines))
            print("Save, code 0")
        except Exception as e:
            print(f"Ошибка при сохранении настроек: {e}")
        print("IS_GAME_STARTED: Menu:", str(SAVES["IS_GAME_STARTED"]))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Установка иконки приложения
    try:
        app.setWindowIcon(QIcon("Assets/calculator_icon.png"))
    except:
        pass

    # Установка стиля приложения
    app.setStyleSheet("""
        * {
            font-family: "Segoe UI";
        }
        QMenu {
            color: white;
        }
        QMenu::item:selected {
            background-color: #404040;
            color: white;
        }
        QMenu::item:pressed {
            background-color: #282828;
            color: white;
        }
    """)

    ex = Calculator()

    # Наследуем позицию от предыдущего запуска или центрируем
    settings = QSettings("YourCompany", "Calculator")
    pos = settings.value("window_pos", None)
    if pos:
        ex.move(pos)
    else:
        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - ex.width()) // 2
        y = (screen.height() - ex.height()) // 2
        ex.move(x, y)

    ex.show()
    sys.exit(app.exec())
