from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QStyle

from ..configure import configs

import sys
import logging


class Application(QApplication):
    def __init__(self):
        # Initialize new application
        app = QApplication(sys.argv)

        # Create main window
        window = MainWindow()

        # Exit Python when application ends
        sys.exit(app.exec())


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        if __debug__:
            logging.info("Initialize main window")

        super(MainWindow, self).__init__()

        self.setWindowTitle("AHK Manager")

        # Add system tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(
        self.style().standardIcon(QStyle.SP_ComputerIcon))

        self.show()