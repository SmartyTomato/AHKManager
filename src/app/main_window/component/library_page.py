from app.main_window.component.library_list_widget import LibraryListWidget
from app.main_window.component.library_table_widget import LibraryTableWidget
from app.main_window.component.shared_component import get_search_box
from app.main_window.component.tab_page import TabPage


class LibraryPage(TabPage):

    def __init__(self, parent):
        TabPage.__init__(self, parent)

        self.widget_list = []

        # library list widget
        library_list_widget = LibraryListWidget(self)
        self.layout().addWidget(library_list_widget, 0, 0, 1, 1)

        # add script table
        script_list_widget = LibraryTableWidget(self)
        self.layout().addWidget(script_list_widget, 0, 1, 2, 2)

        # add search box
        search_box = get_search_box()
        self.layout().addLayout(search_box, 1, 0, 1, 1)

        # set relative size
        self.layout().setColumnStretch(0, 10)
        self.layout().setColumnStretch(1, 20)

        self.widget_list.append(library_list_widget)
        self.widget_list.append(script_list_widget)

    def refresh(self):
        for widget in self.widget_list:
            widget.refresh()
