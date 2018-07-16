from typing import List

from core.model.profile import Profile
from core.model.script import Script


class ProfileRepository(object):

    def __init__(self):
        self.profile_list: List[Profile] = []

    # region public methods

    def add(self, profile: Profile):
        if self._is_instance(profile):
            self.profile_list.append(profile)

    def find(self, identifier: str) ->Profile:
        for profile in self.profile_list:
            if profile.has_id(identifier):
                return profile

        return None

    def find_script(self, identifier: str) -> Script:
        for profile in self.profile_list:
            bl = profile.has_script(identifier)
            if bl:
                return identifier

        return None

    def remove_script(self, script: Script):
        for profile in self.profile_list:
            if profile.find(script.identifier()):
                profile.remove(script)
                return

    def remove(self, instance: Profile):
        if self._is_instance(instance) and instance in self.profile_list:
            self.profile_list.remove(instance)

    # endregion public methods

    # region private methods

    @staticmethod
    def _is_instance(instance) -> bool:
        if instance and isinstance(instance, Profile):
            return True
        else:
            return False

    # endregion private methods

    # region to string

    def to_json(self):
        out = {}
        out['profile_list'] = []
        for profile in self.profile_list:
            out['profile_list'].append(profile.to_json())

        return out

    @staticmethod
    def from_json(json_str):
        repo = ProfileRepository()

        for profile in json_str['profile_list']:
            repo.profile_list.append(Profile.from_json(profile))

        return repo

    def __str__(self):
        out = []
        out.append('Profile repository:')

        for profile in self.profile_list:
            out.append(str(profile))

        return '\n'.join(out)

    def __repr__(self):
        out = 'ProfileRepository('
        out += 'library_count={}'.format(len(self.profile_list))
        out += ')'

        return out

    # endregion to string
