import os

from source.core.common import get_files_in_directory
from source.core.script import Script


class Library(object):
    def __init__(self, path):
        self.library_path = path
        self.script_list = []
        self.init_dir(path)

    def init_dir(self, path):
        """
        initialize library with directory
        :param path:
        """
        # add script in the directory in to the list
        files = get_files_in_directory(path)

        # initialize script file
        for file in files:
            self.script_list.append(Script(file))

    def find_script(self, path):
        """
        find script in the library
        :param path:
        :return: script object
        """
        for script in self.script_list:
            if script.script_path == path:
                return script

    def to_string(self):
        values = [self.library_path]

        for script in self.script_list:
            values.append(script.script_path)

        values.append('')

        return values
