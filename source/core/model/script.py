from subprocess import Popen

from core.model.state import State
from core.utility.utility import Utility


class Script(object):

    def __init__(self, path: str):
        self.name: str = Utility.get_file_name_no_extension(path)
        self.path: str = Utility.format_path(path)
        self.state: State = State()
        self.process: Popen = None

    # region public methods

    def start(self, process):
        self.process = process
        self.state.running = True

    def stop(self):
        self.process = None
        self.state.running = False

    def identifier(self)->str:
        return self.path

    def has_id(self, identifier: str)->bool:
        return self.identifier() == identifier

    def exists(self) -> bool:
        return Utility.path_exists(self.path)

    def allow_state_change(self) -> bool:
        return not self.is_locked()

    def is_locked(self):
        return self.state.lock

    def lock(self):
        self.state.lock = True

    def startup(self):
        self.state.startup = True

    def is_running(self):
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
        out +='name={}, '.format(self.name)
        out +='path={}, '.format(self.path)
        out +='state={}'.format(repr(self.state))
        out += ')'

        return out

    # endregion string
