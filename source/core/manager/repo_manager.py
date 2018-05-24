from core.utility.logger import Logger
from core.profile import Profile
from core.repository import Repository
from global_variables import error_messages, warning_messages


class RepoManager:

    def __init__(self):
        self.profile_list = []
        self.repository = Repository()

    #--------------------------------------------------------------------#
    # add
    #--------------------------------------------------------------------#

    def add_library(self, path):
        self.clear_all_messages()
        return self.repository.add_library(path)

    def add_profile(self, name):
        self.clear_all_messages()
        for profile in self.profile_list:
            if profile.has_name(name):
                error_messages.append(
                    'Profile name already exists: {name}'.format(name=name))
                return False

        Logger.log_info('Profile added: {name}'.format(name=name))
        return self.profile_list.append(Profile(name))

    def add_script_to_library(self, library_path, script_path):
        self.clear_all_messages()
        return self.repository.add_script_to_library(library_path, script_path)

    def add_script_to_profile(self, profile_name, script):
        self.clear_all_messages()
        for profile in self.profile_list:
            if profile.has_name(profile_name):
                return profile.add_script(script)

        error_messages.append(
            'Can not find profile: {name}'.format(name=profile_name))
        return False

    #--------------------------------------------------------------------#
    # find
    #--------------------------------------------------------------------#

    def find_script(self, path):
        self.clear_all_messages()
        return self.repository.find_script(path)

    def find_library(self, path):
        self.clear_all_messages()
        return self.repository.find_library(path)

    def find_all_running_scripts(self):
        self.clear_all_messages()
        return self.repository.find_all_running_scripts()

    def find_profile(self, name):
        for profile in self.profile_list:
            if profile.has_name(name):
                Logger.log_info('Profile found: {name}'.format(name=name))
                return profile

        return None

    #--------------------------------------------------------------------#
    # remove methods
    #--------------------------------------------------------------------#

    def remove_library(self, path):
        self.clear_all_messages()
        return self.repository.remove_library(path)

    def remove_script(self, path):
        self.clear_all_messages()
        return self.repository.remove_script(path)

    # ------------------------------------------------------------------ #
    # refresh
    # ------------------------------------------------------------------ #

    def refresh(self):
        self.clear_all_messages()
        self.repository.refresh()
        for profile in self.profile_list:
            profile.refresh()

    # ------------------------------------------------------------------ #
    # others
    # ------------------------------------------------------------------ #

    def clear_all_messages(self):
        error_messages.clear()
        warning_messages.clear()

    # ------------------------------------------------------------------ #
    # to string
    # ------------------------------------------------------------------ #

    def __str__(self):
        # todo - add profile as well, currently didn't used anywhere
        return self.repository.__str__()

    def to_json(self):
        out = {}
        out['repository'] = self.repository.to_json()

        out['profiles'] = []
        for profile in self.profile_list:
            out['profiles'].append(profile.to_json())

        return out

    @staticmethod
    def from_json(jstr):
        repo_manager = RepoManager()
        repo_manager.repository = Repository.from_json(jstr['repository'])

        for profile in jstr['profiles']:
            repo_manager.profile_list.append(Profile.from_json(profile))

        return repo_manager
