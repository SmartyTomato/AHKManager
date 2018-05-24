from PyQt5.QtWidgets import QTabWidget


from ui.main_window.tab_page import TabPage
from source.core.utility.logger import Logger

class TabWidget(QTabWidget):

    def __init__(self, parent=None):
        Logger.log_info('Initialize tab widget')
        super(TabWidget, self).__init__(parent)

        tab1 = TabPage(self)
        self.addTab(tab1, "general")
