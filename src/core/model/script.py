from typing import Optional

from subprocess import Popen

from core.model.state import State
from core.utility.utility import Utility


class Script():
    """
    Script is a AutoHotKey file
    """

    utility: Utility = Utility()

    def __init__(self, path: str) -> None:
        self.name: str = self.utility.get_file_name_no_extension(path)
        self.path: str = self.utility.format_path(path)
        self.state: State = State()
        self.process: Optional[Popen] = None

    # region public methods

    def start(self, process: Popen):
        """
        Set script running state to true

        Args:
            process (Popen): Popen object,
                can be used to terminate process
        """

        self.process = process
        self.state.running = True

    def stop(self):
        """
        Set script running state to false
        """

        self.process = None
        self.state.running = False

    def pause(self):
        """
        Set script to paused
        """
        self.process = None
        self.state.paused = True

    def is_paused(self):
        return self.state.paused

    def identifier(self)->str:
        """
        Get script identifier

        Returns:
            str: script file path
        """

        return self.path

    def has_id(self, identifier: str)->bool:
        """
        Check if script has given ID

        Args:
            identifier (str): script path

        Returns:
            bool:
        """

        _id = self.utility.format_path(identifier)
        return self.identifier() == _id

    def exists(self) -> bool:
        """
        Check whether script is an existing file with valid file path

        Returns:
            bool:
        """

        return self.utility.is_file(self.path)

    def allow_state_change(self) -> bool:
        """
        Check whether start or stop script is allowed

        Script may locked by force start

        Returns:
            bool:
        """

        return not self.is_locked()

    def is_locked(self) -> bool:
        """
        Get script locked state

        Returns:
            bool:
        """

        return self.state.lock

    def lock(self):
        """
        Set script locked state to true
        """

        self.state.lock = True

    def startup(self):
        """
        Set script startup state to true
        """

        self.state.startup = True

    def is_running(self) -> bool:
        """
        Get script running state

        Returns:
            bool:
        """

        return self.state.running

    # endregion public methods

    # region string

    def to_json(self):
        out = {}

        out['name'] = self.name
        out['path'] = self.path
        out['state'] = self.state.to_json()

        return out

    @staticmethod
    def from_json(json_str):
        path = json_str['path']
        script = Script(path)
        script.name = json_str['name']
        script.state = State.from_json(json_str['state'])

        return script

    def __str__(self):
        out = []
        out.append('Script:')
        out.append('\t Name: {}'.format(self.name))
        out.append('\t Path: {}'.format(self.path))
        out.append('\t State: {}'.format(str(self.state)))

        return '\n'.join(out)

    def __repr__(self):
        out = 'Script('
        out += 'name={}, '.format(self.name)
        out += 'path={}, '.format(self.path)
        out += 'state={}'.format(repr(self.state))
        out += ')'

        return out

    # endregion string
