from typing import Tuple
from typing import Optional

import subprocess
from subprocess import Popen

from core.model.action_result import ActionResult
from core.model.error_messages import ErrorMessages
from core.utility.configuration import Configuration
from core.utility.utility import Utility


class ProcessManager:

    configuration = Configuration()
    utility: Utility = Utility()

    def start(self, path: str) -> Tuple[ActionResult, Optional[Popen]]:
        """
        Open file path using ahk executable path

        Args:
            path (str): file path

        Returns:
            Tuple[ActionResult,  Optional[Popen]]:
                ActionResult: return error
                    if failed to start script
                 Optional[Popen]: launched ahk process
        """

        result = ActionResult()

        if not self.utility.is_file(path):
            result.add_error(
                ErrorMessages.script_path_not_valid.format(path))
            return result, None

        ahk_path = ProcessManager.configuration.utility.ahk_executable
        if not ahk_path:
            result.add_error(
                ErrorMessages.autohotkey_path_is_not_valid.format(ahk_path))
            return result, None

        try:
            process = subprocess.Popen([ahk_path, path], shell=False)
            return result, process
        except Exception:
            result.add_error(
                ErrorMessages.could_not_start_script.format(path))
            return result, None

    def open_explorer(self, path: str) -> ActionResult:
        """
        Open path in file explorer for windows only

        Args:
            path (str): file path

        Returns:
            ActionResult: return error
                if for some reason failed to open path
        """

        result = ActionResult()

        try:
            subprocess.Popen('explorer /select,{}'.format(path))
        except Exception:
            result.add_error(ErrorMessages.could_not_open_path.format(path))

        return result
