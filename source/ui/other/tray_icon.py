from PyQt5 import QtGui
from PyQt5.QtWidgets import QMenu, QSystemTrayIcon

from core.utility.logger import Logger


class TrayIcon(QSystemTrayIcon):

    def __init__(self, parent=None):
        Logger.log_info('initialize tray icon')
        super(TrayIcon, self).__init__(parent)

        # set icon
        self.setIcon(QtGui.QIcon('resources/icon/qtlogo.png'))

        # add right click menu
        menu = QMenu(parent)
        exit_action = menu.addAction('Exit')
        self.setContextMenu(menu)

        self.show()
