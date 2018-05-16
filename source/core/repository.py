from source.core.library import Library
from source.core.common import scan_directory, get_directories
from source.core.script import Script


class Repository(object):
    def __init__(self):
        self.library_list = []
        self.profile_list = []

    def init_path(self, path):
        # Get all directories
        dirs = get_directories(path)

        # create all library (folder) object
        for dir in dirs:
            self.library_list.append(Library(dir))

    def find_script(self, path):
        """
        find script using given path
        script should have unique path in the library
        :param path:
        :return: script object
        """
        for lib in self.library_list:
            script = lib.find_script(path)
            if script is not None:
                return script

    def add_library(self, library):
        """
        add library to the repository
        :param library:
        :return:
        """
        if library is not None:
            self.library_list.append(library)

    def add_path(self, path):
        self.init_path(path)