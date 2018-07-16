import sys

from PyQt5.QtWidgets import QApplication

from app.main_window.main_window import MainWindow
from core.utility.logger import Logger


class Application(QApplication):

    def __init__(self):
        QApplication.__init__(self, sys.argv)

        self.windows = []
        # create main window
        self.windows.append(MainWindow())

        sys.exit(self.exec())
