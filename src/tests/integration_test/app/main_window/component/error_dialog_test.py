# import unittest
# import sys
# from unittest import TestCase

# from PyQt5.QtWidgets import QApplication

# from app.main_window.component.error_dialog import ErrorDialog
# from core.model.action_result import ActionResult


# class ErrorDialogTest(TestCase):
#     action_result = ActionResult()
#     action_result.add_info('Info - 1')
#     action_result.add_info('Info - 3')
#     action_result.add_info('Info - 2')
#     action_result.add_warning('Warning - 1')
#     action_result.add_warning('Warning - 2')
#     action_result.add_warning('Warning - 3')
#     action_result.add_error('Error - 1')
#     action_result.add_error('Error - 2')
#     action_result.add_error('Error - 3')

#     app = QApplication(sys.argv)

#     dialog = ErrorDialog(None, action_result)
#     dialog.exec()
#     app.exit()


# if __name__ == '__main__':
#     unittest.main(exit=False)
