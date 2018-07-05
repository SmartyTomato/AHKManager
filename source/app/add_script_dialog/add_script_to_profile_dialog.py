from typing import List

from PyQt5.QtWidgets import QBoxLayout, QDialog, QPushButton

from app.add_script_dialog.component.add_script_dialog_table_widget import \
    AddScriptDialogTableWidget
from app.main_window.component.table_widget import \
    TableWidget
from core.service.app_service import AppService
from core.model.script import Script
from core.service.library_service import LibraryService
from core.utility.configuration import Configuration


class AddScriptToProfileDialog(QDialog):

    add_button_width = 40
    ok_button_width = 80

    library_service = LibraryService()
    app_service = AppService()
    configuration = Configuration()

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
        self.setWindowTitle(config['name'])
        self.resize(config['width'], config['height'])

        # setup layout
        layout = QBoxLayout(QBoxLayout.TopToBottom, self)
        script_table_layout = QBoxLayout(QBoxLayout.LeftToRight)
        layout.addLayout(script_table_layout)

        available_layout = QBoxLayout(QBoxLayout.TopToBottom)
        script_table_layout.addLayout(available_layout)

        button_layout = QBoxLayout(QBoxLayout.TopToBottom)
        script_table_layout.addLayout(button_layout)

        selected_layout = QBoxLayout(QBoxLayout.TopToBottom)
        script_table_layout.addLayout(selected_layout)

        ok_layout = QBoxLayout(QBoxLayout.LeftToRight)
        layout.addLayout(ok_layout)

        # initialize available script table
        self.available_script_table = AddScriptDialogTableWidget(self, self.available_scripts)
        available_layout.addWidget(self.available_script_table)
        self.available_script_table.refresh()

        # initialize selected script table
        self.selected_script_table = AddScriptDialogTableWidget(self, self.selected_scripts)
        selected_layout.addWidget(self.selected_script_table)
        self.available_script_table.refresh()

        # add and remove button
        add_button = QPushButton('>>>', self)
        add_button.setMaximumWidth(self.add_button_width)
        button_layout.addWidget(add_button)
        add_button.clicked.connect(self.on_add_button_clicked)

        remove_button = QPushButton('<<<', self)
        button_layout.addWidget(remove_button)
        remove_button.setMaximumWidth(self.add_button_width)
        remove_button.clicked.connect(self.on_remove_button_clicked)

        # ok and cancel button
        ok_button = QPushButton('Ok', self)
        ok_button.setMaximumWidth(self.ok_button_width)
        ok_layout.addWidget(ok_button)
        ok_button.clicked.connect(self.on_ok_button_clicked)

        cancel_button = QPushButton('Cancel', self)
        ok_layout.addWidget(cancel_button)
        cancel_button.setMaximumWidth(self.ok_button_width)
        cancel_button.clicked.connect(self.on_cancel_button_clicked)

    def get_selected_scripts(self)->List[Script]:
        return self.selected_script_table.scripts

    # region events

    def on_ok_button_clicked(self):
        self.accept()

    def on_cancel_button_clicked(self):
        self.reject()

    def on_add_button_clicked(self):
        selected_items = self.available_script_table.selectedItems()
        if not selected_items:
            return

        step = len(self.available_script_table.columns)
        i = 0
        while i < len(selected_items):
            item = selected_items[i]

            scripts = list(filter(lambda x: x.has_id(item.script_id), self.available_scripts))
            if not scripts:
                continue

            self.selected_scripts.append(scripts[0])
            self.available_scripts.remove(scripts[0])
            self.selected_script_table.refresh()
            self.available_script_table.refresh()

            i += step

    def on_remove_button_clicked(self):
        selected_items = self.selected_script_table.selectedItems()
        if not selected_items:
            return

        step = len(self.selected_script_table.columns)
        i = 0
        while i < len(selected_items):
            item = selected_items[i]

            scripts = list(filter(lambda x: x.has_id(item.script_id), self.selected_scripts))
            if not scripts:
                continue

            self.available_scripts.append(scripts[0])
            self.selected_scripts.remove(scripts[0])
            self.available_script_table.refresh()
            self.selected_script_table.refresh()

            i += step

    # endregion events

    def _init_available_scripts(self):
        profile = self.app_service.app_model.selected_profile
        if not profile:
            return

        scripts = self.library_service.get_all_scripts()

        for script_id in profile.script_id_list:
            found = list(filter(lambda x: x.has_id(script_id), scripts))
            if not found:
                continue

            scripts.remove(found[0])

        self.available_scripts = scripts
