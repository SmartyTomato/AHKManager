from app.main_window.component.profile_list_widget import ProfileListWidget
from app.main_window.component.profile_table_widget import ProfileTableWidget
from app.main_window.component.shared import get_search_box
from app.main_window.component.tab_page import TabPage


class ProfilePage(TabPage):

    def __init__(self, parent):
        TabPage.__init__(self, parent)

        # profile list widget
        profile_list_widget = ProfileListWidget(self)
        self.layout().addWidget(profile_list_widget, 0, 0, 1, 1)

        # add script table
        script_list_widget = ProfileTableWidget(self)
        self.layout().addWidget(script_list_widget, 0, 1, 2, 2)

        # add search box
        search_box = get_search_box()
        self.layout().addLayout(search_box, 1, 0, 1, 1)

        # set relative size
        self.layout().setColumnStretch(0, 10)
        self.layout().setColumnStretch(1, 20)
