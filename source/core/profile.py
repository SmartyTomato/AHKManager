from core.utility.logger import Logger
from core.script import Script
from core.status import Status
from global_variables import warning_messages


class Profile(object):

    def __init__(self, name):
        self.status = Status()
        self.script_list = []
        self.name = name

    # ------------------------------------------------------------------ #
    # command
    # ------------------------------------------------------------------ #

    def start(self):
        for script in self.script_list:
            script.start()

        self.status.running = True
        Logger.log_info('Profile started: {name}'.format(name=self.name))

    def stop(self):
        for script in self.script_list:
            script.stop()

        self.status.running = False
        Logger.log_info('Profile stopped: {name}'.format(name=self.name))

    def restart(self):
        for script in self.script_list:
            script.restart()

        Logger.log_info('Profile restarted: {name}'.format(name=self.name))

    # ------------------------------------------------------------------ #
    # add
    # ------------------------------------------------------------------ #

    def add_script(self, script):
        """
        add script into the profile
        :param script:
        :return:
        """
        if script is not None:
            self.script_list.append(script)

        # start script right away
        if self.status.running:
            script.start()

        Logger.log_info('Script added into profile: Script: {script_path}. Profile: {profile_name}'.format(
            script_path=script.script_path, profile_name=self.name))

    # ------------------------------------------------------------------ #
    # find
    # ------------------------------------------------------------------ #

    def find_script(self, path):
        for script in self.script_list:
            if script.has_path(path):
                Logger.log_info('Script found: {path}'.format(path=path))
                return script

        return None

    # ------------------------------------------------------------------ #
    # delete
    # ------------------------------------------------------------------ #

    def remove_script(self, script):
        if script is not None:
            if script in self.script_list:
                self.script_list.remove(script)
            else:
                warning_messages.append('Script not in profile: Script: {script_path}. Profile: {profile_name}'.format(
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

    # ------------------------------------------------------------------ #
    # to string
    # ------------------------------------------------------------------ #

    def to_json(self):
        out = {}

        out['name'] = self.name
        out['status'] = self.status.to_json()

        out['scripts'] = []
        for script in self.script_list:
            out['scripts'].append(script.to_json())

        return out

    @staticmethod
    def from_json(jstr):
        profile = Profile(jstr['name'])
        profile.status = Status.from_json(jstr['status'])

        for script in jstr['scripts']:
            profile.script_list.append(Script.from_json(script))

        return profile
