import sys

from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtWidgets import QAction, QMainWindow, QVBoxLayout, QWidget

from core.model.library_repository import LibraryRepository
from core.model.profile_repository import ProfileRepository
from core.service.library_service import library_service
from core.service.profile_service import ProfileService
from core.utility.configuration import Configuration

from app.application.app_service import AppService
from app.main_window.component.tab_widget import TabWidget
from app.main_window.component.tray_icon import TrayIcon
from app.setting_dialog.settings_dialog import SettingsDialog


class MainWindow(QMainWindow):
    configuration = Configuration()
    profile_service = ProfileService()
    app_service = AppService()

    def __init__(self):
        QMainWindow.__init__(self)

        self._load_configs()
        self._init()
        self.app_service.app_model.main_window = self

        # create a vertical layout in the window
        # all widget should insert into the layout
        central_widget = QWidget(self)
        vertical_layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # initialize tab widget
        self.tab_widget = TabWidget(self)
        vertical_layout.addWidget(self.tab_widget)

        # add tray icon
        self.tray_icon = TrayIcon(self)

        self.refresh()
        self.show()

    def _init(self):
        config = self.configuration.main_window

        # set attributes
        self.setWindowTitle(config.name)
        self.resize(config.width, config.height)

        self._create_menus()

    # region events

    def closeEvent(self, event):
        library_service.stop_all()

        # Save configuration when window is closed
        self.configuration.main_window.width = self.width()
        self.configuration.main_window.height = self.height()
        self.app_service.save_configuration()
        self.tray_icon.hide()
        sys.exit()

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() & Qt.WindowMinimized:
                self.setVisible(False)

    # endregion events

    # region public methods

    def refresh(self):
        self.tab_widget.refresh()

    # endregion public methods

    # region private methods

    def _load_configs(self):
        # load saved settings
        self.configuration.load()
        repo = self.configuration.load_libraries()
        if repo:
            library_service.repository = LibraryRepository.from_json(repo)
        repo = self.configuration.load_profiles()
        if repo:
            self.profile_service.repository = ProfileRepository.from_json(repo)

    def _create_menus(self):
        main_menu = self.menuBar()

        # setting
        settings_menu = main_menu.addMenu('Settings')

        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self._show_settings)

        settings_menu.addAction(settings_action)

        # # library
        # libraryMenu = mainMenu.addMenu('Library')
        # libraryMenu.addAction(settingsAction)

        # # profile
        # profileMenu = mainMenu.addMenu('Profile')
        # profileMenu.addAction(settingsAction)

    def _show_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec_()

    # endregion private methods
