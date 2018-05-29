from core.utility.logger import Logger
from core.model.global_variable import GlobalVariable
from core.model.profile import Profile
from core.model.repository import Repository


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
        Logger.log_info('Add profile >>> {name}'.format(name=name))

        self.clear_all_messages()
        for profile in self.profile_list:
            if profile.has_name(name):
                GlobalVariable.add_error_message('Profile name already exists >>> {name}'.format(name=name))
                return False

        self.profile_list.append(Profile(name))
        return True

    def add_script_to_library(self, library_path, script_path):
        self.clear_all_messages()
        return self.repository.add_script_to_library(library_path, script_path)

    def add_script_to_profile(self, profile_name, script):
        Logger.log_info('Add scrirpt to profile >>> Profile: {name} | Script: {script}'.format(
            name=profile_name, script=script.script_path))
        self.clear_all_messages()
        for profile in self.profile_list:
            if profile.has_name(profile_name):
                return profile.add_script(script)

        GlobalVariable.add_error_message('Unable to find profile >>> {name}'.format(name=profile_name))
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
        Logger.log_info('Find profile >>> {name}'.format(name=name))

        for profile in self.profile_list:
            if profile.has_name(name):
                return profile

        Logger.log_info('Profile not found')
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

    def remove_profile(self, name):
        Logger.log_info('Remove profile >>> {name}'.format(name=name))

        profile = self.find_profile(name)

        if profile is None:
            GlobalVariable.add_error_message('Unable to remove profile, profile not found >>> {name}'.format(name=name))
            return False

        if not profile.remove():
            GlobalVariable.add_error_message('Unable to remove profile, some script can not be removed >>> {name}'.format(name=name))
            return False

        return True
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
        GlobalVariable.error_messages.clear()
        GlobalVariable.warning_messages.clear()

    # ------------------------------------------------------------------ #
    # to string
    # ------------------------------------------------------------------ #

    def __str__(self):
        Logger.log_info('To string >>> {name}'.format(name=RepoManager.__name__))

        out = []
        out.append(str(self.repository))

        pout = []
        for profile in self.profile_list:
            pout.append(str(profile))

        out.append('\n'.join(pout))

        return '\n'.join(out)

    def to_json(self):
        Logger.log_info('To json >>> {name}'.format(name=RepoManager.__name__))

        out = {}
        out['repository'] = self.repository.to_json()

        out['profiles'] = []
        for profile in self.profile_list:
            out['profiles'].append(profile.to_json())

        return out

    @staticmethod
    def from_json(jstr):
        Logger.log_info('From json >>> {name}'.format(name=RepoManager.__name__))

        repo_manager = RepoManager()
        repo_manager.repository = Repository.from_json(jstr['repository'])

        for profile in jstr['profiles']:
            repo_manager.profile_list.append(Profile.from_json(profile))

        return repo_manager
