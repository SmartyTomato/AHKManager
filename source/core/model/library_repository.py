from typing import List

from core.model.library import Library
from core.model.script import Script


class LibraryRepository(object):

    def __init__(self):
        self.library_list: List[Library] = []

   # region public methods

    def add(self, library: Library):
        if self._is_instance(library):
            self.library_list.append(library)

    def find(self, identifier: str) ->Library:
        for library in self.library_list:
            if library.has_id(identifier):
                return library

        return None

    def find_script(self, identifier: str) -> Script:
        for library in self.library_list:
            script = library.find(identifier)
            if script:
                return script

        return None

    def remove_script(self, script: Script):
        for library in self.library_list:
            if library.find(script.identifier()):
                library.remove(script)
                return

    def remove(self, instance: Library):
        if self._is_instance(instance) and instance in self.library_list:
            self.library_list.remove(instance)

    def get_all_scripts(self)->List[Script]:
        scripts = []
        for library in self.library_list:
            scripts.extend(library.script_list)

        return scripts

    # endregion public methods

  # region private methods

    @staticmethod
    def _is_instance(instance) -> bool:
        if instance and isinstance(instance, Library):
            return True
        else:
            return False

    # endregion private methods

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
