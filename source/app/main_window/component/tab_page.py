from PyQt5.QtWidgets import QGridLayout, QWidget


class TabPage(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.setLayout(QGridLayout())
