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
        self.app_service.profile_selected_events.append(
            self.on_selected_profile_changed)

    # region events

    def on_selected_profile_changed(self):
        self.refresh()

    # endregion events

    # region method implementations

    def get_scripts(self)->List[Script]:
        return self.app_service.get_selected_profile_scripts()

    def open_menu(self, position: QPoint):
        menu = QMenu('I want to...', self)

        add_text = 'Add'
        remove_text = 'Remove'
        start_text = 'Start'
        stop_text = 'Stop'
        open_in_explorer_text = 'Open in Explorer'

        item_selected = self.selectedItems()

        if item_selected:
            menu.addAction(start_text)
            menu.addAction(stop_text)
            menu.addSeparator()
            menu.addAction(remove_text)
            menu.addSeparator()
            menu.addAction(open_in_explorer_text)
        else:
            menu.addAction(add_text)

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
        elif text == open_in_explorer_text:
            self._open_in_explorer(self.selectedItems())

    # endregion method implementations

    # region private methods

    def _add(self):
        profile_id = self.app_service.app_model.selected_profile_id
        if not profile_id:
            return

        dialog = AddScriptToProfileDialog(self)

        if dialog.exec_():
            scripts = dialog.get_selected_scripts()
            if not scripts:
                return

            for script in scripts:
                self.profile_service.add_script(profile_id,
                                                script.identifier())

            self.app_service.save_configuration()
            self.refresh()

    def _remove(self, items: List[TableWidgetItem]):
        profile_id = self.app_service.app_model.selected_profile_id

        if not profile_id or not items:
            return

        for i in range(0, len(items), len(self.columns)):
            script_id = items[i].script_id
            self.profile_service.remove_script_from_profile(
                profile_id, script_id)

        self.app_service.save_configuration()
        self.refresh()

    def _start(self, items: List[TableWidgetItem]):
        if not items:
            return

        for i in range(0, len(items), len(self.columns)):
            script_id = items[i].script_id
            self.library_service.start_script(script_id)

        self.refresh()

    def _stop(self, items: List[TableWidgetItem]):
        if not items:
            return

        for i in range(0, len(items), len(self.columns)):
            script_id = items[i].script_id
            self.library_service.stop_script(script_id)

        self.refresh()

    def _open_in_explorer(self, items: List[TableWidgetItem]):
        if not items:
            return

        for i in range(0, len(items), len(self.columns)):
            script_id = items[i].script_id
            self.process_manager.open_explorer(script_id)

    # endregion private methods
