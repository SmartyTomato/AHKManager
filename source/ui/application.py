import sys

from PyQt5.QtWidgets import QApplication

from core.utility.configuration import Configuration
from core.utility.logger import Logger
from ui.main_window.main_window import MainWindow


class Application(QApplication):

    def __init__(self):
        Logger.log_info('initialize application')
        super(Application, self).__init__([])

        Configuration.get_instance().load()

        self.windows = []
        # create main window
        self.windows.append(MainWindow())

        sys.exit(self.exec())
