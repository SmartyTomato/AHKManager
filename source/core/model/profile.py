from core.utility.logger import Logger, MethodBoundaryLogger
from core.model.global_variable import GlobalVariable
from core.model.script import Script
from core.model.state import State


class Profile(object):
    _logger = Logger('Profile')

    def __init__(self, name):
        self.state = State()
        self.script_list = []
        self.name = name

    # ------------------------------------------------------------------ #
    # command
    # ------------------------------------------------------------------ #

    @MethodBoundaryLogger(_logger)
    def start(self):
        for script in self.script_list:
            script.start()

        self.state.running = True

    @MethodBoundaryLogger(_logger)
    def stop(self):
        for script in self.script_list:
            script.stop()

        self.state.running = False

    @MethodBoundaryLogger(_logger)
    def restart(self):
        for script in self.script_list:
            script.restart()

    # ------------------------------------------------------------------ #
    # add
    # ------------------------------------------------------------------ #

    @MethodBoundaryLogger(_logger)
    def add_script(self, script):
        """
        add script into the profile
        :param script:
        :return:
        """
        if script is None:
            GlobalVariable.error_messages.append('Could not add None to profile: {name}'.format(name=self.name))
            self._logger.error('Could not add None to profile >>> {name}'.format(name=self.name))
            return False

        self.script_list.append(script)

        # start script right away
        if self.state.running:
            script.start()

        return True

    # ------------------------------------------------------------------ #
    # find
    # ------------------------------------------------------------------ #

    @MethodBoundaryLogger(_logger)
    def find_script(self, path):
        for script in self.script_list:
            if script.has_path(path):
                return script

        self._logger.error('Could not find script >>> {path}'.format(name=self.path))
        return None

    # ------------------------------------------------------------------ #
    # delete
    # ------------------------------------------------------------------ #

    @MethodBoundaryLogger(_logger)
    def remove(self):
        if not self.is_running():
            return True

        has_error = False
        for script in self.script_list:
            success = script.stop()
            if success:
                self.script_list.remove(script)
            else:
                has_error = True
                GlobalVariable.error_messages.append('Could not remove script: {path}'.format(path=script.script_path))
                self._logger.error('Could not remove script >>> {path}'.format(path=script.script_path))

        if has_error:
            GlobalVariable.error_messages.append(
                'Could not remove profile, some script can not be removed: {name}'.format(name=self.name))
            self._logger.error(
                'Could not remove profile, some script can not be removed >>> {name}'.format(name=self.name))

        return has_error

    @MethodBoundaryLogger(_logger)
    def remove_script(self, script):
        if script is not None:
            if script in self.script_list:
                self.script_list.remove(script)
            else:
                GlobalVariable.warning_messages.append(
                    'Script not in profile: Script: {script_path}. Profile: {profile_name}'.format(
                        script_path=script.script_path, profile_name=self.name))
                return True

        # trying to stop the script
        if script.is_running():
            script.stop()

        Logger.log_info('Script removed from profile: Script: {script_path}. Profile: {profile_name}'.format(
            script_path=script.script_path, profile_name=self.name))
        return True

    # ------------------------------------------------------------------ #
    # refresh
    # ------------------------------------------------------------------ #

    def refresh(self):
        # fresh all script in the profile
        # remove script that is not found
        for script in self.script_list:
            success = script.refresh()

            # remove from the script list script failed to refresh
            if not success:
                self.script_list.remove(script)

        Logger.log_info('Profile refreshed')

    # ------------------------------------------------------------------ #
    # others
    # ------------------------------------------------------------------ #

    def has_name(self, name):
        return self.name == name

    def is_running(self):
        return self.state.running

    # ------------------------------------------------------------------ #
    # to string
    # ------------------------------------------------------------------ #

    def __str__(self):
        out = ['Profile:\n\tName: {name}'.format(name=self.name)]

        for script in self.script_list:
            out.append(script.__str__())

        return '\n'.join(out)

    def to_json(self):
        out = {}

        out['name'] = self.name
        out['state'] = self.state.to_json()

        out['scripts'] = []
        for script in self.script_list:
            out['scripts'].append(script.to_json())

        return out

    @staticmethod
    def from_json(json_str):
        profile = Profile(json_str['name'])
        profile.state = State.from_json(json_str['state'])

        for script in json_str['scripts']:
            profile.script_list.append(Script.from_json(script))

        return profile
