from core.utility.logger import Logger, MethodBoundaryLogger
from core.model.global_variable import GlobalVariable
from core.model.profile import Profile
from core.model.repository import Repository


class RepoManager:
    _logger = Logger('RepoManager')

    def __init__(self):
        self._profile_list = []
        self._repository = Repository()

    # --------------------------------------------------------------------#
    # add
    # --------------------------------------------------------------------#
    @MethodBoundaryLogger(_logger)
    def add_library(self, path):
        GlobalVariable.clear_all_messages()
        return self._repository.add_library(path)

    @MethodBoundaryLogger(_logger)
    def add_profile(self, name):
        GlobalVariable.clear_all_messages()
        for profile in self._profile_list:
            if profile.has_name(name):
                GlobalVariable.error_messages.append('Profile name already exists: {name}'.format(name=name))
                self._logger.error('Profile name already exists >>> {profile}'.format(profile=repr(profile)))
                return False

        self._profile_list.append(Profile(name))
        return True

    @MethodBoundaryLogger(_logger)
    def add_script_to_library(self, library_path, script_path):
        GlobalVariable.clear_all_messages()
        return self._repository.add_script_to_library(library_path, script_path)

    @MethodBoundaryLogger(_logger)
    def add_script_to_profile(self, profile_name, script):
        GlobalVariable.clear_all_messages()
        for profile in self._profile_list:
            if profile.has_name(profile_name):
                return profile.add_script(script)

        GlobalVariable.error_messages.append('Could not find profile: {name}'.format(name=profile_name))
        self._logger.error('Could not find profile >>> {name}'.format(name=profile_name))
        return False

    # --------------------------------------------------------------------#
    # find
    # --------------------------------------------------------------------#

    @MethodBoundaryLogger(_logger)
    def find_script(self, path):
        GlobalVariable.clear_all_messages()
        return self._repository.find_script(path)

    @MethodBoundaryLogger(_logger)
    def find_library(self, path):
        GlobalVariable.clear_all_messages()
        return self._repository.find_library(path)

    @MethodBoundaryLogger(_logger)
    def find_all_running_scripts(self):
        GlobalVariable.clear_all_messages()
        return self._repository.find_all_running_scripts()

    @MethodBoundaryLogger(_logger)
    def find_profile(self, name):
        GlobalVariable.clear_all_messages()
        for profile in self._profile_list:
            if profile.has_name(name):
                return profile

        self._logger.info('Profile not found')
        return None

    # --------------------------------------------------------------------#
    # remove methods
    # --------------------------------------------------------------------#

    @MethodBoundaryLogger(_logger)
    def remove_library(self, path):
        GlobalVariable.clear_all_messages()
        return self._repository.remove_library(path)

    @MethodBoundaryLogger(_logger)
    def remove_script(self, path):
        GlobalVariable.clear_all_messages()
        return self._repository.remove_script(path)

    @MethodBoundaryLogger(_logger)
    def remove_profile(self, name):
        profile = self.find_profile(name)

        if profile is None:
            GlobalVariable.error_messages.append(
                'Could not remove profile, profile not found: {name}'.format(name=name))
            self._logger.error('Could not remove profile, profile not found >>> {name}'.format(name=name))
            return False

        if not profile.remove():
            GlobalVariable.add_error_message(
                'Could not remove profile, some script can not be removed: {name}'.format(name=name))
            self._logger.error('Could not remove profile, some script can not be removed >>> {profile}'.format(profile=repr(profile)))
            return False

        return True

    # ------------------------------------------------------------------ #
    # refresh
    # ------------------------------------------------------------------ #

    @MethodBoundaryLogger(_logger)
    def refresh(self):
        GlobalVariable.clear_all_messages()
        self._repository.refresh()
        for profile in self._profile_list:
            profile.refresh()

    # ------------------------------------------------------------------ #
    # to string
    # ------------------------------------------------------------------ #

    @MethodBoundaryLogger(_logger)
    def __str__(self):
        out = [str(self._repository)]

        pout = []
        for profile in self._profile_list:
            pout.append(str(profile))

        out.append('\n'.join(pout))

        return '\n'.join(out)

    @MethodBoundaryLogger(_logger)
    def to_json(self):
        out = {'repository': self._repository.to_json(), 'profiles': []}

        for profile in self._profile_list:
            out['profiles'].append(profile.to_json())

        return out

    @staticmethod
    @MethodBoundaryLogger(_logger)
    def from_json(json_str):
        repo_manager = RepoManager()
        repo_manager._repository = Repository.from_json(json_str['repository'])

        for profile in json_str['profiles']:
            repo_manager._profile_list.append(Profile.from_json(profile))

        return repo_manager
