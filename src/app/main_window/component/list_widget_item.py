from PyQt5 import Qt
from PyQt5.QtWidgets import QListWidgetItem


class ListWidgetItem(QListWidgetItem):

    def __init__(self, parent, display_text: str, identifier: str,
                 is_running: bool = False, is_paused: bool = False) -> None:
        QListWidgetItem.__init__(self, parent)

        self.identifier: str = identifier

        self.setText(display_text)
        self.setToolTip(identifier)

        if is_running:
            self.setForeground(Qt.QColor(0, 0, 255))
        elif is_paused:
            self.setForeground(Qt.QColor(255, 155, 66))
        else:
            self.setForeground(Qt.QColor(0, 0, 0))
