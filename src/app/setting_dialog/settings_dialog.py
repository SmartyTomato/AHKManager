from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import (QDialog, QFileDialog, QGridLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QVBoxLayout)

from src.core.utility.configuration import Configuration


class SettingsDialog(QDialog):

    save_button_size = QSize(60, 30)
    browse_button_size = QSize(30, 20)
    file_type_splitter = ';'
    row_height = 40

    configuration = Configuration()

    def __init__(self, parent):
        QDialog.__init__(self, parent)

        self.path_line_edit = None
        self.file_type_line_edit = None

        self._init()

    def _init(self):
        config = self.configuration.settings_dialog

        # set attribute
        self.setWindowTitle(config.name)
        self.resize(config.width, config.height)

        # setup layout
        layout = QVBoxLayout(self)
        settings_layout = QGridLayout()
        ok_layout = QHBoxLayout()

        layout.addLayout(settings_layout)
        layout.addStretch(1)
        ok_layout.setStretch(0, 0)

        # AHK path
        path_label = QLabel('AutoHotKey executable path:', self)
        settings_layout.addWidget(path_label, 0, 0, 1, 1)

        self.path_line_edit = QLineEdit(self)
        self.path_line_edit.setText(self.configuration.utility.ahk_executable)
        settings_layout.addWidget(self.path_line_edit, 0, 1, 1, 1)

        browse_button = QPushButton('...', self)
        browse_button.setFixedSize(self.browse_button_size)
        settings_layout.addWidget(browse_button, 0, 2, 1, 1)
        browse_button.clicked.connect(self.on_browse_button_clicked)

        # file types
        file_type_label = QLabel('AutoHotKey file type:', self)
        settings_layout.addWidget(file_type_label, 1, 0, 1, 1)

        self.file_type_line_edit = QLineEdit(self)
        self.file_type_line_edit.setText(
            self.file_type_splitter.join(
                self.configuration.utility.file_types))
        settings_layout.addWidget(self.file_type_line_edit, 1, 1, 1, 1)

        # ok and cancel button
        layout.addLayout(ok_layout)

        save_button = QPushButton('Save', self)
        save_button.setFixedSize(self.save_button_size)
        ok_layout.addWidget(save_button)
        save_button.clicked.connect(self.on_save_button_clicked)

        cancel_button = QPushButton('Cancel', self)
        ok_layout.addWidget(cancel_button)
        cancel_button.setFixedSize(self.save_button_size)
        cancel_button.clicked.connect(self.on_cancel_button_clicked)

    # region event

    def on_save_button_clicked(self):
        self.configuration.utility.ahk_executable = self.path_line_edit.text()
        self.configuration.utility.file_types = \
            self.file_type_line_edit.text().split(self.file_type_splitter)
        self.configuration.save_general_configs()
        self.accept()

    def on_cancel_button_clicked(self):
        self.reject()

    def on_browse_button_clicked(self):
        dialog = QFileDialog(self, 'AutoHotKey program')
        dialog.setNameFilters(['Program Files (*.exe)', 'All (*.*)'])
        dialog.selectNameFilter('Program Files (*.exe)')

        if dialog.exec_():
            filenames = dialog.selectedFiles()
            if not filenames:
                return

            self.path_line_edit.setText(filenames[0])

    def closeEvent(self, _):
        self.configuration.settings_dialog.width = self.width()
        self.configuration.settings_dialog.height = self.height()
        self.configuration.save_general_configs()
        self.close()

    # endregion event
