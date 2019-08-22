from typing import List

from src.core.model.script import Script
from src.core.model.state import State
from src.core.utility.utility import Utility


class Library():
    """
    Library is a script container,
    which directly map to the file system (directory/folder)

    Library uses directory path as ID, which uniquely exists in the system
    """
    utility: Utility = Utility()

    def __init__(self, path: str) -> None:
        self.state: State = State()
        self.name: str = self.utility.get_file_name_no_extension(path)
        self.path: str = self.utility.format_path(path)
        self.script_list: List[Script] = []

    # region public methods

    def start(self):
        """
        Set library running state to True
        """

        self.state.running = True

    def stop(self):
        """
        Set library running state to False
        """

        self.state.running = False

    def pause(self):
        """
        Set library to paused state
        """

        self.state.paused = True

    def is_paused(self):
        return self.state.paused

    def resume(self):
        self.state.paused = False
        self.start()

    def add(self, script: Script):
        """
        Add script into the library

        Args:
            script (Script): script object
        """

        self.script_list.append(script)

    def remove(self, script: Script):
        """
        Remove script from the library

        Args:
            script (Script): script object
        """

        if script in self.script_list:
            self.script_list.remove(script)

    def find(self, identifier: str) -> Script:
        """
        Find the script using given identifier (path)

        Args:
            identifier (str): script identifier (path)

        Returns:
            Script: script object
        """

        # below statement will benefit when large amount script
        if not self.may_contains_script(identifier):
            return None

        # loop to find the script
        return next(
            (x for x in self.script_list if x.has_id(identifier)), None)

    def find_running_scripts(self) -> List[Script]:
        """
        Find all running scripts

        Returns:
            List[Script]: list of scripts
        """

        return list(filter(lambda x: x.is_running(), self.script_list))

    def has_script(self, identifier: str) -> bool:
        """
        Check whether library contains script

        Args:
            identifier (str): script ID

        Returns:
            bool: return true when script in the library
        """

        for script in self.script_list:
            if script.has_id(identifier):
                return True

        return False

    def has_id(self, identifier: str) -> bool:
        """
        Check whether library has given identifier (path)

        Args:
            identifier (str): library id (path)

        Returns:
            bool: return true when id matches
        """

        _id = self.utility.format_path(identifier)
        return self.identifier() == _id

    def identifier(self) -> str:
        """
        Get library identifier (path)

        Returns:
            str: library path
        """

        return self.path

    def is_running(self) -> bool:
        """
        Whether library is running

        Returns:
            bool: return true when library is running.
                This does not check each script is
                running or not
        """

        return self.state.running and not self.state.paused

    def exists(self) -> bool:
        """
        Check whether library path is valid
        and path is an exists directory

        Returns:
            bool: return true if library path is
                valid and exists
        """

        return self.utility.is_dir(self.path)

    def may_contains_script(self, identifier: str) -> bool:
        """
        Check whether library may contains script
        by comparing script's parent directory to library path

        Args:
            identifier (str): script identifier (path)

        Returns:
            bool: return true when library path matches
                script's parent directory
        """

        return self.path == self.utility.format_path(
            self.utility.get_parent_directory(identifier))

    # endregion public methods

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
