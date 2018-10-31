from typing import List

from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QInputDialog, QMenu

from core.model.action_result import ActionResult

from app.main_window.component.list_widget import ListWidget
from app.main_window.component.list_widget_item import ListWidgetItem
from app.main_window.component.error_dialog import ErrorDialog


class ProfileListWidget(ListWidget):

    def __init__(self, parent):
        ListWidget.__init__(self, parent)

    # region events

    def on_selection_changed(self):
        selected_item = self.currentItem()
        if not selected_item:
            return

        self.app_service.on_profile_selected(selected_item.identifier)

    # endregion events

    # region method implementations

    def get_containers(self) -> List:
        return self.app_service.get_profile_list()

    def open_menu(self, position: QPoint):
        menu = QMenu('I want to...', self)

        add_text = 'Add'
        remove_text = 'Remove'
        start_text = 'Start'
        stop_text = 'Stop'

        item_selected = self.selectedItems()

        if item_selected:
            menu.addAction(start_text)
            menu.addAction(stop_text)
            menu.addSeparator()
            menu.addAction(remove_text)
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

    # endregion method implementations

    # region private methods

    def _add(self):
        name, ok = QInputDialog.getText(self, 'Add Profile', 'Profile name:')

        result = ActionResult()
        if ok and name:
            temp_result = self.profile_service.add(name)
            result.merge(temp_result)

        self._post_process(result)

    def _remove(self, items: List[ListWidgetItem]):
        if not items:
            return

        result = ActionResult()
        for item in items:
            temp_result = self.profile_service.remove(item.identifier)
            result.merge(temp_result)

        self._post_process(result)

    def _start(self, items: List[ListWidgetItem]):
        if not items:
            return

        result = ActionResult()
        for item in items:
            temp_result, _ = self.profile_service.start(item.identifier)
            result.merge(temp_result)

        self._post_process(result)

    def _stop(self, items: List[ListWidgetItem]):
        if not items:
            return

        result = ActionResult()
        for item in items:
            temp_result, _ = self.profile_service.stop(item.identifier)
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
