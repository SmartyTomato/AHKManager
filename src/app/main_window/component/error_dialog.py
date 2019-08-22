from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, \
    QTableWidgetItem, QAbstractItemView, QHeaderView, QPushButton, QHBoxLayout

from src.core.model.action_result import ActionResult
from src.core.model.message import MessageType


class ErrorDialog(QDialog):
    param = {
        'title': "Error!",
        'width': 1000,
        'height': 600,
        'header_0': 'Type',
        'header_0_width': 80,
        'header_1': 'Message',
        'header_1_width': 360,
        'button_text': 'Ok',
        'button_width': 100,
        'button_height': 60,
    }

    def __init__(self, parent, action_result: ActionResult) -> None:
        QDialog.__init__(self, parent)

        self.action_result = action_result

        self._init()

    def _init(self):
        if not self.action_result:
            self.reject()

        # * Set basic info
        self.setMinimumSize(
            self.param['width'], self.param['height'])
        self.setWindowTitle(self.param['title'])

        # * Create list widget for error messages
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        table_widget = QTableWidget()
        layout.addWidget(table_widget)

        # Set table property
        table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        table_widget.setColumnCount(2)
        table_widget.setWordWrap(False)
        table_widget.setAutoScroll(False)
        # Create header
        table_widget.setHorizontalHeaderItem(
            0, QTableWidgetItem(self.param['header_0']))
        table_widget.setColumnWidth(0, self.param['header_0_width'])
        table_widget.setHorizontalHeaderItem(
            1, QTableWidgetItem(self.param['header_1']))
        table_widget.setColumnWidth(1, self.param['header_1_width'])
        # Set last header stretch with width
        table_widget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Interactive)
        table_widget.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.Stretch)
        table_widget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

        # Add error messages
        table_widget.setRowCount(len(self.action_result.messages))
        for i in range(0, len(self.action_result.messages)):
            message = self.action_result.messages[i]

            msg_type = 'Info'
            background_color = QColor(255, 255, 255)
            foreground_color = QColor(0, 0, 0)
            if message.type == MessageType.ERROR:
                msg_type = 'Error'
                background_color = QColor(255, 99, 71)
                foreground_color = QColor(255, 255, 255)
            elif message.type == MessageType.WARNING:
                msg_type = 'Warning'
                background_color = QColor(255, 165, 0)
                foreground_color = QColor(255, 255, 255)

            table_item = QTableWidgetItem(msg_type)
            if background_color:
                table_item.setBackground(background_color)
            if foreground_color:
                table_item.setForeground(foreground_color)
            table_widget.setItem(i, 0, table_item)
            table_widget.setItem(i, 1, QTableWidgetItem(message.message))

        # * Ok button
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        button_layout.setAlignment(Qt.AlignCenter)
        ok_button = QPushButton(self.param['button_text'])
        ok_button.setFixedSize(
            self.param['button_width'], self.param['button_height'])
        ok_button.clicked.connect(lambda: self.accept())
        button_layout.addWidget(ok_button)
