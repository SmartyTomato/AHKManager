import PyQt5
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox, QHBoxLayout, QTableWidgetItem, QWidget


class TableWidgetItem(QTableWidgetItem):

    def __init__(self, script_id: str,
                 text: str='', is_running: bool=False) -> None:
        QTableWidgetItem.__init__(self)

        self.script_id = script_id
        self.setText(text)
        if is_running:
            self.setForeground(PyQt5.Qt.QColor(0, 0, 255))


class CheckBoxCellWidget(QWidget):
    def __init__(self, script_id: str, is_checked: bool=False) -> None:
        QWidget.__init__(self)

        self.script_id = script_id

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)

        checkBox = QCheckBox()
        checkBox.setCheckState(Qt.Checked if is_checked else Qt.Unchecked)
        layout.addWidget(checkBox)
