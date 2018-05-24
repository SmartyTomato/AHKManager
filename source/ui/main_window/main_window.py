from PyQt5.QtWidgets import QBoxLayout, QMainWindow, QWidget

from ui.main_window.tab_widget import TabWidget
from ui.other.tray_icon import TrayIcon
from core.utility.configuration import Configuration


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        Logger.log_info('initialize main window')
        super(MainWindow, self).__init__(parent)

        # set attributes
        self.setWindowTitle(Configuration.get().title_main_window)

        # create a vertical layout in the window, all widget should insert into the layout
        central_widget = QWidget(self)
        vertical_layout = QBoxLayout(QBoxLayout.TopToBottom, central_widget)
        self.setCentralWidget(central_widget)

        # initialize tab widget
        tab_widget = TabWidget(self)

        vertical_layout.addWidget(tab_widget)

        # add tray icon
        self.tray_icon = TrayIcon(self)

        self.show()

    def closeEvent(self, event):
        # when window closed
        Configuration.get().save()
