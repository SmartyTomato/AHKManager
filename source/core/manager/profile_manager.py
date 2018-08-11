from typing import Tuple

from core.manager.script_manager import ScriptManager
from core.model.action_result import ActionResult
from core.model.error_messages import ErrorMessages
from core.model.profile import Profile
from core.model.script import Script
from core.model.singleton import Singleton
from core.service.library_service import LibraryService


class ProfileManager(Singleton):

    library_service: LibraryService = LibraryService()
    script_manager: ScriptManager = ScriptManager()

    def init_profile(self, name: str) -> Tuple[ActionResult, Profile]:
        """
        Initialize profile

        Args:
            name (str): profile name

        Returns:
            Tuple[ActionResult, Profile]:
        """

        result = ActionResult()
        profile = Profile(name)
        return result, profile

    # region command

    def start(self, profile: Profile) -> Tuple[ActionResult, Profile]:
        """
        Start profile and all its scripts

        Args:
            profile (Profile): profile object

        Returns:
            Tuple[ActionResult, Profile]:
        """

        result = ActionResult()

        for script_id in profile.script_id_list:
            temp_result, _ = self.library_service.start_script(script_id)
            result.merge(temp_result)

        profile.start()
        result.ignore_error()
        return result, profile

    def stop(self, profile: Profile) -> Tuple[ActionResult, Profile]:
        """
        Stop profile and all its scripts

        Args:
            profile (Profile):  profile object

        Returns:
            Tuple[ActionResult, Profile]:
        """

        result = ActionResult()

        for script_id in profile.script_id_list:
            temp_result, _ = self.library_service.stop_script(script_id)
            result.merge(temp_result)

        profile.stop()
        result.ignore_error()
        return result, profile

    def restart(self, profile: Profile) -> Tuple[ActionResult, Profile]:
        """
        Restart profile and all its scripts

        Args:
            profile (Profile): profile object

        Returns:
            Tuple[ActionResult, Profile]:
        """

        result = ActionResult()
        profile.stop()

        for script_id in profile.script_id_list:
            temp_result, _ = self.library_service.restart_script(script_id)
            result.merge(temp_result)

        profile.start()
        result.ignore_error()
        return result, profile

    def refresh(self, profile: Profile) -> Tuple[ActionResult, Profile]:
        """
        Refresh profile and all its script
        Script not exists will be removed from profile

        Args:
            profile (Profile): profile object

        Returns:
            Tuple[ActionResult, Profile]: [description]
        """

        result = ActionResult()

        for script_id in profile.script_id_list:
            script = self.library_service.find_script(script_id)

            if script:
                temp_result, script = self.script_manager.refresh(script)
                result.merge(temp_result)

                # remove from the script list script failed to refresh
                if not temp_result.success() or not script:
                    profile.remove(script)
            else:
                result.add_error(
                    ErrorMessages.could_not_find_script.format(script_id))

        result.ignore_error()
        return result, profile

    # endregion command

    # region public methods

    def add_script(self, profile: Profile, script: Script) \
            -> Tuple[ActionResult, Profile]:
        """
        Add script to profile

        Args:
            profile (Profile): profile object
            script (Script): script object

        Returns:
            Tuple[ActionResult, Profile]:
        """

        result = ActionResult()

        # this shouldn't happen
        if not profile or not script:
            return result, None

        profile.add(script.identifier())

        if profile.is_running():
            temp_result = self.library_service.start_script(
                script.identifier())
            result.merge(temp_result)

        return result, profile

    # endregion public methods
