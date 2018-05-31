import os
import sys

from core.utility.logger import Logger
from core.utility.utility import Utility
from core.model.global_variable import GlobalVariable
from core.model.state import State


class Script(object):
    _logger = Logger('Script')

    def __init__(self):
        self.title = ''
        self.script_path = ''
        self.status = State()
        self.process = None

    def init(self):
        """
        initialize variables
        :return: void
        """
        self.title = ''
        self.script_path = ''
        self.status = State()
        self.process = None

    def init_script(self, path):
        """
        initialize script with file path, all parameter will reset
        :param path: file path
        :return: bool, whether success
        """
        # check if path is a file
        if not os.path.isfile(path):
            GlobalVariable.warning_messages.append(
                'Path is not a valid file path: {path}'.format(path=path))
            return False

        # check if path exists
        if not os.path.exists(path):
            GlobalVariable.warning_messages.append(
                'Path does not exists: {path}'.format(path=path))
            return False

        # check if path not the file type we want
        if not Utility.is_script_file(path):
            GlobalVariable.warning_messages.append(
                'Path not a script file: {path}'.format(path=path))
            return False

        self.init()
        self.title = Utility.get_file_name_no_extension(path)
        self.script_path = os.path.normpath(path)

        return True

    # ------------------------------------------------------------------ #
    # command
    # ------------------------------------------------------------------ #

    def start(self):
        if not self.allow_state_change():
            if self.is_running():
                return True

            return False

        if self.process is not None:
            return self.restart()

        return self.start_script()

    def force_start(self):
        success = self.start()

        if success:
            Logger.log_info('Force start script: {path}'.format(
                path=self.script_path))
            self.lock()
            return True
        else:
            return False

    def stop(self):
        if not self.allow_state_change():
            if self.is_running():
                GlobalVariable.warning_messages.append(
                    'Unable to stop script, script locked: {path}'.format(path=self.script_path))
                return False
            else:
                Logger.log_info('Trying to stop script when script locked: {path}'.format(
                    path=self.script_path))
                return True

        if self.process is None:
            Logger.log_info('Trying to stop script when it not running')
            return True

        try:
            self.process.kill()
            self.process = None
            self.status.running = False
            Logger.log_info('Script stopped: {path}'.format(
                path=self.script_path))
            return True
        except OSError as error:
            GlobalVariable.warning_messages.append('Unable to stop script: {path}. {msg}'.format(
                path=self.script_path, msg=error))
            return False

    def restart(self):
        if not self.allow_state_change():
            GlobalVariable.warning_messages.append(
                'Unable to restart script: {path}'.format(path=self.script_path))
            return False

        if not self.stop():
            return False

        success = self.start_script()

        if not success:
            GlobalVariable.warning_messages.append(
                'Unable to restart script: {path}'.format(path=self.script_path))
            return False

        Logger.log_info('Script restarted: {path}'.format(
            path=self.script_path))
        return True

    def start_script(self):
        try:
            process = GlobalVariable.get_process_manager().start(self.script_path)
        except OSError as error:
            GlobalVariable.warning_messages.append('Unable to start script: {path}. {msg}'.format(
                path=self.script_path, msg=error))
            return False

        if process is None:
            GlobalVariable.warning_messages.append(
                'Unable to start: {path}'.format(path=self.script_path))
            return False

        self.process = process
        self.status.running = True
        Logger.log_info('Script started: {path}'.format(path=self.script_path))
        return True

    # ------------------------------------------------------------------ #
    # delete
    # ------------------------------------------------------------------ #

    def remove(self):
        """
        remove script, exclude and hide from the library. Do not delete file
        :return: void
        """
        # for some reason we can not stop the script, do not hide script in that case
        if not self.stop():
            return False

        self.exclude()
        self.hide()
        Logger.log_info('Script removed: {path}'.format(path=self.script_path))
        return True

    def delete(self):
        """
        delete the script and file
        :return: bool, whether success
        """
        # if file not exists, it success anyway
        if not self.exists():
            GlobalVariable.warning_messages.append(
                'Script does not exists: {path}'.format(path=self.script_path))
            return True

        # for some reason the script can not be stopped
        if not self.stop():
            return False

        # try to delete file
        try:
            os.remove(self.script_path)
        except OSError as error:
            GlobalVariable.warning_messages.append('Unable to delete file: {path}. {msg}'
                                                   .format(path=self.script_path, msg=error))
            return False
        except:
            # unknown error
            GlobalVariable.warning_messages.append('Unknown error when delete file {path}. {msg}'
                                                   .format(path=self.script_path, msg=sys.exc_info()[0].value))
            return False

        Logger.log_info('Script deleted: {path}'.format(path=self.script_path))
        return True

    # ------------------------------------------------------------------ #
    # refresh
    # ------------------------------------------------------------------ #

    def refresh(self):
        """
        refresh script status and check whether file exists
        :return: bool, whether success
        """
        if not self.exists():
            GlobalVariable.warning_messages.append(
                'Script does not exists: {path}'.format(path=self.script_path))
            return False

        Logger.log_info('Script refreshed: {path}'.format(
            path=self.script_path))
        return True

    # ------------------------------------------------------------------ #
    # others
    # ------------------------------------------------------------------ #

    def show(self):
        """
        should show script or not
        :return: bool
        """
        return not (self.status.exclude or self.status.hide)

    def has_path(self, path):
        """
        check script has given file path
        Usage: use to find script in library
        :param path:
        :return: bool
        """
        return self.script_path == os.path.normpath(path)

    def exists(self):
        return os.path.exists(self.script_path)

    def allow_state_change(self):
        return self.show() and not self.is_locked()

    def lock(self):
        self.status.lock = True

    def is_locked(self):
        return self.status.lock

    def startup(self):
        self.status.startup = True

    def exclude(self):
        self.status.exclude = True

    def hide(self):
        self.status.hide = True

    def is_running(self):
        return self.status.running

    # ------------------------------------------------------------------ #
    # to string
    # ------------------------------------------------------------------ #

    def __str__(self):
        """
        to string
        :return: single string value
        """
        return 'Script:\n\tTitle: {title}\n\tPath: {path}'.format(title=self.title, path=self.script_path)

    def to_json(self):
        out = {}

        out['title'] = self.title
        out['script_path'] = self.script_path
        out['state'] = self.status.to_json()

        return out

    @staticmethod
    def from_json(jstr):
        script = Script()
        script.title = jstr['title']
        script.script_path = jstr['script_path']
        script.status = State.from_json(jstr['state'])

        return script
