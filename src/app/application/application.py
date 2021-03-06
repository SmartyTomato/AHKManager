import sys

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from src.app.main_window.main_window import MainWindow
from src.app.application.app_service import AppService
from src.core.utility.configuration import Configuration


class Application(QApplication):

    app_service = AppService()
    configuration = Configuration()

    def __init__(self):
        QApplication.__init__(self, sys.argv)

        self.app_service.app_model.application = self

        self.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
        self.setWindowIcon(
            QtGui.QIcon(self.configuration.main_window.icon_path))
        self.setQuitOnLastWindowClosed(False)

        self.windows = []
        # create main window
        self.windows.append(MainWindow())
