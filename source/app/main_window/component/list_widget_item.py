from PyQt5 import Qt
from PyQt5.QtWidgets import QListWidgetItem


class ListWidgetItem(QListWidgetItem):

    def __init__(self, parent, display_text: str, toolTip: str, is_running: bool=False):
        QListWidgetItem.__init__(self, parent)

        self.identifier: str = toolTip

        self.setText(display_text)
        self.setToolTip(toolTip)

        if is_running:
            self.setForeground(Qt.QColor(0, 0, 255))
        else:
            self.setForeground(Qt.QColor(0, 0, 0))
