from typing import Tuple

from core.manager.script_manager import ScriptManager
from core.model.action_result import ActionResult
from core.model.error_messages import ErrorMessages
from core.model.library import Library
from core.utility.utility import Utility


class LibraryManager():

    script_manager = ScriptManager()
    utility: Utility = Utility()

    def init_library(self, path: str) -> Tuple[ActionResult, Library]:
        """
        Initialize directory and all its sub-directories

        Args:
            path (str): directory path

        Returns:
            Tuple[ActionResult, Library]: return error
                when path is not directory
        """
        result = ActionResult()
        path = self.utility.format_path(path)

        # check whether path is a valid directory
        if not self.utility.is_dir(path):
            result.add_error(
                ErrorMessages.path_is_not_directory_path.format(path))
            return result, None

        files = self.utility.get_files_in_directory(path)
        if not files:
            # ignore the directory do not have any file
            result.add_warning(
                ErrorMessages.directory_is_empty.format(path))
            return result, None

        library = Library(path)
        for file in files:
            # initialize script file
            temp_result, script = self.script_manager.init_script(file)
            result.merge(temp_result)

            # only add script to the list when no error returned.
            if temp_result.success() and script:
                library.add(script)

        return result, library

    # region public methods

    def refresh(self, library: Library) \
            -> Tuple[ActionResult, Library]:
        """
        Refresh library, remove not found scripts

        Args:
            library (Library): library object

        Returns:
            Tuple[ActionResult, Library]: return error
                when library not found
        """

        result = ActionResult()

        # if library not exists, the scripts are not exists either
        if not library.exists():
            result.add_error(
                ErrorMessages.library_path_not_exists_library_removed
                .format(library.path))
            return result

        # fresh all script
        # remove script that is not found
        for script in library.script_list:
            # remove from the script list script failed to refresh
            temp_result, script = self.script_manager.refresh(script)
            result.merge(temp_result)

            if not temp_result.success() or not script:
                library.remove(script)

        return result

    def reload(self, library: Library)-> Tuple[ActionResult, Library]:
        """
        Reload library path, search for new script that not in the library

        Args:
            library (Library): library object

        Returns:
            Tuple[ActionResult, Library]:
                ActionResult: return error when library path not exists
        """
        result = ActionResult()
        # check whether path is a valid directory
        if not library.exists():
            result.add_error(
                ErrorMessages.library_path_not_exists.format(library.path))
            return result, None

        files = self.utility.get_files_in_directory(library.path)
        if not files:
            # ignore the directory do not have any file
            return result, None

        for file in files:
            script = library.find(file)

            if not script:
                # initialize script file
                temp_result, script = self.script_manager.init_script(file)
                result.merge(temp_result)

                # only add script to the list when no error returned.
                if temp_result.success() and script:
                    library.add(script)

        return result, library

    def remove(self, library: Library) -> ActionResult:
        """
        Remove library, trying to stop all scripts before removal

        Args:
            library (Library): library object

        Returns:
            ActionResult: return error if script cannot be stopped
        """

        result = ActionResult()

        # remove each script from the library
        i = 0
        while i < len(library.script_list):
            script = library.script_list[i]

            temp_result = self.script_manager.remove(script)
            result.merge(temp_result)

            if temp_result.success():
                del library.script_list[i]
                i -= 1

            i += 1

        if not result.success():
            result.add_error(
                ErrorMessages
                .could_not_remove_library_script_can_not_be_removed
                .format(library.identifier()))

        return result

    # endregion public methods

    # region command

    def start(self, library: Library) -> Tuple[ActionResult, Library]:
        """
        Start library and all its scripts

        Args:
            library (Library): library object

        Returns:
            Tuple[ActionResult, Library]:
                ActionResult: return error
                    if failed to start any scripts
        """

        result = ActionResult()

        for script in library.script_list:
            temp_result, script = self.script_manager.start(script)
            result.merge(temp_result)

        library.start()
        return result, library

    def stop(self, library: Library) -> Tuple[ActionResult, Library]:
        """
        Stop library and all its scripts

        Args:
            library (Library): libray object

        Returns:
            Tuple[ActionResult, Library]:
                ActionResult: return error
                    if failed to stop any script
        """

        result = ActionResult()

        for script in library.script_list:
            temp_result, script = self.script_manager.stop(script)
            result.merge(temp_result)

        library.stop()
        return result, library

    def pause(self, library: Library) -> Tuple[ActionResult, Library]:
        """
        Pause library and all scripts

        Args:
            library (Library):

        Returns:
            Tuple[ActionResult, Library]:
                return error when script cannot be stopped
        """

        result = ActionResult()
        if library.is_running():
            library.pause()

        for script in library.script_list:
            temp_result, script = self.script_manager.pause(script)
            result.merge(temp_result)

        return result, library

    def resume(self, library: Library) -> Tuple[ActionResult, Library]:
        """
        Resume library and all scripts

        Args:
            library (Library):

        Returns:
            Tuple[ActionResult, Library]:
        """

        result = ActionResult()
        if library.is_paused():
            library.resume()

        for script in library.script_list:
            temp_result, script = self.script_manager.resume(script)
            result.merge(temp_result)

        return result, library

    # endregion command

    # def delete(self, library: Library) -> bool:
    #     # if folder not exists, nothing should be done
    #     if not library.exists():
    #         self.logger.info('Library path does not exist >>> {}'.format(
    #               repr(library)))
    #         return True

    #     has_error = False

    #     # delete scripts
    #     for script in library.script_list:
    #         success = self.script_manager.delete(script)
    #         # remove script from the list when script is deleted successfully
    #         if success:
    #             library.remove(script)
    #         else:
    #             has_error = True

    #     # do not delete library when any file Could not delete or script \
    #  list has items.
    #     if has_error or library.script_list:
    #         self.message_service.add(
    #             Message(MessageType.ERROR,
    #                     'Could not delete library, some script can not be \
    # deleted: {}'.format(library.path)))
    #         self.logger.error(
    # 'Could not delete library, some script can not be deleted >>> {}'.format(
    # repr(library)))
    #         return False

    #     # delete directory when no error occurs
    #     return self.utility.remove_dir(library.path)

    # def add_script(self, library: Library, path: str) -> ActionResult:
    #     result = ActionResult()

    #     # This directory is missing
    #     if not library.exists():
    #         result.add_error(ErrorMessages.library_path_not_exists.format(
    #           library.path))
    #         return result

    #     # check whether path is a file before copy the file to the directory
    #     if not self.script_manager.is_script_file(path):
    #         result.add_error(ErrorMessages.library_path_not_exists.format(
    # library.path))
    #         return result

    #     # generate script path
    #     file_name=self.utility.get_file_name(path)
    #     script_path=self.utility.join_path(library.path, file_name)

    #     # copy script file into library folder
    #     if not self.utility.copy_file(path, script_path):
    #         U
    #         return None

    #     # initialize script with the new file path
    #     script=self.script_manager.init_script(script_path)

    #     if not script:
    #         self.message_service.add(
    #             Message(MessageType.ERROR,
    #  'Could not initialize script: {}'.format(script_path)))
    #         self.logger.error('Could not initialize script >>> {}'.format(
    # script_path))
    #         return None

    #     library.repository.add(script)
    #     return script
