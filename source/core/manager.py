import os

from source.core.profile import Profile
from source.core.repository import Repository


class Manager:
    def __init__(self):
        self.profile_list = []
        self.repository = Repository()

    def add_repository(self, path):
        self.repository.add_path(path)

    def add_profile(self,name):
        self.profile_list.append(Profile(name))

    def add_script_to_profile(self,profile_name, script):
        for profile in self.profile_list:
            if profile.name == profile_name:
                profile.add(script)

    def remove_repository(self, path):
        # todo - remove from the profile as well
        for library in self.repository.library_list:
            if library.library_path == path:
                self.repository.library_list.remove(library)
                return

    def to_string(self):
        values = []

        for library in self.repository.library_list:
            values.extend(library.to_string())

        values.append('')

        return values

    def find_script(self,path):
        return self.repository.find_script(path)