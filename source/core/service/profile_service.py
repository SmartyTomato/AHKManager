from typing import List

from core.manager.profile_manager import ProfileManager
from core.manager.script_manager import ScriptManager
from core.model.profile import Profile
from core.model.script import Script
from core.model.profile_repository import ProfileRepository
from core.model.singleton import Singleton
from core.service.library_service import LibraryService
from core.service.message_service import MessageService
from core.utility.logger import Logger
from core.utility.message import Message, MessageType


class ProfileService(Singleton):
    logger = Logger('ProfileService')

    message_service: MessageService = MessageService()
    library_service: LibraryService = LibraryService()
    profile_manager: ProfileManager = ProfileManager()
    script_manager: ScriptManager = ScriptManager()

    def __init__(self):
        self.repository: ProfileRepository = ProfileRepository()

    # region add

    def add(self, name: str = '') -> Profile:
        profile = self.repository.find(name)
        if profile:
            self.message_service.add(
                Message(MessageType.ERROR, 'Profile name already exists: {}'.format(name)))
            self.logger.error('Profile name already exists >>> {}'.format(repr(profile)))
            return None

        if not name:
            name = self.get_next_profile_name()

        profile = self.profile_manager.init_profile(name)
        if not profile:
            self.message_service.add(
                Message(MessageType.ERROR, 'Could not add profile: {}'.format(name)))
            self.logger.error('Could not add profile >>> {}'.format(repr(name)))
            return None

        return self.repository.add(profile)

    def add_script(self, name: str, script_id: str):
        profile = self._profile_exists(name)
        if not profile:
            return False

        script = self.find_script(script_id)
        if script:
            self.message_service.add(
                Message(MessageType.WARNING, 'Profile already contains script: {}'.format(script.identifier())))
            self.logger.warning('Profile already contains script >>> Script: {}'.format(repr(script)))
            return False

        script = self.library_service.find_script(script_id)
        if not script:
            self.message_service.add(
                Message(MessageType.ERROR, 'Could not find script in the repository: {}'.format(script_id)))
            self.logger.error('Could not find script in the repository >>> {}'.format(script_id))

        return self.profile_manager.add_script(profile, script)

    # endregion add

    # region find

    def find(self, identifier: str) -> Profile:
        profile = self.repository.find(identifier)
        if not profile:
            self.logger.info('Could not find profile >>> {}'.format(identifier))
            return None

        return profile

    def find_script(self, identifier: str) ->Script:
        profile = self.find_profile_contains_script(identifier)
        if not profile:
            return None

        script = self.library_service.find_script(identifier)
        if not script:
            return None

        return script

    def find_profile_contains_script(self, script_id: str)->Profile:
        for profile in self.repository.profile_list:
            if profile.has_script(script_id):
                return profile

        self.message_service.add(
            Message(MessageType.ERROR, 'Could not find profile contains script: {}'.format(script_id)))
        self.logger.error('Could not find profile contains script >>> {}'.format(script_id))
        return None

    def find_running_profile_contains_script(self, identifier: str)->List[Profile]:
        return list(filter(lambda x: x.has_script(identifier) and x.is_running(), self.repository.profile_list))

    def get_profile_scripts(self, identifier)->List[Script]:
        scripts = []
        profile = self.find(identifier)
        if not profile:
            return []

        for script_id in profile.script_id_list:
            scripts.append(self.library_service.find_script(script_id))

        return scripts

    # endregion find

    # region remove

    def remove(self, identifier):
        profile = self._profile_exists(identifier)
        if not profile:
            return

        # can be removed if not running
        if not profile.is_running():
            self.repository.remove(profile)
            return

        # trying to stop script before remove
        for profile in self.repository.profile_list:
            for script_id in profile.script_id_list:
                self.remove_script(script_id)

        self.repository.remove(profile)

    def remove_script(self, identifier: str):
        script = self.find_script(identifier)
        if not script:
            return

        # get all profiles and libraries currently running contains script
        profiles = self.find_running_profile_contains_script(script.identifier())
        library = self.library_service.find_library_contains_script(script.identifier())

        # check to see anything is running other than this script
        if len(profiles) == 1 and not library:
            self.script_manager.stop(script)

        for profile in self.repository.profile_list:
            if profile.has_script(identifier):
                profile.remove(identifier)

        # endregion remove

        # region command

    def start(self, name: str):
        profile = self._profile_exists(name)
        if not profile:
            return

        self.profile_manager.start(profile)

    def stop(self, name: str):
        profile = self._profile_exists(name)
        if not profile:
            return

        self.profile_manager.stop(profile)

    def restart(self, name: str):
        profile = self._profile_exists(name)
        if not profile:
            return

        self.profile_manager.restart(profile)

    def refresh(self):
        for profile in self.repository.profile_list:
            self.profile_manager.refresh(profile)

    # endregion command

    # region public methods

    def get_next_profile_name(self) -> str:
        name = 'profile'
        if not self.repository.find(name):
            return name

        i = 0
        while True:
            i += 1
            if not self.repository.find(name + str(i)):
                return name

    # endregion public methods

    # region private methods

    def _profile_exists(self, name: str) -> Profile:
        profile = self.repository.find(name)
        if not profile:
            self.message_service.add(Message(MessageType.ERROR, 'Could not find profile: {}'.format(name)))
            self.logger.error('Could not find profile >>> {}'.format(name))
            return None

        return profile

    # endregion private methods
