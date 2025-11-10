"""Пометка: в этой версии планируется переработать бпр (меню с кнопками крестика и свёртывания) и добавить блок
мини-игр с первой мини-игрой а так второй раз переписать логику блока ввода"""
import math
import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QLineEdit,
                             QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy, QLineEdit, QMessageBox)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QFont, QIcon, QPixmap, QAction


class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        self.setFixedHeight(40)
        self.setStyleSheet("""
            CustomTitleBar {
                background-color: #2b2b2b;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 5px;
                border-radius: 3px;
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #404040;
            }
            QPushButton#close_btn:hover {
                background-color: #e74c3c;
            }
            QPushButton#min_btn:hover {
                background-color: #404040;
            }
        """)

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(5)

        # Иконка приложения
        icon_label = QLabel()
        try:
            pixmap = QPixmap("calculator_icon.png")
            if not pixmap.isNull():  # Проверяем, что изображение загрузилось
                pixmap = pixmap.scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio,
                                       Qt.TransformationMode.SmoothTransformation)
                icon_label.setPixmap(pixmap)
            else:
                raise Exception("Image is null")
        except:
            icon_label.setText("🧮")
            icon_label.setStyleSheet("font-size: 16px;")

        # Название приложения
        title_label = QLabel("Калькулятор")
        title_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")

        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addStretch()

        # Кнопки управления окном
        self.min_btn = QPushButton("−")
        self.min_btn.setObjectName("min_btn")
        self.min_btn.setFixedSize(25, 25)
        self.min_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        self.close_btn = QPushButton("×")
        self.close_btn.setObjectName("close_btn")
        self.close_btn.setFixedSize(25, 25)
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        # Подключаем сигналы
        self.min_btn.clicked.connect(self.parent.showMinimized)
        self.close_btn.clicked.connect(self.close_app)

        layout.addWidget(self.min_btn)
        layout.addWidget(self.close_btn)

        self.setLayout(layout)

        # Переменные для перемещения окна
        self.dragging = False
        self.drag_position = QPoint()

    def close_app(self):
        """Корректное закрытие приложения"""
        self.parent.close()
        QApplication.quit()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.parent.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.dragging:
            self.parent.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.dragging = False


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

    def initUI(self):
        # Создание GUI
        self.setWindowTitle("Калькулятор")
        self.setFixedSize(370, 580)  # Увеличил высоту на 40px для title bar
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

        # секретная кнопка
        self.secret_button = QPushButton("", content_widget)
        self.secret_button.setFixedSize(40, 40)  # Размер невидимой области
        self.secret_button.move(317, 13)  # Позиция в правом верхнем углу поля ввода
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

        # Блок отвечающий за кнопки:
        # Создание кнопок
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
        btn1.resize(70, 70)
        btn2.resize(70, 70)
        btn3.resize(70, 70)
        btn4.resize(70, 70)
        btn5.resize(70, 70)
        btn6.resize(70, 70)
        btn7.resize(70, 70)
        btn8.resize(70, 70)
        btn9.resize(70, 70)
        btn0.resize(140, 70)
        btn_plus.resize(70, 70)
        btn_minus.resize(70, 70)
        btn_multiply.resize(70, 70)
        btn_share.resize(70, 70)
        btn_equally.resize(70, 140)
        btn_dot.resize(70, 70)
        btn_delete.resize(70, 70)
        btn_clear_entry.resize(70, 70)
        btn_memory_clear.resize(70, 70)
        btn_memory_read.resize(70, 70)
        btn_memory_store.resize(70, 70)
        btn_memory_plus.resize(70, 70)
        btn_memory_minus.resize(70, 70)
        btn_clear.resize(70, 70)
        btn_plus_minus.resize(70, 70)
        btn_root.resize(70, 70)
        btn_percent.resize(70, 70)
        btn_inverse_value.resize(70, 70)

        # Расположение кнопок
        btn1.move(10, 250)
        btn2.move(80, 250)
        btn3.move(150, 250)
        btn4.move(10, 320)
        btn5.move(80, 320)
        btn6.move(150, 320)
        btn7.move(10, 390)
        btn8.move(80, 390)
        btn9.move(150, 390)
        btn0.move(10, 460)
        btn_plus.move(220, 250)
        btn_minus.move(220, 320)
        btn_multiply.move(220, 390)
        btn_share.move(220, 460)
        btn_equally.move(290, 390)
        btn_dot.move(150, 460)
        btn_delete.move(10, 180)
        btn_clear_entry.move(80, 180)
        btn_memory_clear.move(10, 110)
        btn_memory_read.move(80, 110)
        btn_memory_store.move(150, 110)
        btn_memory_plus.move(220, 110)
        btn_memory_minus.move(290, 110)
        btn_clear.move(150, 180)
        btn_plus_minus.move(220, 180)
        btn_root.move(290, 180)
        btn_percent.move(290, 250)
        btn_inverse_value.move(290, 320)

        # Функционал кнопок
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

        for btn in [btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn0, btn_plus, btn_minus, btn_equally,
                    btn_share, btn_multiply, btn_dot, btn_delete, btn_clear_entry, btn_memory_clear, btn_memory_read,
                    btn_memory_store, btn_memory_plus, btn_memory_minus, btn_clear, btn_plus_minus, btn_root,
                    btn_percent, btn_inverse_value]:
            btn.setStyleSheet(button_style)

        # Создание основного текстового окна
        self.text_count = QLineEdit(content_widget)
        self.text_count.setReadOnly(True)
        self.text_count.setText("0")
        self.text_count.move(15, 15)
        self.text_count.setFixedWidth(340)
        self.text_count.resize(260, 90)
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

        # Текстовое окно памяти
        self.memory_text_count = QLineEdit(content_widget)
        self.memory_text_count.setReadOnly(True)
        self.memory_text_count.setText("")
        self.memory_text_count.move(25, 20)
        self.memory_text_count.setFixedWidth(320)
        self.memory_text_count.resize(260, 15)
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

        # Выделение и копирование
        self.text_count.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.text_count.setCursorMoveStyle(Qt.CursorMoveStyle.VisualMoveStyle)
        self.memory_text_count.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.memory_text_count.setCursorMoveStyle(Qt.CursorMoveStyle.VisualMoveStyle)

        # Меню копирования для основного поля
        self.text_count.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        copy_action_main = QAction("Копировать", self.text_count)
        copy_action_main.triggered.connect(lambda: self.copy_text("main"))
        self.text_count.addAction(copy_action_main)

        # Меню копирования для поля памяти (с пометкой "Копировать M")
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
                elif self.count == "0":
                    self.count = "("
                elif self.old_type == "num":
                    self.count += "("

            elif inp == ")":
                if self.old_type == "num":
                    self.count += ")"
                    self.old_type = "num"

        self.text_count.setText(str(self.count))

    def result(self, arg="result"):
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
                    return self.count
                else:
                    self.text_count.setText(self.count)
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
        if result == 777:
            # тут будет вызываться адаптированная игра казино, которая пока-что находится на классном компьютере
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Установка иконки приложения
    try:
        app.setWindowIcon(QIcon("calculator_icon.png"))
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
    ex.show()
    sys.exit(app.exec())
