from typing import List

from src.core.model.profile import Profile


class ProfileRepository():
    """
    Profile repository is a profile container.
    Stores a list of profiles
    """

    def __init__(self):
        self.profile_list: List[Profile] = []

    # region public methods

    def add(self, profile: Profile):
        """
        Add profile into repository

        Args:
            profile (Profile): profile objectobject
        """

        self.profile_list.append(profile)

    def find(self, identifier: str) -> Profile:
        """
        Find profile using the identifier (name)

        Args:
            identifier (str): profile name

        Returns:
            Profile: profile object or None
        """

        return next((x for x in self.profile_list
                     if x.has_id(identifier)), None)

    def remove(self, instance: Profile):
        """
        Remove profile

        Args:
            instance (Profile): profile instance
        """

        if instance in self.profile_list:
            self.profile_list.remove(instance)

    # endregion public methods

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
