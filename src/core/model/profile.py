from typing import List

from src.core.model.state import State


class Profile():
    """
    Profile is a script container, stores a list of script IDs.

    Profile stores script ID only, not script object.
    If script id needed use ProfileService,
    search in library repository using the script id
    The script ids can be used to search script in the library.

    Profile uses name as ID, which uniquely exists in the system
    """

    def __init__(self, name):
        self.name: str = name
        self.state: State = State()
        self.script_id_list: List[str] = []

    # region public methods

    def start(self):
        """
        Set profile running state to true
        """

        self.state.running = True

    def stop(self):
        """
        Set profile running state to false
        """

        self.state.running = False

    def add(self, script_id: str):
        """
        Add script into profile

        Args:
            script_id (str): script id
        """

        self.script_id_list.append(script_id)

    def remove(self, script_id: str):
        """
        Remove script from the profile

        Args:
            script_id (str):
        """

        if script_id in self.script_id_list:
            self.script_id_list.remove(script_id)

    def has_script(self, identifier: str) -> bool:
        """
        Check whether profile contains script

        Args:
            identifier (str): script id

        Returns:
            bool: return true script id found
        """

        if identifier in self.script_id_list:
            return True

        return False

    def has_id(self, identifier: str) -> bool:
        """
        Check if profile has given ID (name)

        Args:
            identifier (str): profile name

        Returns:
            bool: return true if profile name is
                the same as the given ID
        """

        return identifier == self.identifier()

    def identifier(self) -> str:
        """
        Get profile ID

        Returns:
            str: profile name
        """

        return self.name

    def is_running(self) -> bool:
        """
        Get profile current running state

        Returns:
            bool: return true when profile is running
        """

        return self.state.running

    def is_paused(self):
        return False

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
