from PyQt5.QtWidgets import QTabWidget

from app.main_window.component.library_page import LibraryPage
from app.main_window.component.profile_page import ProfilePage


class TabWidget(QTabWidget):

    def __init__(self, parent):
        QTabWidget.__init__(self, parent)

        # set tab style
        self.setStyleSheet("QTabBar::tab {width: 100px; height: 30px; font-size: 16px}\
                            QTabBar::tab:selected \
                            {color: white; background-color: \
                            rgb(0, 181, 255);}")

        profile_page = ProfilePage(self)
        self.addTab(profile_page, "Profile")

        library_page = LibraryPage(self)
        self.addTab(library_page, "Library")

        # process_page = ProcessPage(self)
        # self.addTab(process_page, "Process")

        self.currentChanged.connect(self.on_selected_tab_changed)

    def on_selected_tab_changed(self, index):
        self.widget(index).refresh()
