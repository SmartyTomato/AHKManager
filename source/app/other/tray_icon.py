from PyQt5 import QtGui
from PyQt5.QtWidgets import QMenu, QSystemTrayIcon

from core.utility.logger import Logger


class TrayIcon(QSystemTrayIcon):

    def __init__(self, parent=None):
        super(TrayIcon, self).__init__(parent)

        # set icon
        self.setIcon(QtGui.QIcon('resources/icon/qtlogo.png'))

        show_text = 'Show'
        add_text = 'Add'
        exit_action = 'Exit'

        # add right click menu
        menu = QMenu(parent)
        show_action = menu.addAction(show_text)
        add_action = menu.addAction(add_text)
        exit_action = menu.addAction(exit_action)
        self.setContextMenu(menu)

        self.show()
