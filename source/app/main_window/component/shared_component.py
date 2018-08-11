from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit


def get_search_box(parent=None) -> QHBoxLayout:
    # search edit box
    search_layout = QHBoxLayout(parent)
    search_label = QLabel('Search: ', parent)
    search_layout.addWidget(search_label)
    search_line_edit = QLineEdit(parent)
    search_layout.addWidget(search_line_edit)

    return search_layout
