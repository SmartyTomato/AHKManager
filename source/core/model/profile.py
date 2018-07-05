from typing import List
from core.model.state import State


class Profile(object):

    def __init__(self, name):
        self.name: str = name
        self.state: State = State()
        self.script_id_list: List[str] = []

    # region public methods

    def start(self):
        self.state.running = True

    def stop(self):
        self.state.running = False

    def add(self, script_id: str):
        self.script_id_list.append(script_id)

    def remove(self,script_id:str):
        if script_id in self.script_id_list:
            self.script_id_list.remove(script_id)

    def has_script(self, identifier: str)->bool:
        return identifier in self.script_id_list

    def has_id(self, identifier: str) -> bool:
        return identifier == self.identifier()

    def identifier(self) -> str:
        return self.name

    def is_running(self) -> bool:
        return self.state.running

    # endregion public methods

    # region string

    def to_json(self):
        out = {}
        out['name'] = self.name

        out['state'] = self.state.to_json()

        out_script_id_list = []
        for script_id in self.script_id_list:
            out_script_id_list.append(script_id)

        out['script_id_list'] = out_script_id_list

        return out

    @staticmethod
    def from_json(json_str):
        name = json_str['name']
        profile = Profile(name)
        profile.state = State.from_json(json_str['state'])

        for script_id in json_str['script_id_list']:
            profile.script_id_list.append(script_id)

        return profile

    def __str__(self):
        out = []
        out.append('Profile:')
        out.append('\t Name: {}'.format(self.name))
        out.append('\t State: {}'.format(str(self.state)))

        for script_id in self.script_id_list:
            out.append(script_id)

        return '\n'.join(out)

    def __repr__(self):
        out = 'Profile('
        out += 'name={}, '.format(self.name)
        out += 'state={}, '.format(repr(self.state))
        out += 'script_count={}'.format(len(self.script_id_list))
        out += ')'

        return out

    # endregion string
