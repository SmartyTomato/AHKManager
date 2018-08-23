import abc
from typing import List

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import (QAbstractItemView, QHeaderView, QTableWidget,
                             QTableWidgetItem)

from app.application.app_service import AppService
from app.main_window.component.table_widget_item import (CheckBoxCellWidget,
                                                         TableWidgetItem)
from core.manager.process_manager import ProcessManager
from core.model.script import Script
from core.service.library_service import LibraryService
from core.service.profile_service import ProfileService


class TableWidget(QTableWidget):

    columns = ['Name', 'Running', 'Locked', 'Path']

    column_orders = {
        'Name': 0,
        'Running': 1,
        'Locked': 2,
        'Path': 3,
    }

    column_widths = {
        'Name': 120,
        'Running': 60,
        'Locked': 60,
        'Path': 300,
    }

    library_service: LibraryService = LibraryService()
    profile_service: ProfileService = ProfileService()
    app_service: AppService = AppService()
    process_manager = ProcessManager()

    def __init__(self, parent):
        QTableWidget.__init__(self, parent)

        self._init()
        self.refresh()

    def _init(self):
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.setColumnCount(len(self.columns))
        self.setWordWrap(False)
        self.setAutoScroll(False)

        for column in self.columns:
            self.setHorizontalHeaderItem(
                self.column_orders[column], QTableWidgetItem(column))
            self.setColumnWidth(
                self.column_orders[column], self.column_widths[column])

        self.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.horizontalHeader().setSectionResizeMode(
            len(self.columns) - 1, QHeaderView.Stretch)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

        # context menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.open_menu)

    # region abstract methods

    @abc.abstractmethod
    def get_scripts(self) ->List[Script]:
        # return self.app_service.app_model.profile_scripts
        raise NotImplementedError()

    @abc.abstractmethod
    def open_menu(self, position: QPoint):
        raise NotImplementedError()

    # endregion abstract methods

    def refresh(self):
        scripts = self.get_scripts()
        if not scripts:
            self.setRowCount(0)
            return

        count = len(scripts)
        self.setRowCount(count)
        for i in range(0, count):
            script = scripts[i]

            for column in self.columns:
                if column == 'Name':
                    self.setItem(i, self.column_orders[column],
                                 TableWidgetItem(script.identifier(),
                                                 script.name,
                                                 script.is_running()))
                elif column == 'Running':
                    self.setItem(i, self.column_orders[column],
                                 TableWidgetItem(script.identifier(),
                                                 '',
                                                 script.is_running()))
                    self.setCellWidget(i, self.column_orders[column],
                                       CheckBoxCellWidget(script.identifier(),
                                                          script.is_running()))
                elif column == 'Locked':
                    self.setItem(i, self.column_orders[column],
                                 TableWidgetItem(script.identifier(),
                                                 '',
                                                 script.is_locked()))
                    self.setCellWidget(i, self.column_orders[column],
                                       CheckBoxCellWidget(script.identifier(),
                                                          script.is_locked()))
                elif column == 'Path':
                    self.setItem(i, self.column_orders[column],
                                 TableWidgetItem(script.identifier(),
                                                 script.path,
                                                 script.is_running()))
