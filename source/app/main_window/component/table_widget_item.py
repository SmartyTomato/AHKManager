import PyQt5
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QWidget, QHBoxLayout, QCheckBox


class TableWidgetItem(QTableWidgetItem):

    def __init__(self, script_id: str, text: str='', is_running: bool=False):
        QTableWidgetItem.__init__(self)

        self.script_id = script_id
        self.setText(text)
        if is_running:
            self.setForeground(PyQt5.Qt.QColor(0, 0, 255))


class CheckBoxCellWidget(QWidget):
    def __init__(self, is_checked: bool=False):
        QWidget.__init__(self)

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)

        checkBox = QCheckBox()
        checkBox.setCheckState(Qt.Checked if is_checked else Qt.Unchecked)
        layout.addWidget(checkBox)
