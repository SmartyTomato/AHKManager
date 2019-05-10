from typing import List
from typing import Tuple

from core.manager.profile_manager import ProfileManager
from core.manager.script_manager import ScriptManager
from core.model.action_result import ActionResult
from core.model.error_messages import ErrorMessages
from core.model.profile import Profile
from core.model.profile_repository import ProfileRepository
from core.model.script import Script
from core.service.library_service import library_service


class ProfileService:
    profile_manager: ProfileManager = ProfileManager()
    script_manager: ScriptManager = ScriptManager()

    repository: ProfileRepository = ProfileRepository()

    # region add

    def add(self, name: str = '') -> Tuple[ActionResult, Profile]:
        """
        Add profile into repository
            name (str, optional): Defaults to ''. Profile name can auto
                generate when not provided

        Returns:
            ActionResult: return error when profile name already exists
        """

        result = ActionResult()

        # * Check whether profile already exists
        profile = self.repository.find(name)
        if profile:
            result.add_error(
                ErrorMessages.profile_name_already_exists.format(name))
            return result, None

        # * Auto generate next available name
        if not name:
            name = self._get_next_profile_name()

        # * Initialize profile
        temp_result, profile = self.profile_manager.init_profile(name)
        result.merge(temp_result)
        if result.success() and profile:
            self.repository.add(profile)

        return result, profile

    def add_script(self, profile_id: str, script_id: str) \
            -> Tuple[ActionResult, Profile]:
        """
        Add script into profile

        Args:
            profile_name (str): profile name
            script_id (str): script path

        Returns:
            Tuple[ActionResult, Profile]:
                ActionResult: return error when profile
                    or script not found
        """

        result = ActionResult()

        # check whether profile exists
        temp_result, profile = self._check_profile_exists(profile_id)
        if not temp_result.success() or not profile:
            return result, None

        # find profile
        profile = self.find(profile_id)
        if profile.has_script(script_id):
            result.add_warning(
                ErrorMessages.profile_already_contains_script
                .format(script_id))
            return result, profile

        # find script
        script = library_service.find_script(script_id)
        if not script:
            result.add_error(
                ErrorMessages.could_not_find_script.format(script_id))
            return result, None

        return self.profile_manager.add_script(profile, script)

    # endregion add

    # region find

    def find(self, identifier: str) -> Profile:
        """
        Find profile

        Args:
            identifier (str): profile name

        Returns:
            Profile: profile object or None
        """

        return self.repository.find(identifier)

    def find_script(self, identifier: str) -> Script:
        """
        Find script, the script must exists in at least one profile

        Args:
            identifier (str): script path

        Returns:
            Script: return None if script not found or
                no profile contains profile
        """

        profile = self.find_profiles_contains_script(identifier)
        if not profile:
            return None

        return library_service.find_script(identifier)

    def find_profiles_contains_script(self, identifier: str) -> List[Profile]:
        """
        Find profiles that contains the script

        Args:
            identifier (str): script path

        Returns:
            List[Profile]: list of profiles
        """

        return list(filter(lambda x: x.has_script(identifier),
                           self.repository.profile_list))

    def find_running_profiles_contains_script(self, identifier: str) \
            -> List[Profile]:
        """
        Find current running profiles that contains script ID

        Args:
            identifier (str): script path

        Returns:
            List[Profile]: list of profiles
        """

        return list(filter(lambda x: x.is_running()
                           and x.has_script(identifier),
                           self.repository.profile_list))

    def get_profile_scripts(self, identifier: str) -> List[Script]:
        """
        Get script in the given profile

        Args:
            identifier (str): profile name

        Returns:
            List[Script]: list of scripts
        """

        scripts = []
        profile = self.find(identifier)
        if not profile:
            return []

        for script_id in profile.script_id_list:
            script = library_service.find_script(script_id)
            if script:
                scripts.append(script)

        return scripts

    # endregion find

    # region remove

    def remove(self, identifier: str) -> ActionResult:
        """
        Remove profile
        Profile will be removed from the repository even when script cannot
        be stopped

        Args:
            identifier (str): profile name

        Returns:
            ActionResult: return error if profile not
                found
                return warning if script cannot be
                stopped
        """

        result = ActionResult()

        temp_result, profile = self._check_profile_exists(identifier)
        if not temp_result.success() or not profile:
            temp_result.ignore_error()
            return temp_result, None

        # can be removed if not running
        if not profile.is_running():
            self.repository.remove(profile)
            return result

        # trying to stop script before remove
        for profile in self.repository.profile_list:
            i = 0
            while i < len(profile.script_id_list):
                script_id = profile.script_id_list[i]

                temp_result = self.remove_script_from_profile(
                    profile.identifier(), script_id)
                result.merge(temp_result)

                if temp_result.success():
                    i -= 1

                i += 1

        self.repository.remove(profile)
        result.ignore_error()
        return result

    def remove_script_from_profile(self, profile_id: str, script_id: str) \
            -> ActionResult:
        """
        Remove script from profile

        Args:
            profile_id (str): profile name
            script_id (str): script path

        Returns:
            ActionResult: return error when profile
                or script not found
        """

        result = ActionResult()

        temp_result, profile = self._check_profile_exists(profile_id)
        if not temp_result.success() or not profile:
            return temp_result

        if script_id not in profile.script_id_list:
            result.add_warning(
                ErrorMessages.script_not_in_profile
                .format(profile=profile.identifier(), script=script_id))
            return result

        # try to stop script if no one else if running this script
        # get all profiles and libraries currently running contains script
        profiles = self.find_running_profiles_contains_script(script_id)
        library = library_service.find_library_contains_script(script_id)

        # check to see anything is running other than this script
        if len(profiles) <= 1 and not (library and library.is_running()):
            temp_result, _ = library_service.stop_script(
                script_id)
            result.merge(temp_result)

        # script will be removed even has error
        profile.remove(script_id)
        result.ignore_error()
        return result

    def remove_script(self, identifier: str) -> ActionResult:
        """
        Remove ID from all profiles.
        If path ID is library, remove all script in that library

        Args:
            identifier (str): script path or library path

        Returns:
            ActionResult: return warning only
        """

        result = ActionResult()

        # if identifier is a library, delete all script belongs to that library
        library = library_service.find(identifier)
        if library:
            for script in library.script_list:
                profiles = self.find_profiles_contains_script(
                    script.identifier())

                if profiles:
                    for profile in profiles:
                        profile.remove(script.identifier())
        else:
            profiles = self.find_profiles_contains_script(identifier)
            if profiles:
                for profile in profiles:
                    profile.remove(identifier)

        result.ignore_error()
        return result

    # endregion remove

    # region command

    def start(self, identifier: str) -> Tuple[ActionResult, Profile]:
        """
        Start profile

        Args:
            identifier (str): profile name

        Returns:
            Tuple[ActionResult, Profile]:
                ActionResult: return error if profile
                    not found
        """

        temp_result, profile = self._check_profile_exists(identifier)
        if not temp_result.success() or not profile:
            return temp_result, None

        return self.profile_manager.start(profile)

    def stop(self, identifier: str) -> Tuple[ActionResult, Profile]:
        """
        Stop profile

        Args:
            identifier (str): profile name

        Returns:
            Tuple[ActionResult, Profile]:
                ActionResult: return error if profile
                    not found
        """

        temp_result, profile = self._check_profile_exists(identifier)
        if not temp_result.success() or not profile:
            return temp_result, None

        return self.profile_manager.stop(profile)

    def stop_all(self) -> ActionResult:
        """
        Stop all script in repository

        Returns:
            ActionResult: only return warning
        """

        result = ActionResult()

        for profile in self.repository.profile_list:
            temp_result, profile = self.profile_manager.stop(profile)
            result.merge(temp_result)

        result.ignore_error()
        return result

    def restart(self, identifier: str) -> ActionResult:
        """
        Restart profile with the given ID

        Args:
            identifier (str): profile name

        Returns:
            ActionResult: return error when profile
                not found
        """

        temp_result, profile = self._check_profile_exists(identifier)
        if not temp_result.success() or not profile:
            return temp_result

        return self.profile_manager.restart(profile)

    def refresh(self) -> Tuple[ActionResult, ProfileRepository]:
        """
        Refresh profile repository, remove script which not found

        Returns:
            Tuple[ActionResult, ProfileRepository]:
        """

        result = ActionResult()

        for profile in self.repository.profile_list:
            temp_result, profile = self.profile_manager.refresh(profile)
            result.merge(temp_result)

        result.ignore_error()
        return result, self.repository

    # endregion command

    # region public methods

    def _get_next_profile_name(self) -> str:
        name = 'profile'
        if not self.repository.find(name):
            return name

        i = 0
        while True:
            i += 1
            name = name + str(i)
            if not self.repository.find(name):
                return name

    # endregion public methods

    # region private methods

    def _check_profile_exists(self, identifier: str) \
            -> Tuple[ActionResult, Profile]:
        result = ActionResult()

        profile = self.find(identifier)
        if not profile:
            result.add_error(
                ErrorMessages.could_not_find_profile.format(identifier))
            return result, None

        return result, profile

    # endregion private methods


profile_service = ProfileService()
