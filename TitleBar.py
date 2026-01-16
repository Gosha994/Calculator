from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

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
            pixmap = QPixmap("Assets/calculator_icon.png")
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
        """Закрытие приложения"""
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
