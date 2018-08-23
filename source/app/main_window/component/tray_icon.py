from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QMenu, QSystemTrayIcon

from app.application.app_service import AppService
from core.service.library_service import LibraryService
from core.service.profile_service import ProfileService
from core.utility.configuration import Configuration


class TrayIcon(QSystemTrayIcon):

    library_service: LibraryService = LibraryService()
    profile_service: ProfileService = ProfileService()
    configuration: Configuration = Configuration()
    app_service: AppService = AppService()

    def __init__(self, parent=None):
        QSystemTrayIcon.__init__(self, parent)

        # set icon
        self.setIcon(QtGui.QIcon(self.configuration.main_window.icon_path))

        # double click event
        self.activated.connect(self.on_activated)

        show_text = 'Show'
        exit_text = 'Exit'
        stop_all_text = 'Stop all'

        # add right click menu
        menu = QMenu(parent)

        stop_all_action = menu.addAction(stop_all_text)
        stop_all_action.triggered.connect(self.on_stop_all_triggered)

        menu.addSeparator()

        show_action = menu.addAction(show_text)
        show_action.triggered.connect(self.show_triggered)

        exit_action = menu.addAction(exit_text)
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
        self.profile_service.stop_all()
        self.library_service.stop_all()

        self.app_service.app_model.main_window.refresh()
