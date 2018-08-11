from typing import List

from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QFileDialog, QMenu

from app.main_window.component.list_widget import ListWidget
from app.main_window.component.list_widget_item import ListWidgetItem


class LibraryListWidget(ListWidget):

    def __init__(self, parent):
        ListWidget.__init__(self, parent)

    # region events

    def on_selection_changed(self):
        selected_item = self.currentItem()
        if not selected_item:
            return

        self.app_service.on_library_selected(selected_item.identifier)

    # endregion events

    # region method implementations

    def get_containers(self) -> List:
        return self.app_service.get_library_list()

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
        elif text == open_in_explorer_text:
            self._open_in_explorer(self.selectedItems())
        elif text == stop_text:
            self._stop(self.selectedItems())

        self.refresh()

    # endregion method implementations

    # region private methods

    def _add(self):
        dialog = QFileDialog(self, 'Library Folders')
        dialog.setFileMode(QFileDialog.Directory)

        if dialog.exec_():
            filenames = dialog.selectedFiles()
            if not filenames:
                return

            for filename in filenames:
                self.library_service.add(filename)

        self.refresh()

    def _remove(self, items: List[ListWidgetItem]):
        if not items:
            return

        for item in items:
            script_id = item.identifier
            self.profile_service.remove_script(script_id)
            self.library_service.remove(script_id)

        self.refresh()

    def _start(self, items: List[ListWidgetItem]):
        if not items:
            return

        for item in items:
            self.library_service.start(item.identifier)

        self.refresh()

    def _open_in_explorer(self, items: List[ListWidgetItem]):
        if not items:
            return

        for item in items:
            self.process_manager.open_explorer(item.identifier)

    def _stop(self, items: List[ListWidgetItem]):
        if not items:
            return

        for item in items:
            self.library_service.stop(item.identifier)

        self.refresh()

    # endregion private methods