import abc

from PyQt5.QtWidgets import QGridLayout, QWidget

from app.application.app_service import AppService


class TabPage(QWidget):

    app_service: AppService = AppService()

    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.setLayout(QGridLayout())

    @abc.abstractmethod
    def refresh(self):
        raise NotImplementedError()
