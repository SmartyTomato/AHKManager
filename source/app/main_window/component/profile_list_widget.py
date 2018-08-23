from typing import List

from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QInputDialog, QMenu

from app.main_window.component.list_widget import ListWidget
from app.main_window.component.list_widget_item import ListWidgetItem


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

        if ok and name:
            self.profile_service.add(name)

            self.app_service.refresh()
            self.app_service.save_configuration()

    def _remove(self, items: List[ListWidgetItem]):
        if not items:
            return

        for item in items:
            self.profile_service.remove(item.identifier)

        self.app_service.refresh()
        self.app_service.save_configuration()

    def _start(self, items: List[ListWidgetItem]):
        if not items:
            return

        for item in items:
            self.profile_service.start(item.identifier)

        self.app_service.refresh()

    def _stop(self, items: List[ListWidgetItem]):
        if not items:
            return

        for item in items:
            self.profile_service.stop(item.identifier)

        self.app_service.refresh()

    # endregion private methods
