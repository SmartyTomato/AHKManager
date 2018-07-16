from PyQt5.QtWidgets import QBoxLayout, QMainWindow, QWidget

from app.main_window.component.tab_widget import TabWidget
from app.other.tray_icon import TrayIcon
from core.model.library_repository import LibraryRepository
from core.model.profile_repository import ProfileRepository
from core.service.library_service import LibraryService
from core.service.profile_service import ProfileService
from core.service.app_service import AppService
from core.utility.configuration import Configuration


class MainWindow(QMainWindow):

    configuration = Configuration()
    library_service = LibraryService()
    profile_service = ProfileService()
    app_service = AppService()

    def __init__(self):
        QMainWindow.__init__(self)

        self._init()

        self._load_configs()
        self.app_service.update_lists()

        # create a vertical layout in the window, all widget should insert into the layout
        central_widget = QWidget(self)
        vertical_layout = QBoxLayout(QBoxLayout.TopToBottom, central_widget)
        self.setCentralWidget(central_widget)

        # initialize tab widget
        tab_widget = TabWidget(self)
        vertical_layout.addWidget(tab_widget)

        # add tray icon
        # todo - uncomment
        # self.tray_icon = TrayIcon(self)

        self.show()

    def _init(self):
        config = self.configuration.main_window

        # set attributes
        self.setWindowTitle(config['name'])
        self.resize(config['width'], config['height'])

    def closeEvent(self, event):
        self.library_service.stop_all()
        # self.tray_icon.hide()
        # del self.tray_icon
        # Save configuration when window is closed
        self.configuration.save(self.profile_service.repository, self.library_service.repository)

    def _load_configs(self):
        # load saved settings
        self.configuration.load()
        repo = self.configuration.load_libraries()
        if repo:
            self.library_service.repository = LibraryRepository.from_json(repo)
        repo = self.configuration.load_profiles()
        if repo:
            self.profile_service.repository = ProfileRepository.from_json(repo)
