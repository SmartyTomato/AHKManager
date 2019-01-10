from typing import Tuple

from core.manager.process_manager import ProcessManager
from core.model.action_result import ActionResult
from core.model.error_messages import ErrorMessages
from core.model.script import Script
from core.model.singleton import Singleton
from core.utility.configuration import Configuration
from core.utility.utility import Utility


class ScriptManager(metaclass=Singleton):

    process_manager = ProcessManager()
    configuration = Configuration()
    utility: Utility = Utility()

    def init_script(self, path: str) -> Tuple[ActionResult, Script]:
        """
        Initialize script

        Args:
            path (str): script path

        Returns:
            Tuple[ActionResult, Script]: return error
                if script path is invalid
        """

        result = ActionResult()

        path = self.utility.format_path(path)
        # check if path not the file type we want
        temp_result = self._is_script_file(path)
        result.merge(temp_result)

        if not temp_result.success():
            return result, None

        script = Script(path)
        return result, script

    # region public methods

    def remove(self, script: Script) -> ActionResult:
        """
        Remove script, trying to stop script first

        Args:
            script (Script):

        Returns:
            ActionResult: return error if script
                not allow state change or not exists
        """

        # for some reason we can not stop the script
        result, script = self.stop(script)

        if not result.success():
            result.add_error(
                ErrorMessages
                .could_not_remove_script_could_not_stop
                .format(script.identifier()))

        return result

    def refresh(self, script: Script) -> Tuple[ActionResult, Script]:
        """
        Refrersh script, check whether it exists

        Args:
            script (Script):

        Returns:
            Tuple[ActionResult, Script]:
        """

        result = ActionResult()

        # check whether file exists
        if not script.exists():
            result.add_warning(
                ErrorMessages.could_not_refresh_script_script_removed
                .format(script.identifier()))

        return result, script

    # endregion public methods

    # region command

    def start(self, script: Script) -> Tuple[ActionResult, Script]:
        """
        Start script

        Args:
            script (Script):

        Returns:
            Tuple[ActionResult, Script]:
        """

        result = ActionResult()

        # check whether script is locked or not exists
        if not script.allow_state_change():
            if script.is_running():
                result.add_warning(
                    ErrorMessages
                    .could_not_start_locked_script_script_already_running
                    .format(script.identifier()))
                return result, script

        if script.process:
            return result, script

        return self._start_script(script)

    def stop(self, script: Script) -> Tuple[ActionResult, Script]:
        """
        Stop script

        Args:
            script (Script):

        Returns:
            Tuple[ActionResult, Script]:
        """

        result = ActionResult()

        if not script.is_running() or not script.process:
            return result, script

        # check whether script is locked or not exists
        if not script.allow_state_change():
            result.add_error(
                ErrorMessages.could_not_stop_locked_script
                .format(script.identifier()))
            return result, script

        # trying to kill the process
        try:
            script.process.kill()
            script.stop()
        except Exception:
            result.add_error(
                ErrorMessages.could_not_stop_script
                .format(script.identifier()))

        return result, script

    def force_start(self, script: Script) -> Tuple[ActionResult, Script]:
        """
        Force start script, script will be locked after this completed

        Args:
            script (Script):

        Returns:
            Tuple[ActionResult, Script]:
        """

        result = ActionResult()

        temp_result, script = self._start_script(script)
        result.merge(temp_result)

        if temp_result.success():
            script.lock()

        return result, script

    def restart(self, script: Script) -> Tuple[ActionResult, Script]:
        """
        Restart script

        Args:
            script (Script):

        Returns:
            Tuple[ActionResult, Script]:
        """

        result = ActionResult()

        if not script.allow_state_change():
            result.add_error(
                ErrorMessages.could_not_restart_script
                .format(script.identifier()))
            return result, script

        temp_result, script = self.stop(script)

        if not temp_result.success():
            return temp_result, script

        return self._start_script(script)

    def pause(self, script: Script) -> Tuple[ActionResult, Script]:
        """
        Pause script

        Args:
            script (Script):

        Returns:
            Tuple[ActionResult, Script]: return error when process
                cannot be stopped
        """

        result = ActionResult()

        if not script.is_running() or not script.process:
            return result, script

        # * check whether script is locked or not exists
        if not script.allow_state_change():
            result.add_error(
                ErrorMessages.could_not_stop_locked_script
                .format(script.identifier()))
            return result, script

        # trying to kill the process
        try:
            script.process.kill()
            script.pause()
        except Exception:
            result.add_error(
                ErrorMessages.could_not_stop_script.format(
                    script.identifier()))

        return result, script

    # endregion command

    def _start_script(self, script: Script) -> Tuple[ActionResult, Script]:
        result = ActionResult()

        temp_result, process = self.process_manager.start(script.path)

        if not temp_result.success() or not process:
            return temp_result, script

        script.start(process)
        return result, script

    def _is_script_file(self, path: str) -> ActionResult:
        result = ActionResult()

        if not self.utility.is_file(path):
            result.add_error(ErrorMessages.path_is_not_file.format(path))
            return result

        is_script_file = self.utility.get_file_extension(path) in \
            ScriptManager.configuration.utility.file_types
        if not is_script_file:
            result.add_error(
                ErrorMessages.path_is_not_script_file.format(path))

        return result

    # def delete(self, script: Script) -> bool:
    #     # for some reason the script can not be stopped
    #     if not script.stop():
    #         return False

    #     # if file not exists, it success anyway
    #     if not script.exists():
    #         self.logger.info('Script does not exists >>> {}'.format( \
    # repr(script)))
    #         return True

    #     # try to delete file
    #     return self.utility.remove_file(script.script_path)
