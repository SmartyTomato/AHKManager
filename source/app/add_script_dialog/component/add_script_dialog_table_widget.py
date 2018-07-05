from typing import List

from PyQt5.QtCore import QPoint

from app.main_window.component.table_widget import \
    TableWidget
from core.model.script import Script


class AddScriptDialogTableWidget(TableWidget):

    columns = ['Name', 'Path']

    column_orders = {
        'Name': 0,
        'Path': 1,
    }

    column_widths = {
        'Name': 120,
        'Path': 300,
    }

    def __init__(self, parent, scripts: List[Script]):
        self.scripts = scripts
        TableWidget.__init__(self, parent)

    def get_scripts(self)->List[Script]:
        return self.scripts

    def open_menu(self, position: QPoint):
        return
