from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit


def get_search_box()->QHBoxLayout:
    # search edit box
    search_layout = QHBoxLayout()
    search_label = QLabel('Search: ')
    search_layout.addWidget(search_label)
    search_line_edit = QLineEdit()
    search_layout.addWidget(search_line_edit)

    return search_layout