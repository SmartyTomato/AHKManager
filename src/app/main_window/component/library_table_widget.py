from typing import List

from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QMenu

from core.model.script import Script
from core.model.action_result import ActionResult

from app.main_window.component.table_widget import TableWidget
from app.main_window.component.table_widget_item import TableWidgetItem
from app.main_window.component.error_dialog import ErrorDialog


class LibraryTableWidget(TableWidget):

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
        self.app_service.library_selected_events.append(
            self.on_selected_library_changed)

    # region events

    def on_selected_library_changed(self):
        self.refresh()

    # endregion events

    # region method implementations

    def get_scripts(self)->List[Script]:
        return self.app_service.get_selected_library_scripts()

    def open_menu(self, position: QPoint):
        menu = QMenu('I want to...', self)

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

        selected_option = menu.exec(self.mapToGlobal(position))

        if not selected_option:
            return

        text = selected_option.text()
        if text == remove_text:
            self._remove(self.selectedItems())
        elif text == start_text:
            self._start(self.selectedItems())
        elif text == open_in_explorer_text:
            self._open_in_explorer(self.selectedItems())
        elif text == stop_text:
            self._stop(self.selectedItems())

    # endregion method implementations

    # region private methods

    def _remove(self, items: List[TableWidgetItem]):
        if not items:
            return

        result = ActionResult()
        for i in range(0, len(items), len(self.columns)):
            script_id = items[i].script_id
            temp_result = self.profile_service.remove_script(script_id)
            result.merge(temp_result)
            temp_result = self.library_service.remove_script(script_id)
            result.merge(temp_result)

        self._post_process(result)

    def _start(self, items: List[TableWidgetItem]):
        if not items:
            return

        result = ActionResult()
        for i in range(0, len(items), len(self.columns)):
            script_id = items[i].script_id
            temp_result, _ = self.library_service.start_script(script_id)
            result.merge(temp_result)

        self._post_process(result)

    def _stop(self, items: List[TableWidgetItem]):
        if not items:
            return

        result = ActionResult()
        for i in range(0, len(items), len(self.columns)):
            script_id = items[i].script_id
            temp_result, _ = self.library_service.stop_script(script_id)
            result.merge(temp_result)

        self._post_process(result)

    def _open_in_explorer(self, items: List[TableWidgetItem]):
        if not items:
            return

        result = ActionResult()
        for i in range(0, len(items), len(self.columns)):
            script_id = items[i].script_id
            temp_result = self.process_manager.open_explorer(script_id)
            result.merge(temp_result)

        self._post_process(result)

    def _post_process(self, result: ActionResult):
        self._show_error_dialog(result)
        self.app_service.save_configuration()
        self.app_service.refresh()

    def _show_error_dialog(self, result: ActionResult):
        if result.messages:
            error_dialog = ErrorDialog(self, result)
            error_dialog.exec_()
    # endregion private methods
