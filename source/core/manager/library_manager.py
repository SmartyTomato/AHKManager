from core.manager.script_manager import ScriptManager
from core.model.library import Library
from core.model.script import Script
from core.model.singleton import Singleton
from core.service.message_service import MessageService
from core.utility.logger import Logger
from core.utility.message import Message, MessageType
from core.utility.utility import Utility


class LibraryManager(Singleton):
    logger = Logger('LibraryManager')

    message_service = MessageService()
    script_manager = ScriptManager()

    def init_library(self, path: str) -> Library:
        path = Utility.format_path(path)

        if not Utility.is_dir(path):
            return None

        # add script in the directory into the list
        files = Utility.get_files_in_directory(path)

        if not files:
            self.message_service.add(Message(MessageType.WARNING, 'Empty directory: {}'.format(path)))
            self.logger.warning('Empty directory >>> {}'.format(path))
            return None

        library = Library(path)

        # initialize script file
        for file in files:
            if self.script_manager.is_script_file(file):
                script = self.script_manager.init_script(file)

                # only add script when no error returned.
                if script:
                    library.add(script)
                else:
                    self.message_service.add(Message(MessageType.ERROR, 'Could not initialize script: {}'.format(file)))
                    self.logger.error('Could not initialize script >>> {}'.format(file))
            else:
                # add warning when file is not script
                self.message_service.add(Message(MessageType.WARNING, 'Path is not a script file: {}'.format(file)))
                self.logger.warning('Path is not a script file >>> {}'.format(file))

        return library

    def refresh(self, library: Library) -> bool:
        if not library.exists():
            self.message_service.add(Message(MessageType.WARNING, 'Library does not exists: {}'.format(library.path)))
            self.logger.warning('Library does not exists >>> {}'.format(repr(library)))
            return False

        # fresh all script in the library
        # remove script that is not found
        for script in library.script_list:
            # remove from the script list script failed to refresh
            if not self.script_manager.refresh(script):
                library.remove(script)
                self.logger.info(
                    'Remove non-exist script from library >>> Library: {library} | Script: {script}'.format(
                        library=repr(library), script=repr(script)))

        return True

    # region public methods

    def add_script(self, library: Library, path: str) -> Script:
        # This directory is missing
        if not library.exists():
            self.message_service.add(
                Message(MessageType.ERROR, 'Library path does not exists: {}'.format(library.path)))
            self.logger.error('Library path does not exists >>> {}'.format(repr(library)))
            return None

        # check whether path is a file before copy the file to the directory
        if not self.script_manager.is_script_file(path):
            self.message_service.add(
                Message(MessageType.ERROR, 'Path is not a script file: {}'.format(path)))
            self.logger.error('Path is not a script file >>> {}'.format(path))
            return None

        # generate script path in the library
        file_name = Utility.get_file_name(path)
        script_path = Utility.join_path(library.path, file_name)

        # copy script file into library folder
        if not Utility.copy_file(path, script_path):
            return None

        # initialize script with the new file path
        script = self.script_manager.init_script(script_path)

        if not script:
            self.message_service.add(
                Message(MessageType.ERROR, 'Could not initialize script: {}'.format(script_path)))
            self.logger.error('Could not initialize script >>> {}'.format(script_path))
            return None

        library.repository.add(script)
        return script

    def remove(self, library: Library) -> bool:
        has_error = False
        for script in library.script_list:
            success = self.script_manager.remove(script)
            if success:
                library.remove(script)
            else:
                has_error = True

        if has_error:
            self.message_service.add(Message(MessageType.ERROR,
                                             'Could not remove library, some script can not be removed: {}'.format(
                                                 library.path)))
            self.logger.error(
                'Could not remove library, some script can not be removed >>> {}'.format(repr(library)))
            return False

        return True

    # endregion public methods

    # region command

    def start(self, library: Library):
        for script in library.script_list:
            self.script_manager.start(script)

        library.start()

    def stop(self, library: Library):
        for script in library.script_list:
            self.script_manager.stop(script)

        library.stop()

    # endregion command

    # def delete(self, library: Library) -> bool:
    #     # if folder not exists, nothing should be done
    #     if not library.exists():
    #         self.logger.info('Library path does not exist >>> {}'.format(repr(library)))
    #         return True

    #     has_error = False

    #     # delete scripts in the library
    #     for script in library.script_list:
    #         success = self.script_manager.delete(script)
    #         # remove script from the list when script is deleted successfully
    #         if success:
    #             library.remove(script)
    #         else:
    #             has_error = True

    #     # do not delete library when any file Could not delete or script list has items.
    #     if has_error or library.script_list:
    #         self.message_service.add(
    #             Message(MessageType.ERROR,
    #                     'Could not delete library, some script can not be deleted: {}'.format(library.path)))
    #         self.logger.error(
    #             'Could not delete library, some script can not be deleted >>> {}'.format(repr(library)))
    #         return False

    #     # delete directory when no error occurs
    #     return Utility.remove_dir(library.path)
