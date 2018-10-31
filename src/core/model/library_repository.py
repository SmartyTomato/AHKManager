from typing import List

from core.model.library import Library
from core.model.script import Script


class LibraryRepository():
    """
    Library repository is a library container.
    Stores a list of libraries
    """

    def __init__(self):
        self.library_list: List[Library] = []

    # region public methods

    def add(self, library: Library):
        """
        Add library into the repository

        Args:
            library (Library): library object
        """

        self.library_list.append(library)

    def find(self, identifier: str) -> Library:
        """
        Find the library has the given id

        Args:
            identifier (str): Library identifier (path)

        Returns:
            Library: library object or None
        """

        return next(
            (x for x in self.library_list if x.has_id(identifier)), None)

    def find_script(self, identifier: str) -> Script:
        """
        Find script has given id

        Args:
            identifier (str): Script path

        Returns:
            Script: script object or None
        """

        for library in self.library_list:
            script = library.find(identifier)
            if script:
                return script

        return None

    def remove(self, instance: Library):
        """
        Remove library from the repository

        Args:
            instance (Library): library instance
        """

        if instance in self.library_list:
            self.library_list.remove(instance)

    def get_all_scripts(self) -> List[Script]:
        """
        Get all scripts from all libraries

        Returns:
            List[Script]: list of scripts
        """

        scripts: List[Script] = []
        for library in self.library_list:
            scripts.extend(library.script_list)

        return scripts

    # endregion public methods

    # region to string

    def to_json(self):
        out = {}

        out_library_list = []
        for library in self.library_list:
            out_library_list.append(library.to_json())

        out['library_list'] = out_library_list

        return out

    @staticmethod
    def from_json(json_str):
        repo = LibraryRepository()

        for library in json_str['library_list']:
            repo.library_list.append(Library.from_json(library))

        return repo

    def __str__(self):
        out = []
        out.append('Library repository:')

        for library in self.library_list:
            out.append(str(library))

        return '\n'.join(out)

    def __repr__(self):
        out = 'LibraryRepository('
        out += 'library_count={}'.format(len(self.library_list))
        out += ')'

        return out

    # endregion to string
