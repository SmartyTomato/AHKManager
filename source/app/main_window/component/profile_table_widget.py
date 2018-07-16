from typing import List

from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QMenu

from app.add_script_dialog.add_script_to_profile_dialog import \
    AddScriptToProfileDialog
from app.main_window.component.table_widget import TableWidget
from app.main_window.component.table_widget_item import TableWidgetItem
from core.model.script import Script


class ProfileTableWidget(TableWidget):

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

    def __init__(self, parent):
        TableWidget.__init__(self, parent)

        # register event
        self.app_service.profile_selected_events.append(self.on_selected_profile_changed)

    # region events

    def on_selected_profile_changed(self):
        self.refresh()

    # endregion events

    # region method implementations

    def get_scripts(self)->List[Script]:
        return self.app_service.app_model.profile_scripts

    def open_menu(self, position: QPoint):
        menu = QMenu('I want to...', self)

        add_text = 'Add'
        remove_text = 'Remove'
        start_text = 'Start'
        stop_text = 'Stop'

        menu.addAction(add_text)
        menu.addAction(remove_text)
        menu.addSeparator()
        menu.addAction(start_text)
        menu.addAction(stop_text)
        selected_option = menu.exec(self.mapToGlobal(position))

        if not selected_option:
            return

        text = selected_option.text()

        if text == add_text:
            self._add()
        elif text == remove_text:
            self._remove(self.selectedItems())
        elif text == start_text:
            self._start(self.selectedItems())
        elif text == stop_text:
            self._stop(self.selectedItems())
        elif text == start_text:
            self._start(self.selectedItems())

    # endregion method implementations

    # region private methods

    def _add(self):
        profile = self.app_service.app_model.selected_profile
        if not profile:
            return

        dialog = AddScriptToProfileDialog(self)

        if dialog.exec_():
            scripts = dialog.get_selected_scripts()
            if not scripts:
                return

            for script in scripts:
                self.profile_service.add_script(profile.identifier(), script.identifier())

            self.app_service.update_lists()
            self.refresh()

    def _remove(self, items: List[TableWidgetItem]):
        if not items:
            return

        for i in range(0, len(items), len(self.columns)):
            identifier = items[i+self.column_orders['Path']].text()
            self.profile_service.remove_script(identifier)

        self.app_service.update_lists()
        self.refresh()

    def _start(self, items: List[TableWidgetItem]):
        if not items:
            return

        for i in range(0, len(items), len(self.columns)):
            identifier = items[i+self.column_orders['Path']].text()
            self.library_service.start_script(identifier)

        self.app_service.update_lists()
        self.refresh()

    def _stop(self, items: List[TableWidgetItem]):
        if not items:
            return

        for i in range(0, len(items), len(self.columns)):
            identifier = items[i+self.column_orders['Path']].text()
            self.library_service.stop_script(identifier)

        self.app_service.update_lists()
        self.refresh()

    # endregion private methods
