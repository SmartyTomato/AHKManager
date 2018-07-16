from typing import List

from core.model.script import Script
from core.model.state import State
from core.utility.utility import Utility


class Library(object):

    def __init__(self, path: str):
        self.state: State = State()
        self.name: str = Utility.get_file_name_no_extension(path)
        self.path: str = Utility.format_path(path)
        self.script_list: List[Script] = []

    # region public methods

    def start(self):
        self.state.running = True

    def stop(self):
        self.state.running = False

    def add(self, script: Script):
        if self._is_script_instance(script):
            self.script_list.append(script)

    def remove(self, script: Script):
        if self. _is_script_instance(script) and script in self.script_list:
            self.script_list.remove(script)

    def find(self, identifier: str) -> Script:
        # below statement will benefit when large amount script in the library
        if not self.may_contains_script(identifier):
            return None

        # loop to find the script
        for script in self.script_list:
            if script.has_id(identifier):
                return script

        return None

    def find_running_scripts(self) -> List[Script]:
        scripts = []

        for script in self.script_list:
            if script.is_running():
                scripts.append(script)

        return scripts

    def has_script(self, script: Script) -> bool:
        return script in self.script_list

    def has_id(self, identifier: str) -> bool:
        return identifier == self.identifier()

    def identifier(self) -> str:
        return self.path

    def is_running(self) -> bool:
        return self.state.running

    def exists(self) -> bool:
        return Utility.path_exists(self.path)

    def may_contains_script(self, identifier: str) -> bool:
        return self.path == Utility.format_path(Utility.get_parent_directory(identifier))

    # endregion public methods

    # region private methods

    @staticmethod
    def _is_script_instance(instance: object) -> bool:
        if instance and isinstance(instance, Script):
            return True
        else:
            return False

    # endregion private methods

    # region to string

    def to_json(self):
        out = {}

        out['path'] = self.path
        out['name'] = self.name
        out['state'] = self.state.to_json()

        out_script_list = []
        for script in self.script_list:
            out_script_list.append(script.to_json())

        out['script_list'] = out_script_list

        return out

    @staticmethod
    def from_json(json_str):
        path = json_str['path']
        library = Library(path)
        library.name = json_str['name']
        library.state = State.from_json(json_str['state'])

        for script in json_str['script_list']:
            library.script_list.append(Script.from_json(script))

        return library

    def __str__(self):
        out = []
        out.append('Library:')
        out.append('\t Name: {}'.format(self.name))
        out.append('\t Path: {}'.format(self.path))
        out.append('\t State: {}'.format(str(self.state)))

        for script in self.script_list:
            out.append(str(script))

        return '\n'.join(out)

    def __repr__(self):
        out = 'Library('
        out += 'name={}, '.format(self.name)
        out += 'path={}, '.format(self.path)
        out += 'state={}, '.format(repr(self.state))
        out += 'script_count={}'.format(len(self.script_list))
        out += ')'

        return out

    # endregion to string
