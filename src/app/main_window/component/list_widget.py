import abc

from typing import List

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QAbstractItemView, QListWidget

from src.app.application.app_service import AppService
from src.app.main_window.component.list_widget_item import ListWidgetItem
from src.core.manager.process_manager import ProcessManager


class ListWidget(QListWidget):

    app_service: AppService = AppService()
    process_manager: ProcessManager = ProcessManager()

    def __init__(self, parent):
        QListWidget.__init__(self, parent)

        self._init()
        self.refresh()

    def _init(self):
        # set list only one item can be selected
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.open_menu)
        self.itemSelectionChanged.connect(self.on_selection_changed)

    # region abstract methods

    @abc.abstractmethod
    def get_containers(self) -> List:
        raise NotImplementedError()

    @abc.abstractmethod
    def open_menu(self, position: QPoint):
        raise NotImplementedError()

    # endregion abstract methods

    # region events

    @abc.abstractmethod
    def on_selection_changed(self):
        # selected_item = self.currentItem()
        # if not selected_item:
        #     return None

        # library = library_service.find(selected_item.identifier)

        # self.app_service.app_model.selected_library = library
        raise NotImplementedError()

    # endregion events

    # region public methods

    def refresh(self):
        self.clear()

        containers = self.get_containers()
        if not containers:
            return

        for container in containers:
            list_widget_item = ListWidgetItem(self,
                                              container.name,
                                              container.identifier(),
                                              container.is_running(),
                                              container.is_running())
            self.addItem(list_widget_item)

    # endregion public methods
