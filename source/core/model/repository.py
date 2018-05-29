import os

from core.utility.logger import Logger
from core.utility.utility import get_directories
from core.model.global_variable import GlobalVariable
from core.model.library import Library


class Repository(object):

    def __init__(self):
        self.init()

    def init(self):
        self.library_list = []

    # ------------------------------------------------------------------ #
    # add
    # ------------------------------------------------------------------ #
    def add_library(self, path):
        # check if path is a directory
        if not os.path.isdir(path):
            GlobalVariable.error_messages .append(
                'Path is not a valid directory path: {path}'.format(path=path))
            return False

        # check if path is
        if not os.path.exists(path):
            GlobalVariable.error_messages.append(
                'Path does not exists: {path}'.format(path=path))
            return False

        # add path itself to list
        library = Library()
        success = library.init_library(path)
        if success:
            self.library_list.append(library)

        # get all sub directories
        directories = get_directories(path)

        # create all library (folder) object
        for directory in directories:
            library = Library()
            success = library.init_library(directory)
            if success:
                self.library_list.append(library)

        Logger.log_info(
            'Add library into repository: {path}'.format(path=path))
        return True

    def add_script_to_library(self, library_path, script_path):
        library = self.find_library(library_path)

        if library is not None:
            return library.add_script(script_path)
        else:
            GlobalVariable.error_messages.append(
                'Unable to find library'.format(path=library_path))
            return False

    # ------------------------------------------------------------------ #
    # find
    # ------------------------------------------------------------------ #

    def find_script(self, path):
        """
        find script using given path
        script should have unique path in the library
        :param path: file path
        :return: script object or none
        """
        for library in self.library_list:
            if library.may_contains_script(path):
                script = library.find_script(path)
                if script is not None:
                    return script

        return None

    def find_library(self, path):
        for library in self.library_list:
            if library.has_path(path):
                return library

        return None

    def find_all_running_scripts(self):
        scripts = []

        for library in self.library_list:
            scripts.extend(library.find_all_running_scripts())

        return scripts

    # ------------------------------------------------------------------ #
    # delete
    # ------------------------------------------------------------------ #

    def remove_library(self, path):
        for library in self.library_list:
            if library.has_path(path):
                return library.remove()

    def remove_script(self, path):
        for library in self.library_list:
            if library.may_contains_script(path):
                return library.remove_script(path)

    def delete_library(self, path):
        library = self.find_library(path)
        if library is None:
            # can not find library
            GlobalVariable.warning_messages.append(
                'Library does not exists: {path}'.format(path=path))
            return True

        success = library.delete()
        # only remove from the list when no error occurs
        if success:
            self.library_list.remove(library)
            Logger.log_info(
                'Library deleted from repository: {path}'.format(path=path))
            return True
        # unable to delete file
        else:
            return False

    def delete_script(self, path):
        for library in self.library_list:
            if library.may_contains_script(path):
                return library.delete_script(path)

        GlobalVariable.warning_messages.append(
            'Script does not exists: {path}'.format(path=path))
        return True

    # ------------------------------------------------------------------ #
    # refresh
    # ------------------------------------------------------------------ #

    def refresh(self):
        for library in self.library_list:
            success = library.refresh()

            # only false when library not exists. So remove it from the repository
            if not success:
                self.library_list.remove(library)

        Logger.log_info('Repository refreshed')

    # ------------------------------------------------------------------ #
    # to string
    # ------------------------------------------------------------------ #

    def __str__(self):
        out = []

        for library in self.library_list:
            out.append(library.__str__())

        return '\n'.join(out)

    def to_json(self):
        out = {}
        out['libraries'] = []
        for library in self.library_list:
            out['libraries'].append(library.to_json())

        return out

    @staticmethod
    def from_json(jstr):
        repo = Repository()

        for library in jstr['libraries']:
            repo.library_list.append(Library.from_json(library))

        return repo
