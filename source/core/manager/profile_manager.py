from core.manager.script_manager import ScriptManager
from core.model.profile import Profile
from core.model.script import Script
from core.model.singleton import Singleton
from core.service.library_service import LibraryService
from core.utility.logger import Logger
from core.utility.message import Message, MessageType
from core.service.message_service import MessageService


class ProfileManager(Singleton):
    logger = Logger('ProfileManager')

    library_service: LibraryService = LibraryService()
    script_manager = ScriptManager()
    message_service: MessageService = MessageService()

    def init_profile(self, name: str) -> Profile:
        return Profile(name)

    # region command

    def start(self, profile: Profile):
        for script_id in profile.script_id_list:
            script = self.library_service.find_script(script_id)
            if script:
                self.script_manager.start(script)
            else:
                self.message_service.add(
                    Message(MessageType.ERROR, 'Could not find script: {}'.format(script_id)))
                self.logger.error('Could not find script >>> {}'.format(script_id))

        profile.start()

    def stop(self, profile: Profile):
        for script_id in profile.script_id_list:
            script = self.library_service.find_script(script_id)
            if script:
                self.script_manager.stop(script)
            else:
                self.message_service.add(
                    Message(MessageType.ERROR, 'Could not find script: {}'.format(script_id)))
                self.logger.error('Could not find script >>> {}'.format(script_id))

        profile.stop()

    def restart(self, profile: Profile):
        for script_id in profile.script_id_list:
            script = self.library_service.find_script(script_id)
            if script:
                self.script_manager.restart(script)
            else:
                self.message_service.add(
                    Message(MessageType.ERROR, 'Could not find script: {}'.format(script_id)))
                self.logger.error('Could not find script >>> {}'.format(script_id))

        profile.start()

    def refresh(self, profile: Profile):
        for script_id in profile.script_id_list:
            script = self.library_service.find_script(script_id)

            if script:
                success = self.script_manager.refresh(script)
                # remove from the script list script failed to refresh
                if not success:
                    profile.remove(script)
                    self.logger.info(
                        'Remove non-exist script from profile >>> Profile: {profile} | Script: {script}'.format(
                            profile=repr(profile), script=repr(script)))
            else:
                self.message_service.add(
                    Message(MessageType.ERROR, 'Could not find script: {}'.format(script_id)))
                self.logger.error('Could not find script >>> {}'.format(script_id))

    # endregion command

    # region public methods

    def add_script(self, profile: Profile, script: Script):
        if not profile or not script:
            return

        profile.add(script.identifier())

        if profile.is_running():
            self.script_manager.start(script)

    # endregion public methods
