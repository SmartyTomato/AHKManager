from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QMenu, QSystemTrayIcon, QMessageBox

from app.application.app_service import AppService
from core.service.library_service import LibraryService
from core.service.profile_service import ProfileService
from core.utility.configuration import Configuration

# region constants

button_text_show = 'Show'
button_text_exit = 'Exit'
button_text_stop = 'Stop all'
button_text_pause = 'Pause'
button_text_resume = 'Resume'

dialog_title = 'Information'
dialog_message_stop = 'All script has been stopped'
dialog_message_pause = 'All script has been paused'
dialog_message_resume = 'All script has been resumed'

# endregion constants


class TrayIcon(QSystemTrayIcon):

    library_service: LibraryService = LibraryService()
    profile_service: ProfileService = ProfileService()
    configuration: Configuration = Configuration()
    app_service: AppService = AppService()

    def __init__(self, parent=None):
        QSystemTrayIcon.__init__(self, parent)

        # set tray icon
        self.setIcon(QtGui.QIcon(self.configuration.main_window.icon_path))

        # double click event
        self.activated.connect(self.on_activated)

        # add right click menu
        menu = QMenu(parent)

        pause_action = menu.addAction(button_text_pause)
        pause_action.triggered.connect(self.on_pause_triggered)

        resume_action = menu.addAction(button_text_resume)
        resume_action.triggered.connect(self.on_resume_triggered)

        stop_all_action = menu.addAction(button_text_stop)
        stop_all_action.triggered.connect(self.on_stop_all_triggered)

        menu.addSeparator()

        show_action = menu.addAction(button_text_show)
        show_action.triggered.connect(self.show_triggered)

        exit_action = menu.addAction(button_text_exit)
        exit_action.triggered.connect(self.on_exit_triggered)

        self.setContextMenu(menu)
        self.show()

    def on_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_triggered()

    def show_triggered(self):
        self.app_service.app_model.main_window.setVisible(True)
        self.app_service.app_model.main_window.setWindowState(Qt.WindowActive)

    def on_exit_triggered(self):
        self.app_service.app_model.main_window.closeEvent(QCloseEvent())

    def on_stop_all_triggered(self):
        self.library_service.stop_all()
        self.profile_service.stop_all()

        self._refresh_main_window()
        self._show_message_box(dialog_message_stop)

    def on_pause_triggered(self):
        self.library_service.pause_all()
        self._show_message_box(dialog_message_pause)

    def on_resume_triggered(self):
        self.library_service.resume_all()
        self._show_message_box(dialog_message_resume)

    # region private methods

    def _show_message_box(self, message: str):
        # * Show notification box
        message_box = QMessageBox(None)
        message_box.setIcon(QMessageBox.Information)
        message_box.setText(message)
        message_box.setWindowTitle(dialog_title)
        message_box.exec_()

    def _refresh_main_window(self):
        # * Refresh UI
        self.app_service.app_model.main_window.refresh()

    # endregion private methods
