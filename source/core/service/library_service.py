from typing import List

from core.manager.library_manager import LibraryManager
from core.manager.script_manager import ScriptManager
from core.model.library import Library
from core.model.library_repository import LibraryRepository
from core.model.script import Script
from core.model.singleton import Singleton
from core.service.message_service import MessageService
from core.utility.logger import Logger
from core.utility.message import Message, MessageType
from core.utility.utility import Utility


class LibraryService(Singleton):
    logger = Logger('LibraryService')

    message_service: MessageService = MessageService()
    library_manager: LibraryManager = LibraryManager()
    script_manager: ScriptManager = ScriptManager()

    def __init__(self):
        self.repository: LibraryRepository = LibraryRepository()

    # region add

    def add(self, path: str):
        if not Utility.is_dir(path):
            return

        # add path itself to list
        if not self._library_duplicated(path):
            self.library_manager.init_library(path)

        # get all sub directories
        directories = Utility.get_directories(path)

        # create all library (folder) object
        for directory in directories:
            directory = Utility.format_path(directory)

            if not self._library_duplicated(directory):
                library = self.library_manager.init_library(directory)

                if library:
                    self.repository.add(library)
                else:
                    self.message_service.add(
                        Message(MessageType.ERROR, 'Could not initialize library: {}'.format(directory)))
                    self.logger.error('Could not initialize library >>> {}'.format(directory))

    # endregion add

    # region find

    def find(self, identifier: str) -> Library:
        library = self.repository.find(identifier)
        if not library:
            self.logger.info('Could not find library >>> {}'.format(identifier))
            return None

        return library

    def find_script(self, identifier: str)->Script:
        script = self.repository.find_script(identifier)
        if not script:
            self.message_service.add(
                Message(MessageType.ERROR, 'Could not find script in the repository: {}'.format(identifier)))
            self.logger.error('Could not find script in the repository >>> {}'.format(identifier))
            return None

        return script

    def find_library_contains_script(self, identifier: str)->List[Library]:
        result = list(filter(lambda x: x.has_script(identifier), self.repository.library_list))
        return result if result else []

    # endregion find

    # region remove

    def remove(self, identifier: str):
        library = self._library_exists(identifier)
        if not library:
            return

        success = self.library_manager.remove(library)
        if success:
            self.repository.remove(library)

    def remove_script(self, identifier: str):
        script = self.find_script(identifier)
        if not script:
            return

        success = self.script_manager.remove(script)

        if not success:
            self.message_service.add(
                Message(MessageType.ERROR, 'Could not find library: {}'.format(identifier)))
            self.logger.error('Could not find library >>> {}'.format(identifier))
            return

        self.repository.remove_script(script)

    # endregion remove

    # region command

    def start(self, identifier: str):
        library = self._library_exists(identifier)
        if not library:
            return

        self.library_manager.start(library)

    def start_script(self, identifier: str):
        script = self.find_script(identifier)
        if not script:
            return

        self.script_manager.start(script)

    def stop_script(self, identifier: str):
        script = self.find_script(identifier)
        if not script:
            return

        self.script_manager.stop(script)

    def stop(self, identifier: str):
        library = self._library_exists(identifier)
        if not library:
            return

        self.library_manager.stop(library)

    def stop_all(self):
        for library in self.repository.library_list:
            self.library_manager.stop(library)

    # endregion command

    # region public methods

    def refresh(self):
        for library in self.repository.library_list:
            if not self.library_manager.refresh(library):
                self.repository.remove(library)

    def get_all_scripts(self)->List[Script]:
        return self.repository.get_all_scripts()

    # endregion public methods

    # region private methods

    def _library_exists(self, identifier: str) -> Library:
        library = self.find(identifier)

        if not library:
            self.message_service.add(
                Message(MessageType.ERROR, 'Could not find library: {}'.format(identifier)))
            self.logger.error('Could not find library >>> {}'.format(identifier))
            return None

        return library

    def _library_duplicated(self, path):
        path = Utility.format_path(path)
        library = self.find(path)
        if library:
            self.library_manager.refresh(library)
            self.message_service.add(
                Message(MessageType.WARNING, 'Library already exists, refresh: {}'.format(library.identifier())))
            self.logger.warning('Library already exists >>> {}'.format(repr(library)))
            return True

        return False

    # endregion private methods

    # def delete_library(self, path: str):
    #     library = self._library_exists(path)
    #     if not library:
    #         return

    #     success = self.library_manager.delete(library)
    #     if not success:
    #         self.message_service.add(
    #             Message(MessageType.ERROR, 'Could not delete library: {}'.format(library.path)))
    #         self.logger.error('Could not delete library >>> {}'.format(repr(library)))
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
