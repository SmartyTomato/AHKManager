from typing import List
from typing import Tuple

from core.manager.library_manager import LibraryManager
from core.manager.script_manager import ScriptManager
from core.model.action_result import ActionResult
from core.model.error_messages import ErrorMessages
from core.model.library import Library
from core.model.library_repository import LibraryRepository
from core.model.script import Script
from core.model.singleton import Singleton
from core.utility.utility import Utility


class LibraryService(metaclass=Singleton):

    library_manager: LibraryManager = LibraryManager()
    script_manager: ScriptManager = ScriptManager()

    def __init__(self):
        self.repository: LibraryRepository = LibraryRepository()

    # region add

    def add(self, path: str) -> Tuple[ActionResult, LibraryRepository]:
        """
        Initialize and add library into repository using given path
        If library already exists, add extra script into library.
        Do not remove non exists script, call refresh instead

        Args:
            path (str): directory path

        Returns:
            Tuple[ActionResult, LibraryRepository]:
                ActionResult: return error when the given
                    directory path is invalid
        """

        result = ActionResult()
        path = Utility.format_path(path)

        # check whether path is as valid directory
        if not Utility.is_dir(path):
            result.add_error(
                ErrorMessages.path_is_not_directory_path.format(path))
            return result, self.repository

        # add path itself to list
        library = self.find(path)
        if not library:
            temp_result, library = self.library_manager.init_library(path)
            result.merge(temp_result)

            if temp_result.success() and library:
                self.repository.add(library)
        else:
            # Library already in the repository, refresh library
            self.library_manager.reload(library)

        # initialize all sub directories
        directories = Utility.get_directories(path)

        for directory in directories:
            library = self.find(directory)

            if not library:
                # create library object
                temp_result, library = \
                    self.library_manager.init_library(directory)
                result.merge(temp_result)

                if temp_result.success() and library:
                    self.repository.add(library)
            else:
                # Library already in the repository, refresh library
                self.library_manager.reload(library)

        # ignore errors, initialize library only return warning,
        # as some library may success
        result.ignore_error()
        return result, self.repository

    # endregion add

    # region find

    def find(self, identifier: str) -> Library:
        """
        Get library using library ID

        Args:
            identifier (str): library path

        Returns:
            Library: library object or None
        """

        Utility.format_path(identifier)
        return self.repository.find(identifier)

    def find_script(self, identifier: str) -> Script:
        """
        Get script using script ID

        Args:
            identifier (str): script path

        Returns:
            Script: script object or None
        """

        return self.repository.find_script(identifier)

    def find_library_contains_script(self, identifier: str) -> Library:
        """
        Get library which contains the given script ID

        Args:
            identifier (str): script path

        Returns:
            Library: library or None
        """

        return next((x for x in self.repository.library_list
                     if x.has_script(identifier)), None)

    # endregion find

    # region remove

    def remove(self, identifier: str) -> ActionResult:
        """
        Remove library using libray ID

        Args:
            identifier (str): library path

        Returns:
            ActionResult: return error when failed
                to stop library and all script,
                if library not exists return warning
        """

        result = ActionResult()

        # check whether library exists
        temp_result, library = self._check_library_exists(identifier)
        if not temp_result.success() or not library:
            temp_result.ignore_error()
            return temp_result

        # remove library along with the scripts
        temp_result = self.library_manager.remove(library)
        result.merge(temp_result)

        # remove library from the repository when everything is removed
        if temp_result.success():
            self.repository.remove(library)

        return result

    def remove_script(self, identifier: str) -> ActionResult:
        """
        Remove script using script ID

        Args:
            identifier (str): script path

        Returns:
            ActionResult: return error when failed
                to stop script,
                if script not exists return warning
        """

        result = ActionResult()

        temp_result, script = self._check_script_exists(identifier)
        if not temp_result.success() or not script:
            temp_result.ignore_error()
            return temp_result

        # trying to stop script before remove
        temp_result = self.script_manager.remove(script)
        result.merge(temp_result)

        if temp_result.success():
            # find library containning script
            library = self.find_library_contains_script(identifier)
            library.remove(script)

        return result

    # endregion remove

    # region command

    def start(self, identifier: str) -> Tuple[ActionResult, Library]:
        """
        Start library using library ID

        Args:
            identifier (str): libray path

        Returns:
            Tuple[ActionResult, Library]:
                ActionResult: return error when library
                    is not found
        """

        temp_result, library = self._check_library_exists(identifier)
        if not temp_result.success() or not library:
            return temp_result, None

        return self.library_manager.start(library)

    def start_script(self, identifier: str) -> Tuple[ActionResult, Script]:
        """
        Start script using script ID

        Args:
            identifier (str): script path

        Returns:
            Tuple[ActionResult, Script]:
                ActionResult: return error when script
                    is not found
        """

        temp_result, script = self._check_script_exists(identifier)
        if not temp_result.success() or not script:
            return temp_result, None

        return self.script_manager.start(script)

    def restart_script(self, identifier: str) -> Tuple[ActionResult, Script]:
        """
        Restart script using script ID

        Args:
            identifier (str): script path

        Returns:
            Tuple[ActionResult, Script]:
                ActionResult: return error when script
                    is not found
        """

        temp_result, script = self._check_script_exists(identifier)
        if not temp_result.success() or not script:
            return temp_result, None

        return self.script_manager.restart(script)

    def stop(self, identifier: str) -> Tuple[ActionResult, Library]:
        """
        Stop library using library ID

        Args:
            identifier (str): library path

        Returns:
            Tuple[ActionResult, Library]:
                ActionResult: return error when library
                    is not found
        """

        temp_result, library = self._check_library_exists(identifier)
        if not temp_result.success() or not library:
            return temp_result, None

        return self.library_manager.stop(library)

    def stop_script(self, identifier: str) -> Tuple[ActionResult, Script]:
        """
        Stop script using script ID

        Args:
            identifier (str): script path

        Returns:
            Tuple[ActionResult, Script]:
                ActionResult: return error when script
                    is not found
        """

        temp_result, script = self._check_script_exists(identifier)
        if not temp_result.success() or not script:
            return temp_result, None

        return self.script_manager.stop(script)

    def stop_all(self) -> ActionResult:
        """
        Stop all library in the repository

        Returns:
            ActionResult: return only warning messages
        """

        result = ActionResult()

        for library in self.repository.library_list:
            temp_result, library = self.library_manager.stop(library)
            result.merge(temp_result)

        result.ignore_error()
        return result

    # endregion command

    # region public methods

    def refresh(self) -> Tuple[ActionResult, LibraryRepository]:
        """
        Refresh library repository, check whether library exists.
        The library not exists on the disk will be removed from
        the repository

        Returns:
            Tuple[ActionResult, LibraryRepository]:
                ActionResult: return warning message only
        """

        result = ActionResult()

        for library in self.repository.library_list:
            temp_result, library = self.library_manager.refresh(library)

            if not temp_result.success() or not library:
                # only return error when library path is not exists,
                # remove library from the list
                self.repository.remove(library)

        result.ignore_error()
        return result, self.repository

    def get_all_scripts(self) -> List[Script]:
        """
        Get all scripts in the repository

        Returns:
            List[Script]: list of all the scripts
        """

        return self.repository.get_all_scripts()

    # endregion public methods

    # region private methods

    def _check_library_exists(self, identifier: str) \
            -> Tuple[ActionResult, Library]:
        result = ActionResult()

        library = self.find(identifier)
        if not library:
            result.add_error(
                ErrorMessages.could_not_find_library.format(identifier))

        return result, library

    def _check_script_exists(self, identifier: str) \
            -> Tuple[ActionResult, Script]:
        result = ActionResult()

        script = self.find_script(identifier)
        if not script:
            result.add_error(
                ErrorMessages.could_not_find_script.format(identifier))
            return result, None

        return result, script

    # endregion private methods

    # def delete_library(self, path: str):
    #     library = self._library_exists(path)
    #     if not library:
    #         return

    #     success = self.library_manager.delete(library)
    #     if not success:
    #         self.message_service.add(
    #             Message(MessageType.ERROR, 'Could not delete library: {}'\
    # .format(library.path)))
    #         self.logger.error('Could not delete library >>> {}'.format(
    # repr(library)))
    #         return

    #     self.repository.remove(library)

    # def add_script(self, library_path: str, script_path: str) -> Script:
    #     library = self._library_exists(library_path)
    #     if not library:
    #         return None

    #     script = self.library_manager.add_script(library, script_path)
    #     return script

    # def delete_script(self, path: str):

    #     script = self.find_script(path)

    #     if script is None:
    #         # library don't contains script
    #         self.logger.info('Script does not exists >>> {}'.format(path))
    #         return True

    #     if not self.script_manager.delete(script):
    #         return

    #     # only remove from the list when no error occurs
    #     self.repository.remove_script(script.identifier())
    #     return True
