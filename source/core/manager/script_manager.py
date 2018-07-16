from core.manager.process_manager import ProcessManager
from core.model.script import Script
from core.model.singleton import Singleton
from core.service.message_service import MessageService
from core.utility.configuration import Configuration
from core.utility.logger import Logger
from core.utility.message import Message, MessageType
from core.utility.utility import Utility


class ScriptManager(Singleton):
    logger = Logger('ScriptManager')

    message_service = MessageService()
    process_manager = ProcessManager()
    configuration = Configuration()

    def init_script(self, path: str) -> Script:
        path = Utility.format_path(path)

        # check if path not the file type we want
        if not self.is_script_file(path):
            self.message_service.add(Message(MessageType.WARNING, 'Path not a script file: {}'.format(path)))
            self.logger.warning('Path not a script file >>> {}'.format(path))
            return None

        script = Script(path)
        return script

    # region public methods

    def remove(self, script: Script) -> bool:
        # for some reason we can not stop the script, do not hide script in that case
        if not self.stop(script):
            self.message_service.add(
                Message(MessageType.ERROR, 'Could not remove script: {}'.format(script.path)))
            self.logger.error('Could not remove script >>> {}'.format(repr(script)))
            return False

        return True

    def refresh(self, script: Script) -> bool:
        if not script.exists():
            self.message_service.add(Message(MessageType.WARNING, 'Script does not exists: {}'.format(script.path)))
            self.logger.warning('Script does not exists >>> {}'.format(repr(script)))
            return False

        return True

    # endregion public methods

    # region command

    def start(self, script: Script):
        if not script.allow_state_change():
            if script.is_running():
                self.logger.info(
                    'Could not start locked script, but script already running >>> {}'.format(repr(script)))
                return

            self.message_service.add(
                Message(MessageType.ERROR, 'Could not start locked script: {}'.format(script.path)))
            self.logger.error('Could not start locked script >>> {}'.format(repr(script)))
            return

        if script.process is not None:
            self.logger.info(
                'Script already running >>> {}'.format(repr(script)))
            return

        self._start_script(script)

    def stop(self, script: Script) -> bool:
        if not script.is_running() or script.process is None:
            return True

        if not script.allow_state_change():
            self.message_service.add(
                Message(MessageType.ERROR, 'Could not stop script, script locked: {}'.format(script.path)))
            self.logger.error('Could not stop script, script locked >>> {}'.format(repr(script)))
            return False

        try:
            script.process.kill()
            script.stop()
            return True
        except OSError as error:
            self.message_service.add(Message(MessageType.ERROR, 'Could not stop script: {}'.format(script.path)))
            self.logger.error('Could not stop script >>> Script: {script} | Error: {error}'.format(
                script=repr(script), error=error))
            return False

    def force_start(self, script: Script):
        success = self._start_script(script)

        if success:
            script.lock()

    def restart(self, script: Script):
        if not script.allow_state_change():
            self.message_service.add(
                Message(MessageType.ERROR, 'Could not restart script: {path}'.format(path=script.path)))
            self.logger.error('Could not restart script >>> {}'.format(repr(script)))
            return

        if not self.stop(script):
            return

        self._start_script(script)

    # endregion command

    def _start_script(self, script: Script) -> bool:
        try:
            process = self.process_manager.start(script.path)
        except OSError as error:
            self.message_service.add(Message(MessageType.ERROR, 'Could not start script: {}'.format(script.path)))
            self.logger.error('Could not start script >>> Script: {script} | Error: {error}'.format(
                script=repr(script), error=error))
            return False

        if process is None:
            self.message_service.add(
                Message(MessageType.ERROR, 'Could not start script: {}'.format(script.path)))
            self.logger.error('Could not start script >>> {}'.format(repr(script)))
            return False

        script.start(process)
        return True

    @staticmethod
    def is_script_file(path: str) -> bool:
        """
        whether should import file or not
        :param path:
        :return: is selected or not
        """
        if not Utility.is_file(path):
            Utility.message_service.add(Message(MessageType.ERROR, 'Path is not a file: {}'.format(path)))
            Utility.logger.error('Path is not a file >>> {}'.format(path))
            return False

        if not Utility.path_exists(path):
            Utility.message_service.add(Message(MessageType.ERROR, 'Path does not exists: {}'.format(path)))
            Utility.logger.error('Path does not exists >>> {}'.format(path))
            return False

        return Utility.get_file_extension(path) in ScriptManager.configuration.utility['file_types']

    # def delete(self, script: Script) -> bool:
    #     # for some reason the script can not be stopped
    #     if not script.stop():
    #         return False

    #     # if file not exists, it success anyway
    #     if not script.exists():
    #         self.logger.info('Script does not exists >>> {}'.format(repr(script)))
    #         return True

    #     # try to delete file
    #     return Utility.remove_file(script.script_path)
