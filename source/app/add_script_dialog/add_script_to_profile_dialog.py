from typing import List

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QPushButton, QVBoxLayout

from app.add_script_dialog.component.add_script_dialog_table_widget import \
    AddScriptDialogTableWidget
from app.application.app_service import AppService
from app.main_window.component.table_widget import TableWidget
from core.model.script import Script
from core.service.library_service import LibraryService
from core.service.profile_service import ProfileService
from core.utility.configuration import Configuration


class AddScriptToProfileDialog(QDialog):

    add_button_size = QSize(50, 40)
    ok_button_size = QSize(100, 60)

    library_service: LibraryService = LibraryService()
    profile_service: ProfileService = ProfileService()
    app_service: AppService = AppService()
    configuration: Configuration = Configuration()

    def __init__(self, parent):
        QDialog.__init__(self, parent)

        self.available_scripts: List[Script] = []
        self.selected_scripts: List[Script] = []
        self.available_script_table: TableWidget = None
        self.selected_script_table: TableWidget = None

        self._init_available_scripts()
        self._init()
        self.show()

    def _init(self):
        config = self.configuration.add_script_dialog

        # set attributes
        self.setWindowTitle(config.name)
        self.resize(config.width, config.height)

        # setup layouts
        layout = QVBoxLayout(self)
        script_table_layout = QHBoxLayout()
        ok_layout = QHBoxLayout()
        available_layout = QVBoxLayout()
        button_layout = QVBoxLayout()
        selected_layout = QVBoxLayout()

        layout.addLayout(script_table_layout)
        layout.addLayout(ok_layout)

        script_table_layout.addLayout(available_layout)
        script_table_layout.addLayout(button_layout)
        script_table_layout.addLayout(selected_layout)

        # initialize available script table
        self.available_script_table = AddScriptDialogTableWidget(
            self, self.available_scripts)
        self.available_script_table.itemDoubleClicked.connect(
            self.on_available_script_table_item_double_clicked)
        available_layout.addWidget(self.available_script_table)
        self.available_script_table.refresh()

        # initialize selected script table
        self.selected_script_table = AddScriptDialogTableWidget(
            self, self.selected_scripts)
        self.selected_script_table.itemDoubleClicked.connect(
            self.on_selected_script_table_item_double_clicked)
        selected_layout.addWidget(self.selected_script_table)
        self.available_script_table.refresh()

        # add and remove button
        button_layout.addStretch(1)
        add_button = QPushButton('>', self)
        add_button.setFixedSize(self.add_button_size)
        button_layout.addWidget(add_button)
        add_button.clicked.connect(self.on_add_button_clicked)

        add_all_button = QPushButton('>>>', self)
        add_all_button.setFixedSize(self.add_button_size)
        button_layout.addWidget(add_all_button)
        add_all_button.clicked.connect(self.on_add_all_button_clicked)
        button_layout.addStretch(1)

        remove_button = QPushButton('<', self)
        button_layout.addWidget(remove_button)
        remove_button.setFixedSize(self.add_button_size)
        remove_button.clicked.connect(self.on_remove_button_clicked)

        remove_all_button = QPushButton('<<<', self)
        button_layout.addWidget(remove_all_button)
        remove_all_button.setFixedSize(self.add_button_size)
        remove_all_button.clicked.connect(self.on_remove_all_button_clicked)
        button_layout.addStretch(1)

        # ok and cancel button
        ok_button = QPushButton('Ok', self)
        ok_button.setFixedSize(self.ok_button_size)
        ok_layout.addWidget(ok_button)
        ok_button.clicked.connect(self.on_ok_button_clicked)

        cancel_button = QPushButton('Cancel', self)
        ok_layout.addWidget(cancel_button)
        cancel_button.setFixedSize(self.ok_button_size)
        cancel_button.clicked.connect(self.on_cancel_button_clicked)

    def get_selected_scripts(self) -> List[Script]:
        return self.selected_script_table.scripts

    # region events

    def on_ok_button_clicked(self):
        self.accept()

    def on_cancel_button_clicked(self):
        self.reject()

    def on_add_button_clicked(self):
        # get selected table items
        selected_items = self.available_script_table.selectedItems()
        if not selected_items:
            return

        # each row has x number of columns
        step = len(self.available_script_table.columns)
        i = 0
        while i < len(selected_items):
            item = selected_items[i]
            self._select_script(item.script_id)
            i += step

    def on_add_all_button_clicked(self):
        # reset the scripts
        # now you will have everything available in avaliable_script list
        self._init_available_scripts()

        # set selected as available scripts
        self.selected_scripts = self.available_scripts
        self.available_scripts = []

        # set the table scripts
        self.selected_script_table.scripts = self.selected_scripts
        self.available_script_table.scripts = self.available_scripts

        # refresh tables
        self.available_script_table.refresh()
        self.selected_script_table.refresh()

    def on_remove_all_button_clicked(self):
        # reset all data
        self._init_available_scripts()
        self.selected_script_table.scripts = self.selected_scripts
        self.available_script_table.scripts = self.available_scripts
        self.available_script_table.refresh()
        self.selected_script_table.refresh()

    def on_remove_button_clicked(self):
        selected_items = self.selected_script_table.selectedItems()
        if not selected_items:
            return

        # each row has x number of columns
        step = len(self.selected_script_table.columns)
        i = 0
        while i < len(selected_items):
            item = selected_items[i]
            self._unselect_script(item.script_id)
            i += step

    def on_available_script_table_item_double_clicked(self, item):
        self._select_script(item.script_id)

    def on_selected_script_table_item_double_clicked(self, item):
        self._unselect_script(item.script_id)

    def closeEvent(self, _):
        self.configuration.add_script_dialog.width = self.width()
        self.configuration.add_script_dialog.height = self.height()
        self.configuration.save_general_configs()
        self.close()

    # endregion events

    def _init_available_scripts(self):
        profile = self.profile_service.find(
            self.app_service.app_model.selected_profile_id)
        if not profile:
            return

        self.available_scripts = []
        self.selected_scripts = []
        scripts = self.library_service.get_all_scripts()

        for script_id in profile.script_id_list:
            found = next((x for x in scripts if x.has_id(script_id)), None)
            if not found:
                continue

            scripts.remove(found)

        self.available_scripts = scripts

    def _select_script(self, script_id):
        script = next((x for x in self.available_scripts
                       if x.has_id(script_id)), None)
        if not script:
            return

        self.selected_scripts.append(script)
        self.available_scripts.remove(script)
        self.selected_script_table.refresh()
        self.available_script_table.refresh()

    def _unselect_script(self, script_id):
        script = next((x for x in self.selected_scripts
                       if x.has_id(script_id)), None)
        if not script:
            return

        self.available_scripts.append(script)
        self.selected_scripts.remove(script)
        self.available_script_table.refresh()
        self.selected_script_table.refresh()
